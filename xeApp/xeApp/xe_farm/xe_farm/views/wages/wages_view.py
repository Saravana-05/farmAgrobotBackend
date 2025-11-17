from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from django.db import transaction
from ...models import Employee, Wage
from ...serializers import WageSerializer
from django.db.models import Sum, Q

@api_view(['POST'])
def save_wage_data(request):
    """
    Save wage data for multiple employees
    
    Request format:
    {
        "employees": [1, 2, 3],  # Array of employee IDs
        "amount": 25000.00,
        "effective_from": "2024-01-01",
        "effective_to": "2024-12-31",  # Optional
        "remarks": "Annual salary update"  # Optional
    }
    """
    try:
        # Check if request has any data
        if not request.data:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Debug logging
        print(f"Request data: {request.data}")
        
        # Extract and validate employees array
        employee_ids = request.data.get('employees', [])
        if not employee_ids or not isinstance(employee_ids, list):
            return Response({
                'status': 'error',
                'message': 'Employees field is required and must be an array'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate that we have at least one employee
        if len(employee_ids) == 0:
            return Response({
                'status': 'error',
                'message': 'At least one employee must be selected'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract common wage data
        wage_data = {
            'amount': request.data.get('amount'),
            'effective_from': request.data.get('effective_from'),
            'effective_to': request.data.get('effective_to'),
            'remarks': request.data.get('remarks', '')
        }
        
        print(f"Processing wage data for {len(employee_ids)} employees: {employee_ids}")
        print(f"Wage data: {wage_data}")
        
        # Lists to store results
        successful_wages = []
        failed_employees = []
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            # Validate all employees first
            valid_employees = []
            for emp_id in employee_ids:
                try:
                    # Convert to int if it's a string
                    if isinstance(emp_id, str):
                        emp_id = int(emp_id)
                    
                    employee = Employee.objects.get(id=emp_id)
                    
                    # Check if employee is active
                    if not employee.status:
                        failed_employees.append({
                            'employee_id': emp_id,
                            'employee_name': employee.name,
                            'error': 'Cannot add wage for inactive employee'
                        })
                        continue
                    
                    valid_employees.append(employee)
                    
                except Employee.DoesNotExist:
                    failed_employees.append({
                        'employee_id': emp_id,
                        'employee_name': f'Employee ID {emp_id}',
                        'error': 'Employee not found'
                    })
                except (ValueError, TypeError) as e:
                    failed_employees.append({
                        'employee_id': emp_id,
                        'employee_name': f'Employee ID {emp_id}',
                        'error': f'Invalid employee ID: {str(e)}'
                    })
            
            # If no valid employees, return error
            if not valid_employees:
                return Response({
                    'status': 'error',
                    'message': 'No valid employees found to create wages',
                    'failed_employees': failed_employees
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create wage records for valid employees
            for employee in valid_employees:
                try:
                    # Prepare individual wage data
                    individual_wage_data = wage_data.copy()
                    individual_wage_data['employee'] = employee.id
                    
                    # Validate the wage data using serializer
                    serializer = WageSerializer(data=individual_wage_data)
                    
                    if not serializer.is_valid():
                        failed_employees.append({
                            'employee_id': employee.id,
                            'employee_name': employee.name,
                            'error': f'Validation failed: {serializer.errors}'
                        })
                        continue
                    
                    # Create wage record
                    wage = serializer.save()
                    successful_wages.append(wage)
                    
                    print(f"SUCCESS: Created wage for {employee.name}: Rs.{wage.amount}")
                    
                except Exception as e:
                    failed_employees.append({
                        'employee_id': employee.id,
                        'employee_name': employee.name,
                        'error': f'Error creating wage: {str(e)}'
                    })
                    print(f"ERROR: Failed to create wage for {employee.name}: {e}")
        
        # Prepare response
        if successful_wages:
            # Serialize successful wages
            response_serializer = WageSerializer(successful_wages, many=True)
            
            response_data = {
                'status': 'success',
                'message': f'Successfully created {len(successful_wages)} wage record(s)',
                'data': {
                    'wages': response_serializer.data,
                    'summary': {
                        'total_requested': len(employee_ids),
                        'successful': len(successful_wages),
                        'failed': len(failed_employees)
                    }
                }
            }
            
            # Include failed employees info if any
            if failed_employees:
                response_data['data']['failed_employees'] = failed_employees
                response_data['message'] += f', {len(failed_employees)} failed'
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        else:
            # All employees failed
            return Response({
                'status': 'error',
                'message': 'Failed to create wage records for all employees',
                'data': {
                    'failed_employees': failed_employees,
                    'summary': {
                        'total_requested': len(employee_ids),
                        'successful': 0,
                        'failed': len(failed_employees)
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_wage_list(request):
    """
    Get list of wages with optional filtering, searching, and pagination
    
    Query Parameters:
    - page: Page number for pagination (default: 1)
    - limit: Number of items per page (default: 10, max: 100)
    - search: Search term to filter by employee name or contact
    - employee_id: Filter by specific employee
    - current_only: Show only current wages (true/false)
    - min_amount: Filter by minimum wage amount
    - max_amount: Filter by maximum wage amount
    - from_date: Filter wages effective from this date
    - to_date: Filter wages effective to this date
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 10)), 100)
        search = request.GET.get('search', '').strip()
        employee_id = request.GET.get('employee_id', '').strip()
        current_only = request.GET.get('current_only', '').strip().lower() == 'true'
        
        # Debug logging
        print(f"[DEBUG] Date filter params received:")
        print(f"[DEBUG] from_date: {request.GET.get('from_date', 'None')}")
        print(f"[DEBUG] to_date: {request.GET.get('to_date', 'None')}")
        
        # Start with all wages
        wages = Wage.objects.select_related('employee').all()
        
        # Apply search filter
        if search:
            wages = wages.filter(
                Q(employee__name__icontains=search) |
                Q(employee__tamil_name__icontains=search) |
                Q(employee__contact__icontains=search) |
                Q(remarks__icontains=search)
            )
        
        # Apply employee filter
        if employee_id and employee_id.isdigit():
            wages = wages.filter(employee_id=int(employee_id))
        
        # Apply current wages filter
        if current_only:
            today = date.today()
            wages = wages.filter(
                effective_from__lte=today
            ).filter(
                Q(effective_to__isnull=True) | Q(effective_to__gte=today)
            )
        
        # Apply amount filters
        min_amount = request.GET.get('min_amount', '').strip()
        if min_amount:
            try:
                wages = wages.filter(amount__gte=Decimal(min_amount))
                print(f"[DEBUG] Applied min_amount filter: {min_amount}")
            except Exception as e:
                print(f"[ERROR] Error parsing min_amount: {e}")
        
        max_amount = request.GET.get('max_amount', '').strip()
        if max_amount:
            try:
                wages = wages.filter(amount__lte=Decimal(max_amount))
                print(f"[DEBUG] Applied max_amount filter: {max_amount}")
            except Exception as e:
                print(f"[ERROR] Error parsing max_amount: {e}")
        
        # Apply date filters
        from_date = request.GET.get('from_date', '').strip()
        if from_date:
            try:
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
                # Filter wages that start on or after the from_date
                wages = wages.filter(effective_from__gte=from_date_obj)
                print(f"[DEBUG] Applied from_date filter: {from_date_obj}")
            except Exception as e:
                print(f"[ERROR] Error parsing from_date '{from_date}': {e}")
                return Response({
                    'status': 'error',
                    'message': f'Invalid from_date format. Expected YYYY-MM-DD, got: {from_date}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        to_date = request.GET.get('to_date', '').strip()
        if to_date:
            try:
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
                # Filter wages that start on or before the to_date
                wages = wages.filter(effective_from__lte=to_date_obj)
                print(f"[DEBUG] Applied to_date filter: {to_date_obj}")
            except Exception as e:
                print(f"[ERROR] Error parsing to_date '{to_date}': {e}")
                return Response({
                    'status': 'error',
                    'message': f'Invalid to_date format. Expected YYYY-MM-DD, got: {to_date}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Debug: Print final query
        print(f"[DEBUG] Final query count before pagination: {wages.count()}")
        
        # Order by effective date (newest first)
        wages = wages.order_by('-effective_from', '-created_at')
        
        # Apply pagination
        paginator = Paginator(wages, limit)
        
        # Validate page number
        if page < 1:
            page = 1
        elif page > paginator.num_pages and paginator.num_pages > 0:
            page = paginator.num_pages
        
        page_obj = paginator.get_page(page)
        
        # Serialize the data
        serializer = WageSerializer(page_obj.object_list, many=True)
        
        # Calculate summary
        total_amount = wages.aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'status': 'success',
            'message': 'Wages retrieved successfully',
            'data': {
                'wages': serializer.data,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'per_page': limit
                },
                'summary': {
                    'total_amount': float(total_amount)
                }
            }
        }, status=status.HTTP_200_OK)
        
    except ValueError as e:
        print(f"[ERROR] ValueError: {e}")
        return Response({
            'status': 'error',
            'message': 'Invalid parameter values'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def save_bulk_wage_data(request):
    """
    Alternative endpoint for bulk wage creation with different data structure
    
    Request format option 2:
    {
        "wages": [
            {
                "employee": 1,
                "amount": 25000.00,
                "effective_from": "2024-01-01",
                "effective_to": "2024-12-31",
                "remarks": "Annual salary"
            },
            {
                "employee": 2,
                "amount": 30000.00,
                "effective_from": "2024-01-01",
                "remarks": "Promotion"
            }
        ]
    }
    """
    try:
        if not request.data:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        wages_data = request.data.get('wages', [])
        if not wages_data or not isinstance(wages_data, list):
            return Response({
                'status': 'error',
                'message': 'Wages field is required and must be an array'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        successful_wages = []
        failed_wages = []
        
        with transaction.atomic():
            for i, wage_data in enumerate(wages_data):
                try:
                    # Validate individual wage data
                    serializer = WageSerializer(data=wage_data)
                    
                    if not serializer.is_valid():
                        failed_wages.append({
                            'index': i,
                            'wage_data': wage_data,
                            'error': serializer.errors
                        })
                        continue
                    
                    # Check if employee exists and is active
                    employee = serializer.validated_data.get('employee')
                    if not employee.status:
                        failed_wages.append({
                            'index': i,
                            'wage_data': wage_data,
                            'error': 'Cannot add wage for inactive employee'
                        })
                        continue
                    
                    # Create wage record
                    wage = serializer.save()
                    successful_wages.append(wage)
                    
                except Exception as e:
                    failed_wages.append({
                        'index': i,
                        'wage_data': wage_data,
                        'error': str(e)
                    })
        
        # Prepare response
        if successful_wages:
            response_serializer = WageSerializer(successful_wages, many=True)
            
            response_data = {
                'status': 'success',
                'message': f'Successfully created {len(successful_wages)} wage record(s)',
                'data': {
                    'wages': response_serializer.data,
                    'summary': {
                        'total_requested': len(wages_data),
                        'successful': len(successful_wages),
                        'failed': len(failed_wages)
                    }
                }
            }
            
            if failed_wages:
                response_data['data']['failed_wages'] = failed_wages
                response_data['message'] += f', {len(failed_wages)} failed'
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                'status': 'error',
                'message': 'Failed to create wage records',
                'data': {
                    'failed_wages': failed_wages,
                    'summary': {
                        'total_requested': len(wages_data),
                        'successful': 0,
                        'failed': len(failed_wages)
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_wage_detail(request, wage_id):
    """
    Get detailed information for a specific wage by ID
    """
    try:
        print(f"Fetching wage detail for ID: {wage_id}")
        
        # Get wage by ID or return 404
        wage = get_object_or_404(
            Wage.objects.select_related('employee'), 
            id=wage_id
        )
        
        print(f"Found wage: Employee={wage.employee.name}, Amount={wage.amount}")
        
        # Serialize the wage data
        serializer = WageSerializer(wage)
        serialized_data = serializer.data
        
        print(f"Serialized data: {serialized_data}")
        
        return Response({
            'success': True,
            'status': 'success',
            'message': 'Wage details retrieved successfully',
            'data': serialized_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error in get_wage_detail: {e}")
        return Response({
            'success': False,
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def edit_wage_data(request, wage_id):
    """
    Edit wage data - FIXED VERSION
    """
    try:
        print(f"Starting wage edit for ID: {wage_id}")
        print(f"Request data: {request.data}")
        
        # Get the wage instance
        try:
            wage = Wage.objects.select_related('employee').get(id=wage_id)
            print(f"Found existing wage: Employee={wage.employee.name}, Amount={wage.amount}")
        except Wage.DoesNotExist:
            print(f"Wage not found with ID: {wage_id}")
            return Response({
                'success': False,
                'status': 'error',
                'message': 'Wage record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if request has any data
        if not request.data:
            print("No data received in request")
            return Response({
                'success': False,
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a copy of request data for processing
        wage_data = request.data.copy()
        print(f"Original wage_data: {wage_data}")
        
        # CRITICAL FIX: Handle employee field conversion properly
        employee_id_to_validate = None
        if 'employee' in wage_data:
            employee_id_to_validate = wage_data['employee']
            # Remove 'employee' and add 'employee_id' for serializer
            wage_data.pop('employee')
            wage_data['employee_id'] = employee_id_to_validate
            print(f"Converted 'employee' to 'employee_id': {employee_id_to_validate}")
        
        # CRITICAL FIX: Validate employee exists before serializer validation
        if employee_id_to_validate is not None:
            try:
                # Handle both string and int IDs
                if isinstance(employee_id_to_validate, str):
                    employee_id_to_validate = int(employee_id_to_validate)
                
                # Check if employee exists and is active
                employee = Employee.objects.get(id=employee_id_to_validate)
                print(f"Found employee: {employee.name} (ID: {employee.id}, Active: {employee.status})")
                
                if not employee.status:
                    print(f"Employee {employee.name} is inactive")
                    return Response({
                        'success': False,
                        'status': 'error',
                        'message': f'Cannot assign wage to inactive employee: {employee.name}'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                # Update wage_data with the validated employee ID
                wage_data['employee_id'] = employee.id
                
            except Employee.DoesNotExist:
                print(f"Employee not found with ID: {employee_id_to_validate}")
                return Response({
                    'success': False,
                    'status': 'error',
                    'message': f'Employee with ID {employee_id_to_validate} not found'
                }, status=status.HTTP_404_NOT_FOUND)
            except (ValueError, TypeError) as e:
                print(f"Invalid employee ID format: {employee_id_to_validate}, Error: {e}")
                return Response({
                    'success': False,
                    'status': 'error',
                    'message': f'Invalid employee ID format: {employee_id_to_validate}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"Final wage_data for serializer: {wage_data}")
        
        # Validate the wage data (partial update allowed)
        serializer = WageSerializer(wage, data=wage_data, partial=True)
        
        if not serializer.is_valid():
            print(f"Validation failed: {serializer.errors}")
            return Response({
                'success': False,
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        print(f"Validation passed: {validated_data}")
        
        # Update wage record
        for attr, value in validated_data.items():
            old_value = getattr(wage, attr, None)
            setattr(wage, attr, value)
            print(f"Updated {attr}: {old_value} -> {value}")
        
        wage.save()
        print(f"Wage saved successfully")
        
        # Return success response
        response_serializer = WageSerializer(wage)
        return Response({
            'success': True,
            'status': 'success',
            'message': 'Wage data updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Exception in edit_wage_data: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_employee_wages(request, employee_id):
    """
    Get all wages for a specific employee
    """
    try:
        # Get employee or return 404
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Get all wages for this employee
        wages = Wage.objects.filter(employee=employee).order_by('-effective_from')
        
        # Serialize the wage data
        serializer = WageSerializer(wages, many=True)
        
        # Get current wage
        current_wage = Wage.get_current_wage(employee)
        current_wage_data = WageSerializer(current_wage).data if current_wage else None
        
        return Response({
            'status': 'success',
            'message': 'Employee wages retrieved successfully',
            'data': {
                'employee_id': employee.id,
                'employee_name': employee.name,
                'current_wage': current_wage_data,
                'wage_history': serializer.data
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_wage_statistics(request):
    """
    Get wage statistics and summary information
    """
    try:
        from django.db.models import Count, Avg, Min, Max, Sum
        
        total_wages = Wage.objects.count()
        
        # Get current wages only
        today = date.today()
        current_wages = Wage.objects.filter(
            effective_from__lte=today
        ).filter(
            Q(effective_to__isnull=True) | Q(effective_to__gte=today)
        )
        
        total_current_wages = current_wages.count()
        
        # Calculate statistics
        wage_stats = current_wages.aggregate(
            avg_wage=Avg('amount'),
            min_wage=Min('amount'),
            max_wage=Max('amount'),
            total_wage_expense=Sum('amount')
        )
        
        # Get wage distribution (ranges)
        wage_ranges = [
            {'range': '0-10000', 'count': current_wages.filter(amount__lt=10000).count()},
            {'range': '10000-25000', 'count': current_wages.filter(amount__gte=10000, amount__lt=25000).count()},
            {'range': '25000-50000', 'count': current_wages.filter(amount__gte=25000, amount__lt=50000).count()},
            {'range': '50000+', 'count': current_wages.filter(amount__gte=50000).count()},
        ]
        
        # Get recent wage changes (last 30 days)
        thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
        recent_changes = Wage.objects.filter(created_at__gte=thirty_days_ago).count()
        
        return Response({
            'status': 'success',
            'message': 'Wage statistics retrieved successfully',
            'data': {
                'summary': {
                    'total_wage_records': total_wages,
                    'current_active_wages': total_current_wages,
                    'average_wage': float(wage_stats['avg_wage'] or 0),
                    'minimum_wage': float(wage_stats['min_wage'] or 0),
                    'maximum_wage': float(wage_stats['max_wage'] or 0),
                    'total_monthly_expense': float(wage_stats['total_wage_expense'] or 0),
                    'recent_changes': recent_changes
                },
                'wage_distribution': wage_ranges
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_wage(request, wage_id):
    """
    Delete wage record
    
    Query Parameters:
    - hard_delete: true/false (default: true - wages are typically hard deleted)
    """
    try:
        # Get the wage object
        wage = get_object_or_404(Wage.objects.select_related('employee'), id=wage_id)
        
        # Store wage data for response before deletion
        wage_data = {
            'wage_id': wage.id,
            'employee_name': wage.employee.name,
            'amount': float(wage.amount),
            'effective_from': wage.effective_from,
            'effective_to': wage.effective_to
        }
        
        # Check if this is the only current wage for the employee
        if wage.is_current:
            current_wages_count = Wage.objects.filter(
                employee=wage.employee,
                effective_from__lte=date.today()
            ).filter(
                Q(effective_to__isnull=True) | Q(effective_to__gte=date.today())
            ).count()
            
            if current_wages_count == 1:
                return Response({
                    'status': 'warning',
                    'message': 'Cannot delete the only current wage for this employee. Please add a new wage first.',
                    'data': wage_data
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the wage record
        wage.delete()
        
        return Response({
            'status': 'success',
            'message': 'Wage record deleted successfully',
            'data': wage_data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def end_current_wage(request, wage_id):
    """
    End the current wage by setting effective_to date to today or specified date
    
    Request Body:
    {
        "end_date": "YYYY-MM-DD" (optional, defaults to today)
    }
    """
    try:
        # Get the wage object
        wage = get_object_or_404(Wage.objects.select_related('employee'), id=wage_id)
        
        # Check if wage is currently active (assumes you have an is_current property/method)
        # If you don't have is_current, you can check manually:
        today = date.today()
        is_currently_active = (
            wage.effective_from <= today and 
            (wage.effective_to is None or wage.effective_to >= today)
        )
        
        if not is_currently_active:
            return Response({
                'status': 'error',
                'message': 'This wage is not currently active'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if wage already has an end date
        if wage.effective_to:
            return Response({
                'status': 'error',
                'message': 'This wage already has an end date'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get end date from request or use today
        end_date = request.data.get('end_date')
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid end date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            end_date = date.today()
        
        # Validate end date
        if end_date < wage.effective_from:
            return Response({
                'status': 'error',
                'message': 'End date cannot be before the effective from date'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the wage with end date
        wage.effective_to = end_date
        wage.save(update_fields=['effective_to'])
        
        # Return success response with updated wage data
        response_serializer = WageSerializer(wage)
        return Response({
            'status': 'success',
            'message': f'Wage ended successfully on {end_date.strftime("%Y-%m-%d")}',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error in end_current_wage: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)