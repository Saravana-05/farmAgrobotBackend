from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from ...models import Employee, Wage
from ...serializers import WageSerializer
from django.db.models import Sum, Q

@api_view(['POST'])
def save_wage_data(request):
    """
    Save wage data for an employee
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
        
        # Validate the wage data
        serializer = WageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Check if employee exists and is active
        employee = validated_data.get('employee')
        if not employee.status:
            return Response({
                'status': 'error',
                'message': 'Cannot add wage for inactive employee'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create wage record
        wage = Wage.objects.create(**validated_data)
        
        # Return success response
        response_serializer = WageSerializer(wage)
        return Response({
            'status': 'success',
            'message': 'Wage data saved successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Server error: {e}")
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
        print(f"🔍 Date filter params received:")
        print(f"📅 from_date: {request.GET.get('from_date', 'None')}")
        print(f"📅 to_date: {request.GET.get('to_date', 'None')}")
        
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
                print(f"💰 Applied min_amount filter: {min_amount}")
            except Exception as e:
                print(f"❌ Error parsing min_amount: {e}")
        
        max_amount = request.GET.get('max_amount', '').strip()
        if max_amount:
            try:
                wages = wages.filter(amount__lte=Decimal(max_amount))
                print(f"💰 Applied max_amount filter: {max_amount}")
            except Exception as e:
                print(f"❌ Error parsing max_amount: {e}")
        
        # Apply date filters - FIXED LOGIC
        from_date = request.GET.get('from_date', '').strip()
        if from_date:
            try:
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
                # Filter wages that start on or after the from_date
                wages = wages.filter(effective_from__gte=from_date_obj)
                print(f"📅 Applied from_date filter: {from_date_obj}")
            except Exception as e:
                print(f"❌ Error parsing from_date '{from_date}': {e}")
                return Response({
                    'status': 'error',
                    'message': f'Invalid from_date format. Expected YYYY-MM-DD, got: {from_date}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        to_date = request.GET.get('to_date', '').strip()
        if to_date:
            try:
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
                # FIXED: Filter wages that start on or before the to_date
                # This makes more sense for date range filtering
                wages = wages.filter(effective_from__lte=to_date_obj)
                print(f"📅 Applied to_date filter: {to_date_obj}")
            except Exception as e:
                print(f"❌ Error parsing to_date '{to_date}': {e}")
                return Response({
                    'status': 'error',
                    'message': f'Invalid to_date format. Expected YYYY-MM-DD, got: {to_date}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Alternative approach if you want to filter by effective_to date instead:
        # Uncomment the block below and comment the to_date block above
        """
        to_date = request.GET.get('to_date', '').strip()
        if to_date:
            try:
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
                # Filter wages that end on or before the to_date OR are still active
                wages = wages.filter(
                    Q(effective_to__lte=to_date_obj) | 
                    Q(effective_to__isnull=True) |
                    Q(effective_from__lte=to_date_obj)  # Include wages that started before to_date
                )
                print(f"📅 Applied to_date filter (by effective_to): {to_date_obj}")
            except Exception as e:
                print(f"❌ Error parsing to_date '{to_date}': {e}")
                return Response({
                    'status': 'error',
                    'message': f'Invalid to_date format. Expected YYYY-MM-DD, got: {to_date}'
                }, status=status.HTTP_400_BAD_REQUEST)
        """
        
        # Debug: Print final query
        print(f"🔍 Final query count before pagination: {wages.count()}")
        
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
        print(f"❌ ValueError: {e}")
        return Response({
            'status': 'error',
            'message': 'Invalid parameter values'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_wage_detail(request, wage_id):
    """
    Get detailed information for a specific wage by ID - FIXED
    """
    try:
        print(f"🔍 Fetching wage detail for ID: {wage_id}")
        
        # Get wage by ID or return 404
        wage = get_object_or_404(
            Wage.objects.select_related('employee'), 
            id=wage_id
        )
        
        print(f"📋 Found wage: Employee={wage.employee.name}, Amount={wage.amount}")
        
        # Serialize the wage data
        serializer = WageSerializer(wage)
        serialized_data = serializer.data
        
        print(f"📤 Serialized data: {serialized_data}")
        
        return Response({
            'success': True,
            'status': 'success',
            'message': 'Wage details retrieved successfully',
            'data': serialized_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Error in get_wage_detail: {e}")
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
        print(f"🔄 Starting wage edit for ID: {wage_id}")
        print(f"📥 Request data: {request.data}")
        
        # Get the wage instance
        try:
            wage = Wage.objects.select_related('employee').get(id=wage_id)
            print(f"📋 Found existing wage: Employee={wage.employee.name}, Amount={wage.amount}")
        except Wage.DoesNotExist:
            print(f"❌ Wage not found with ID: {wage_id}")
            return Response({
                'success': False,
                'status': 'error',
                'message': 'Wage record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if request has any data
        if not request.data:
            print("❌ No data received in request")
            return Response({
                'success': False,
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a copy of request data for processing
        wage_data = request.data.copy()
        
        # Handle employee field - convert to employee_id if needed
        if 'employee' in wage_data:
            wage_data['employee_id'] = wage_data.pop('employee')
            print(f"🔄 Converted 'employee' to 'employee_id': {wage_data['employee_id']}")
        
        # Validate the wage data (partial update allowed)
        serializer = WageSerializer(wage, data=wage_data, partial=True)
        
        if not serializer.is_valid():
            print(f"❌ Validation failed: {serializer.errors}")
            return Response({
                'success': False,
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        print(f"✅ Validation passed: {validated_data}")
        
        # Check if employee is being changed and is active
        employee = validated_data.get('employee', wage.employee)
        if not employee.status:
            print(f"❌ Employee {employee.name} is inactive")
            return Response({
                'success': False,
                'status': 'error',
                'message': 'Cannot assign wage to inactive employee'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update wage record
        for attr, value in validated_data.items():
            old_value = getattr(wage, attr, None)
            setattr(wage, attr, value)
            print(f"🔄 Updated {attr}: {old_value} -> {value}")
        
        wage.save()
        print(f"✅ Wage saved successfully")
        
        # Return success response
        response_serializer = WageSerializer(wage)
        return Response({
            'success': True,
            'status': 'success',
            'message': 'Wage data updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Exception in edit_wage_data: {e}")
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
        
        # Check if wage is currently active
        if not wage.is_current:
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
        
        # Update the wage
        wage.effective_to = end_date
        wage.save(update_fields=['effective_to', 'updated_at'])
        
        # Return success response
        response_serializer = WageSerializer(wage)
        return Response({
            'status': 'success',
            'message': 'Wage ended successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)