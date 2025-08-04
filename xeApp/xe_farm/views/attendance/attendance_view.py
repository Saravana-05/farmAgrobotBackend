from calendar import monthrange
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from django.db.models import F

from ...models import (
    Attendance, EmployeeAttendance, EmployeeWageSummary, 
    WagePayment, Employee, Wage,generate_wage_summary
)
from ...serializers import (
    AttendanceSerializer, EmployeeAttendanceSerializer,
    CreateAttendanceSerializer, EmployeeWageSummarySerializer,
    WagePaymentSerializer, AttendanceReportSerializer,
    BulkAttendanceUpdateSerializer
)


@api_view(['POST'])
def create_daily_attendance(request):
    """
    Create daily attendance for multiple employees
    
    Request Body:
    {
        "date": "2024-01-15",
        "remarks": "Normal working day",
        "employee_attendances": [
            {
                "employee_id": 1,
                "status": "present",
                "hours_worked": 8.0,
                "overtime_hours": 0.0,
                "remarks": ""
            },
            ...
        ]
    }
    """
    try:
        print(f"📅 Creating attendance for date: {request.data.get('date')}")
        
        # Validate request data
        serializer = CreateAttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        attendance_date = validated_data['date']
        employee_attendances_data = validated_data['employee_attendances']
        
        with transaction.atomic():
            # Create main attendance record
            attendance = Attendance.objects.create(
                date=attendance_date,
                remarks=validated_data.get('remarks', ''),
                total_employees_present=0
            )
            
            print(f"✅ Created attendance record for {attendance_date}")
            
            # Create employee attendance records
            created_attendances = []
            total_present = 0
            
            for emp_data in employee_attendances_data:
                employee = Employee.objects.get(id=emp_data['employee_id'])
                
                # Create employee attendance
                emp_attendance = EmployeeAttendance.objects.create(
                    attendance=attendance,
                    employee=employee,
                    status=emp_data['status'],
                    hours_worked=emp_data.get('hours_worked', 8.0),
                    overtime_hours=emp_data.get('overtime_hours', 0.0),
                    remarks=emp_data.get('remarks', '')
                )
                
                created_attendances.append(emp_attendance)
                
                # Count present employees
                if emp_attendance.status in ['present', 'half_day', 'overtime']:
                    total_present += 1
                
                print(f"✅ Created attendance for {employee.name}: {emp_data['status']}")
            
            # Update total present count
            attendance.total_employees_present = total_present
            attendance.save(update_fields=['total_employees_present'])
            
            print(f"📊 Total employees present: {total_present}")
        
        # Return success response
        response_serializer = AttendanceSerializer(attendance)
        return Response({
            'status': 'success',
            'message': f'Daily attendance created successfully for {attendance_date}',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"❌ Error creating attendance: {e}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_attendance_list(request):
    """
    Get list of daily attendance records with filtering and pagination
    
    Query Parameters:
    - page: Page number
    - limit: Items per page
    - start_date: Filter from date (YYYY-MM-DD)
    - end_date: Filter to date (YYYY-MM-DD)
    - processed: Filter by processed status (true/false)
    - search: Search in remarks
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 10)), 100)
        start_date = request.GET.get('start_date', '').strip()
        end_date = request.GET.get('end_date', '').strip()
        processed = request.GET.get('processed', '').strip()
        search = request.GET.get('search', '').strip()
        
        # Start with all attendance records
        attendances = Attendance.objects.prefetch_related('employee_attendances__employee').all()
        
        # Apply date filters
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                attendances = attendances.filter(date__gte=start_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid start_date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                attendances = attendances.filter(date__lte=end_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid end_date format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Apply processed filter
        if processed.lower() == 'true':
            attendances = attendances.filter(is_processed=True)
        elif processed.lower() == 'false':
            attendances = attendances.filter(is_processed=False)
        
        # Apply search filter
        if search:
            attendances = attendances.filter(remarks__icontains=search)
        
        # Order by date (newest first)
        attendances = attendances.order_by('-date')
        
        # Apply pagination
        paginator = Paginator(attendances, limit)
        
        if page < 1:
            page = 1
        elif page > paginator.num_pages and paginator.num_pages > 0:
            page = paginator.num_pages
        
        page_obj = paginator.get_page(page)
        
        # Serialize data
        serializer = AttendanceSerializer(page_obj.object_list, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Attendance records retrieved successfully',
            'data': {
                'attendances': serializer.data,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'per_page': limit
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_attendance_detail(request, attendance_id):
    """Get detailed attendance information for a specific date"""
    try:
        attendance = get_object_or_404(
            Attendance.objects.prefetch_related('employee_attendances__employee'),
            id=attendance_id
        )
        
        serializer = AttendanceSerializer(attendance)
        
        return Response({
            'status': 'success',
            'message': 'Attendance details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_employee_attendance(request, attendance_id):
    """Update individual employee attendance"""
    try:
        employee_attendance = get_object_or_404(
            EmployeeAttendance.objects.select_related('employee', 'attendance'),
            id=attendance_id
        )
        
        # Check if attendance date is not too old (configurable limit)
        days_old = (date.today() - employee_attendance.attendance.date).days
        if days_old > 7:  # Don't allow changes older than 7 days
            return Response({
                'status': 'error',
                'message': 'Cannot modify attendance older than 7 days'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmployeeAttendanceSerializer(
            employee_attendance, 
            data=request.data, 
            partial=True
        )
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # Save the updated attendance
            updated_attendance = serializer.save()
            
            # Update parent attendance total count
            attendance = updated_attendance.attendance
            attendance.save()  # This will trigger the auto-calculation
        
        return Response({
            'status': 'success',
            'message': 'Employee attendance updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generate_wage_summary(request):
    """
    Generate wage summary for employees for a given period
    
    Request Body:
    {
        "employee_ids": [1, 2, 3] or null for all employees,
        "period_start": "2024-01-01",
        "period_end": "2024-01-31",
        "period_type": "monthly",
        "bonus_amount": 1000.00,
        "deduction_amount": 500.00
    }
    """
    try:
        # Validate request data
        employee_ids = request.data.get('employee_ids')
        period_start = request.data.get('period_start')
        period_end = request.data.get('period_end')
        period_type = request.data.get('period_type', 'weekly')
        bonus_amount = Decimal(str(request.data.get('bonus_amount', 0)))
        deduction_amount = Decimal(str(request.data.get('deduction_amount', 0)))
        
        if not period_start or not period_end:
            return Response({
                'status': 'error',
                'message': 'Period start and end dates are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse dates
        try:
            start_date = datetime.strptime(period_start, '%Y-%m-%d').date()
            end_date = datetime.strptime(period_end, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date < start_date:
            return Response({
                'status': 'error',
                'message': 'End date must be after start date'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get employees
        if employee_ids:
            employees = Employee.objects.filter(id__in=employee_ids, status=True)
        else:
            employees = Employee.objects.filter(status=True)
        
        created_summaries = []
        
        with transaction.atomic():
            for employee in employees:
                summary = generate_wage_summary(
                    employee=employee,
                    start_date=start_date,
                    end_date=end_date,
                    period_type=period_type
                )
                
                # Apply bonus and deductions
                if bonus_amount > 0:
                    summary.bonus_amount = bonus_amount
                if deduction_amount > 0:
                    summary.deduction_amount = deduction_amount
                
                summary.save()
                created_summaries.append(summary)
                
                print(f"✅ Generated wage summary for {employee.name}: ₹{summary.net_amount}")
        
        # Serialize response
        serializer = EmployeeWageSummarySerializer(created_summaries, many=True)
        
        return Response({
            'status': 'success',
            'message': f'Generated wage summaries for {len(created_summaries)} employees',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Complete the get_wage_summaries function
@api_view(['GET'])
def get_wage_summaries(request):
    """
    Get wage summaries with filtering and pagination
    
    Query Parameters:
    - employee_id: Filter by employee
    - payment_status: pending/partial/paid/cancelled
    - period_type: weekly/monthly/custom
    - start_date: Period start date filter
    - end_date: Period end date filter
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 10)), 100)
        employee_id = request.GET.get('employee_id', '').strip()
        payment_status = request.GET.get('payment_status', '').strip()
        period_type = request.GET.get('period_type', '').strip()
        start_date = request.GET.get('start_date', '').strip()
        end_date = request.GET.get('end_date', '').strip()
        
        # Start with all summaries
        summaries = EmployeeWageSummary.objects.select_related('employee').all()
        
        # Apply filters
        if employee_id and employee_id.isdigit():
            summaries = summaries.filter(employee_id=int(employee_id))
        
        if payment_status:
            summaries = summaries.filter(payment_status=payment_status)
        
        if period_type:
            summaries = summaries.filter(period_type=period_type)
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                summaries = summaries.filter(period_start__gte=start_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid start_date format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                summaries = summaries.filter(period_end__lte=end_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid end_date format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Order by period end date (newest first)
        summaries = summaries.order_by('-period_end', 'employee__name')
        
        # Apply pagination
        paginator = Paginator(summaries, limit)
        
        if page < 1:
            page = 1
        elif page > paginator.num_pages and paginator.num_pages > 0:
            page = paginator.num_pages
        
        page_obj = paginator.get_page(page)
        
        # Serialize data
        serializer = EmployeeWageSummarySerializer(page_obj.object_list, many=True)
        
        # Calculate summary statistics
        total_stats = summaries.aggregate(
            total_gross=Sum('gross_amount'),
            total_net=Sum('net_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount')
        )
        
        return Response({
            'status': 'success',
            'message': 'Wage summaries retrieved successfully',
            'data': {
                'summaries': serializer.data,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'per_page': limit
                },
                'statistics': {
                    'total_gross_amount': float(total_stats['total_gross'] or 0),
                    'total_net_amount': float(total_stats['total_net'] or 0),
                    'total_paid_amount': float(total_stats['total_paid'] or 0),
                    'total_pending_amount': float(total_stats['total_pending'] or 0)
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Add missing bulk update functionality
@api_view(['POST'])
def bulk_update_attendance(request):
    """
    Bulk update attendance records
    
    Request Body:
    {
        "attendance_updates": [
            {
                "employee_attendance_id": 1,
                "status": "present",
                "hours_worked": 8.0,
                "overtime_hours": 2.0,
                "remarks": "Updated status"
            },
            ...
        ]
    }
    """
    try:
        serializer = BulkAttendanceUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        updates_data = serializer.validated_data['attendance_updates']
        updated_records = []
        
        with transaction.atomic():
            for update_data in updates_data:
                employee_attendance_id = update_data.pop('employee_attendance_id')
                
                try:
                    emp_attendance = EmployeeAttendance.objects.select_related(
                        'attendance', 'employee'
                    ).get(id=employee_attendance_id)
                    
                    # Check if attendance is not too old
                    days_old = (date.today() - emp_attendance.attendance.date).days
                    if days_old > 7:
                        continue  # Skip old records
                    
                    # Update fields
                    for field, value in update_data.items():
                        setattr(emp_attendance, field, value)
                    
                    emp_attendance.save()
                    updated_records.append({
                        'id': emp_attendance.id,
                        'employee': emp_attendance.employee.name,
                        'date': emp_attendance.attendance.date,
                        'status': emp_attendance.status
                    })
                    
                except EmployeeAttendance.DoesNotExist:
                    continue  # Skip missing records
        
        return Response({
            'status': 'success',
            'message': f'Successfully updated {len(updated_records)} attendance records',
            'data': {
                'updated_records': updated_records
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Add attendance export functionality
@api_view(['GET'])
def export_attendance_report(request):
    """
    Export attendance report as CSV
    
    Query Parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - employee_ids: Comma-separated employee IDs
    - format: csv (default)
    """
    try:
        from django.http import HttpResponse
        import csv
        
        # Get parameters
        start_date = request.GET.get('start_date', '').strip()
        end_date = request.GET.get('end_date', '').strip()
        employee_ids = request.GET.get('employee_ids', '').strip()
        
        if not start_date or not end_date:
            return Response({
                'status': 'error',
                'message': 'Start date and end date are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get attendance data
        attendances = EmployeeAttendance.objects.filter(
            attendance__date__range=[start_date_obj, end_date_obj]
        ).select_related('employee', 'attendance').order_by(
            'attendance__date', 'employee__name'
        )
        
        if employee_ids:
            emp_id_list = [int(x.strip()) for x in employee_ids.split(',') if x.strip().isdigit()]
            attendances = attendances.filter(employee_id__in=emp_id_list)
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="attendance_report_{start_date}_to_{end_date}.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow([
            'Date', 'Employee Name', 'Employee ID', 'Status',
            'Hours Worked', 'Overtime Hours', 'Total Amount', 'Remarks'
        ])
        
        # Write data
        for attendance in attendances:
            writer.writerow([
                attendance.attendance.date,
                attendance.employee.name,
                attendance.employee.id,
                attendance.get_status_display(),
                attendance.hours_worked,
                attendance.overtime_hours,
                attendance.total_amount,
                attendance.remarks
            ])
        
        return response
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # ============= WAGE PAYMENT VIEWS =============

@api_view(['POST'])
def create_wage_payment(request):
    """
    Create a new wage payment
    
    Request Body:
    {
        "wage_summary_id": 1,
        "payment_date": "2024-01-15",
        "amount": 5000.00,
        "payment_mode": "cash",
        "reference_number": "TXN123",
        "paid_by": "Manager Name",
        "remarks": "Weekly payment"
    }
    """
    try:
        serializer = WagePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate wage summary exists and has pending amount
        wage_summary_id = request.data.get('wage_summary_id')
        wage_summary = get_object_or_404(EmployeeWageSummary, id=wage_summary_id)
        
        payment_amount = Decimal(str(request.data.get('amount', 0)))
        
        if payment_amount <= 0:
            return Response({
                'status': 'error',
                'message': 'Payment amount must be greater than zero'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if payment_amount > wage_summary.pending_amount:
            return Response({
                'status': 'error',
                'message': f'Payment amount (₹{payment_amount}) exceeds pending amount (₹{wage_summary.pending_amount})'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # Create payment record
            payment = serializer.save()
            
            print(f"✅ Created payment: ₹{payment.amount} for {wage_summary.employee.name}")
        
        return Response({
            'status': 'success',
            'message': 'Payment recorded successfully',
            'data': WagePaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_wage_payments(request):
    """Get wage payments with filtering and pagination"""
    try:
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 10)), 100)
        employee_id = request.GET.get('employee_id', '').strip()
        payment_mode = request.GET.get('payment_mode', '').strip()
        start_date = request.GET.get('start_date', '').strip()
        end_date = request.GET.get('end_date', '').strip()
        
        payments = WagePayment.objects.select_related(
            'wage_summary__employee'
        ).all()
        
        # Apply filters
        if employee_id and employee_id.isdigit():
            payments = payments.filter(wage_summary__employee_id=int(employee_id))
        
        if payment_mode:
            payments = payments.filter(payment_mode=payment_mode)
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                payments = payments.filter(payment_date__gte=start_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid start_date format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                payments = payments.filter(payment_date__lte=end_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid end_date format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        payments = payments.order_by('-payment_date', '-created_at')
        
        # Pagination
        paginator = Paginator(payments, limit)
        page_obj = paginator.get_page(page)
        
        serializer = WagePaymentSerializer(page_obj.object_list, many=True)
        
        # Calculate summary
        total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'status': 'success',
            'message': 'Payments retrieved successfully',
            'data': {
                'payments': serializer.data,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'per_page': limit
                },
                'summary': {
                    'total_amount_paid': float(total_amount)
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_wage_summary_detail(request, summary_id):
    """Get detailed wage summary with payment history"""
    try:
        summary = get_object_or_404(
            EmployeeWageSummary.objects.select_related('employee').prefetch_related('payments'),
            id=summary_id
        )
        
        # Get attendance records for the period
        attendance_records = EmployeeAttendance.objects.filter(
            employee=summary.employee,
            attendance__date__range=[summary.period_start, summary.period_end]
        ).select_related('attendance').order_by('attendance__date')
        
        summary_data = EmployeeWageSummarySerializer(summary).data
        attendance_data = EmployeeAttendanceSerializer(attendance_records, many=True).data
        
        return Response({
            'status': 'success',
            'message': 'Wage summary details retrieved successfully',
            'data': {
                'summary': summary_data,
                'attendance_records': attendance_data,
                'payment_history': WagePaymentSerializer(summary.payments.all(), many=True).data
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============= EMPLOYEE ATTENDANCE VIEWS =============

@api_view(['GET'])
def get_employee_attendance_history(request, employee_id):
    """Get attendance history for a specific employee"""
    try:
        employee = get_object_or_404(Employee, id=employee_id)
        
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 20)), 100)
        start_date = request.GET.get('start_date', '').strip()
        end_date = request.GET.get('end_date', '').strip()
        status_filter = request.GET.get('status', '').strip()
        
        attendances = EmployeeAttendance.objects.filter(
            employee=employee
        ).select_related('attendance').order_by('-attendance__date')
        
        # Apply filters
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                attendances = attendances.filter(attendance__date__gte=start_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid start_date format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                attendances = attendances.filter(attendance__date__lte=end_date_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid end_date format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if status_filter:
            attendances = attendances.filter(status=status_filter)
        
        # Calculate statistics
        stats = attendances.aggregate(
            total_present=Count('id', filter=Q(status='present')),
            total_absent=Count('id', filter=Q(status='absent')),
            total_half_days=Count('id', filter=Q(status='half_day')),
            total_overtime_hours=Sum('overtime_hours'),
            total_amount_earned=Sum('total_amount')
        )
        
        # Pagination
        paginator = Paginator(attendances, limit)
        page_obj = paginator.get_page(page)
        
        serializer = EmployeeAttendanceSerializer(page_obj.object_list, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Employee attendance history retrieved successfully',
            'data': {
                'employee': {
                    'id': employee.id,
                    'name': employee.name,
                },
                'attendances': serializer.data,
                'statistics': {
                    'total_records': attendances.count(),
                    'total_present': stats['total_present'] or 0,
                    'total_absent': stats['total_absent'] or 0,
                    'total_half_days': stats['total_half_days'] or 0,
                    'total_overtime_hours': float(stats['total_overtime_hours'] or 0),
                    'total_amount_earned': float(stats['total_amount_earned'] or 0),
                    'attendance_percentage': round(
                        (stats['total_present'] or 0) / max(attendances.count(), 1) * 100, 2
                    )
                },
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'per_page': limit
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============= DASHBOARD & STATISTICS VIEWS =============

@api_view(['GET'])
def get_attendance_dashboard(request):
    """Get attendance dashboard with key metrics"""
    try:
        # Get date range (default to current month)
        today = date.today()
        start_date_str = request.GET.get('start_date', f'{today.year}-{today.month:02d}-01')
        end_date_str = request.GET.get('end_date', str(today))
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'status': 'error',
                'message': 'Invalid date format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get attendance data for the period
        attendances = EmployeeAttendance.objects.filter(
            attendance__date__range=[start_date, end_date]
        ).select_related('attendance', 'employee')
        
        # Calculate key metrics
        total_employees = Employee.objects.filter(status=True).count()
        
        daily_stats = attendances.values('attendance__date').annotate(
            present_count=Count('id', filter=Q(status__in=['present', 'overtime'])),
            absent_count=Count('id', filter=Q(status='absent')),
            half_day_count=Count('id', filter=Q(status='half_day')),
            total_amount=Sum('total_amount')
        ).order_by('attendance__date')
        
        # Overall statistics
        overall_stats = attendances.aggregate(
            total_present=Count('id', filter=Q(status__in=['present', 'overtime'])),
            total_absent=Count('id', filter=Q(status='absent')),
            total_half_days=Count('id', filter=Q(status='half_day')),
            total_overtime_hours=Sum('overtime_hours'),
            total_wages_paid=Sum('total_amount')
        )
        
        # Employee-wise statistics
        employee_stats = attendances.values(
            'employee__id', 'employee__name'
        ).annotate(
            present_days=Count('id', filter=Q(status__in=['present', 'overtime'])),
            absent_days=Count('id', filter=Q(status='absent')),
            half_days=Count('id', filter=Q(status='half_day')),
            total_earned=Sum('total_amount'),
            attendance_percentage=F('present_days') * 100.0 / Count('id')
        ).order_by('-total_earned')[:10]  # Top 10
        
        # Recent attendance (last 7 days)
        recent_date = end_date - timedelta(days=6)
        recent_attendances = Attendance.objects.filter(
            date__range=[recent_date, end_date]
        ).order_by('-date')[:7]
        
        return Response({
            'status': 'success',
            'message': 'Dashboard data retrieved successfully',
            'data': {
                'period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_days': (end_date - start_date).days + 1
                },
                'overview': {
                    'total_active_employees': total_employees,
                    'total_present_records': overall_stats['total_present'] or 0,
                    'total_absent_records': overall_stats['total_absent'] or 0,
                    'total_half_day_records': overall_stats['total_half_days'] or 0,
                    'total_overtime_hours': float(overall_stats['total_overtime_hours'] or 0),
                    'total_wages_amount': float(overall_stats['total_wages_paid'] or 0),
                    'average_attendance_rate': round(
                        (overall_stats['total_present'] or 0) / 
                        max(attendances.count(), 1) * 100, 2
                    )
                },
                'daily_trends': list(daily_stats),
                'top_employees': list(employee_stats),
                'recent_attendance': AttendanceSerializer(recent_attendances, many=True).data
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_monthly_attendance_report(request):
    """Get monthly attendance report for all employees"""
    try:
        # Get month and year parameters
        month = int(request.GET.get('month', date.today().month))
        year = int(request.GET.get('year', date.today().year))
        
        if month < 1 or month > 12:
            return Response({
                'status': 'error',
                'message': 'Month must be between 1 and 12'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get month date range
        start_date = date(year, month, 1)
        _, last_day = monthrange(year, month)
        end_date = date(year, month, last_day)
        
        # Get all active employees
        employees = Employee.objects.filter(status=True).order_by('name')
        
        report_data = []
        
        for employee in employees:
            # Get attendance for this employee in the month
            attendances = EmployeeAttendance.objects.filter(
                employee=employee,
                attendance__date__range=[start_date, end_date]
            ).select_related('attendance')
            
            # Calculate statistics
            stats = attendances.aggregate(
                present_days=Count('id', filter=Q(status='present')),
                absent_days=Count('id', filter=Q(status='absent')),
                half_days=Count('id', filter=Q(status='half_day')),
                overtime_days=Count('id', filter=Q(status='overtime')),
                total_overtime_hours=Sum('overtime_hours'),
                total_amount=Sum('total_amount')
            )
            
            working_days = attendances.count()
            present_days = (stats['present_days'] or 0) + (stats['overtime_days'] or 0)
            attendance_percentage = round(present_days / max(working_days, 1) * 100, 2)
            
            employee_data = {
                'employee_id': employee.id,
                'employee_name': employee.name,
                'working_days': working_days,
                'present_days': present_days,
                'absent_days': stats['absent_days'] or 0,
                'half_days': stats['half_days'] or 0,
                'overtime_days': stats['overtime_days'] or 0,
                'total_overtime_hours': float(stats['total_overtime_hours'] or 0),
                'total_amount_earned': float(stats['total_amount'] or 0),
                'attendance_percentage': attendance_percentage
            }
            
            report_data.append(employee_data)
        
        # Calculate overall statistics
        total_stats = {
            'total_employees': len(report_data),
            'total_working_days': sum(emp['working_days'] for emp in report_data),
            'total_present_days': sum(emp['present_days'] for emp in report_data),
            'total_absent_days': sum(emp['absent_days'] for emp in report_data),
            'total_amount_paid': sum(emp['total_amount_earned'] for emp in report_data),
            'average_attendance_rate': round(
                sum(emp['attendance_percentage'] for emp in report_data) / 
                max(len(report_data), 1), 2
            )
        }
        
        return Response({
            'status': 'success',
            'message': 'Monthly attendance report generated successfully',
            'data': {
                'period': {
                    'month': month,
                    'year': year,
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_days': last_day
                },
                'employees': report_data,
                'summary': total_stats
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============= UTILITY VIEWS =============

@api_view(['POST'])
def mark_attendance_processed(request, attendance_id):
    """Mark attendance as processed (wages calculated)"""
    try:
        attendance = get_object_or_404(Attendance, id=attendance_id)
        
        if attendance.is_processed:
            return Response({
                'status': 'error',
                'message': 'Attendance is already marked as processed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        attendance.is_processed = True
        attendance.save(update_fields=['is_processed', 'updated_at'])
        
        return Response({
            'status': 'success',
            'message': 'Attendance marked as processed successfully',
            'data': {
                'attendance_id': attendance.id,
                'date': attendance.date,
                'is_processed': attendance.is_processed
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_attendance(request, attendance_id):
    """Delete attendance record (with safety checks)"""
    try:
        attendance = get_object_or_404(Attendance, id=attendance_id)
        
        # Check if attendance is not too old
        days_old = (date.today() - attendance.date).days
        if days_old > 30:  # Don't allow deletion of records older than 30 days
            return Response({
                'status': 'error',
                'message': 'Cannot delete attendance records older than 30 days'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if wages are already processed
        if attendance.is_processed:
            return Response({
                'status': 'error',
                'message': 'Cannot delete processed attendance records'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        attendance_date = attendance.date
        attendance.delete()
        
        return Response({
            'status': 'success',
            'message': f'Attendance record for {attendance_date} deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def check_attendance_exists(request):
    """Check if attendance exists for a specific date"""
    try:
        check_date = request.GET.get('date', '').strip()
        
        if not check_date:
            return Response({
                'status': 'error',
                'message': 'Date parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            check_date_obj = datetime.strptime(check_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        attendance_exists = Attendance.objects.filter(date=check_date_obj).exists()
        
        attendance_data = None
        if attendance_exists:
            attendance = Attendance.objects.get(date=check_date_obj)
            attendance_data = {
                'id': attendance.id,
                'date': attendance.date,
                'total_employees_present': attendance.total_employees_present,
                'is_processed': attendance.is_processed,
                'total_employee_records': attendance.employee_attendances.count()
            }
        
        return Response({
            'status': 'success',
            'message': 'Attendance check completed',
            'data': {
                'date': check_date_obj,
                'exists': attendance_exists,
                'attendance': attendance_data
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)