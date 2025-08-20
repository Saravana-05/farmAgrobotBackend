from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.utils import timezone
from django.db import transaction
from datetime import datetime, date, timedelta
from collections import defaultdict
from decimal import Decimal

from ...utils import get_monday_of_week, get_week_dates

from ...serializers import (
    AttendanceCreateUpdateSerializer,
    EmployeeAttendanceValidationSerializer, 
    PayWageSerializer,
    AttendanceRecordSerializer
)
from ...models import AttendanceRecord, BulkWagePayment, Employee, Wage, WeeklyWagePayment,Expense


@api_view(['POST'])
def mark_attendance(request):
    """Mark attendance for multiple employees on a specific date"""
    serializer = AttendanceCreateUpdateSerializer(
        data=request.data, 
        context={'request': request}
    )
    
    if serializer.is_valid():
        attendance_record = serializer.save()
        return Response({
            'message': 'Attendance marked successfully',
            'date': attendance_record.date.isoformat(),
            'total_entries': attendance_record.total_employees,
            'attendance_summary': {
                'present': attendance_record.total_present,
                'absent': attendance_record.total_absent,
                'half_day': attendance_record.total_half_day,
                'total_wages': float(attendance_record.calculate_daily_wages_total())
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_attendance(request, date_str):
    """Update attendance for a specific date"""
    try:
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        attendance_record = AttendanceRecord.objects.get(date=attendance_date)
    except (ValueError, AttendanceRecord.DoesNotExist):
        return Response(
            {'error': 'Invalid date format or attendance record not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AttendanceCreateUpdateSerializer(
        attendance_record,
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        attendance_record = serializer.save()
        return Response({
            'message': 'Attendance updated successfully',
            'date': attendance_record.date.isoformat(),
            'total_entries': attendance_record.total_employees,
            'attendance_summary': {
                'present': attendance_record.total_present,
                'absent': attendance_record.total_absent,
                'half_day': attendance_record.total_half_day,
                'total_wages': float(attendance_record.calculate_daily_wages_total())
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_single_attendance(request):
    """Update attendance for a single employee on a specific date"""
    employee_id = request.data.get('employee_id')
    employee_name = request.data.get('employee_name')
    attendance_date_str = request.data.get('date')
    attendance_status = request.data.get('status')
    
    if not all([employee_id, employee_name, attendance_date_str, attendance_status is not None]):
        return Response(
            {'error': 'employee_id, employee_name, date, and status are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
        # Validate employee exists and is active
        employee = Employee.objects.get(id=employee_id, status=True)
        
        # Validate employee name matches
        if employee.name != employee_name:
            return Response(
                {'error': f'Employee name mismatch. Expected: {employee.name}, Got: {employee_name}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except (ValueError, Employee.DoesNotExist) as e:
        return Response(
            {'error': 'Invalid date format, employee not found, or employee is inactive'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if employee has a current wage
    current_wage = Wage.get_current_wage(employee)
    if not current_wage:
        return Response(
            {'error': f'Employee {employee_name} does not have a current wage rate'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if wages are already paid for this week
    week_start = get_monday_of_week(attendance_date)
    wage_payment = WeeklyWagePayment.objects.filter(
        employee=employee,
        week_start_date=week_start,
        payment_status='paid'
    ).first()
    
    if wage_payment:
        return Response(
            {'error': 'Cannot update attendance. Wages already paid for this week.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    with transaction.atomic():
        # Get or create attendance record for the date
        attendance_record, created = AttendanceRecord.objects.get_or_create(
            date=attendance_date,
            defaults={'attendance_data': []}
        )
        
        wage_amount = current_wage.amount
        
        # Update employee attendance in the record
        attendance_record.update_employee_status(
            employee_id, 
            employee_name, 
            attendance_status, 
            wage_amount
        )
    
    return Response({
        'message': 'Attendance updated successfully',
        'employee_name': employee_name,
        'date': attendance_date.isoformat(),
        'status': attendance_status
    })


@api_view(['GET'])
def get_attendance(request, date_str):
    """Get attendance for a specific date"""
    try:
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        attendance_record = AttendanceRecord.objects.get(date=attendance_date)
        serializer = AttendanceRecordSerializer(attendance_record)
        return Response(serializer.data)
    except (ValueError, AttendanceRecord.DoesNotExist):
        return Response(
            {'error': 'Invalid date format or attendance record not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def get_active_employees(request):
    """Get list of all active employees with their current wages"""
    employees = Employee.objects.filter(status=True).order_by('name')
    
    employees_data = []
    employees_without_wage = []
    
    for employee in employees:
        current_wage = Wage.get_current_wage(employee)
        employee_data = {
            'employee_id': str(employee.id),
            'employee_name': employee.name,
            'daily_wage': float(current_wage.amount) if current_wage else 0.0,
            'has_wage': current_wage is not None
        }
        
        employees_data.append(employee_data)
        
        if not current_wage:
            employees_without_wage.append(employee.name)
    
    response_data = {
        'employees': employees_data,
        'total_count': len(employees_data),
        'employees_with_wages': len([e for e in employees_data if e['has_wage']]),
        'employees_without_wages': len(employees_without_wage)
    }
    
    if employees_without_wage:
        response_data['warning'] = f"The following employees don't have wage rates: {', '.join(employees_without_wage)}"
    
    return Response(response_data)


@api_view(['POST'])
def validate_employees_for_attendance(request):
    """Validate employees before marking attendance"""
    serializer = EmployeeAttendanceValidationSerializer(data=request.data)
    
    if serializer.is_valid():
        employee_ids = serializer.validated_data['employee_ids']
        
        # Get employee details with wage information
        employees = Employee.objects.filter(
            id__in=employee_ids, 
            status=True
        ).prefetch_related('wage_set')
        
        valid_employees = []
        invalid_employees = []
        
        for employee in employees:
            current_wage = Wage.get_current_wage(employee)
            employee_data = {
                'employee_id': str(employee.id),
                'employee_name': employee.name,
                'daily_wage': float(current_wage.amount) if current_wage else 0.0,
                'has_wage': current_wage is not None
            }
            
            if current_wage:
                valid_employees.append(employee_data)
            else:
                invalid_employees.append({
                    **employee_data,
                    'issue': 'No current wage rate'
                })
        
        return Response({
            'valid_employees': valid_employees,
            'invalid_employees': invalid_employees,
            'can_mark_attendance': len(invalid_employees) == 0,
            'message': 'All employees are valid for attendance' if len(invalid_employees) == 0 
                      else f'{len(invalid_employees)} employees have issues that need to be resolved'
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def pay_wages(request):
    """Pay wages to employees - handles both bulk and individual payments"""
    try:
        pay_all = request.data.get('pay_all', False)
        week_start = request.data.get('week_start')
        
        if not week_start:
            return Response(
                {'error': 'week_start date is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if pay_all:
            # Pay all employees as bulk payment (single record with employee array)
            return _pay_all_wages_bulk(request, week_start_date)
        else:
            # Pay individual employee (separate individual records)
            return _pay_individual_wage(request, week_start_date)
            
    except Exception as e:
        print(f"Error in pay_wages: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _pay_all_wages_bulk(request, week_start_date):
    """Pay wages to all employees as a single bulk payment record and create expense entry"""
    try:
        # Check if bulk payment already exists for this week
        existing_bulk_payment = BulkWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        if existing_bulk_payment:
            return Response(
                {'error': 'Bulk payment already processed for this week'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        week_dates = get_week_dates(week_start_date)
        week_end_date = week_dates[-1]
        
        # Get all active employees
        employees = Employee.objects.filter(status=True)
        
        # Get attendance records for the week
        attendance_records = AttendanceRecord.objects.filter(
            date__in=week_dates
        )
        
        # Create attendance lookup
        attendance_lookup = {record.date: record.attendance_data for record in attendance_records}
        
        # Prepare employee payment data as array
        employee_payments = []
        total_amount = Decimal('0')
        
        for employee in employees:
            emp_id = str(employee.id)
            current_wage = Wage.get_current_wage(employee)
            daily_wage = current_wage.amount if current_wage else Decimal('0')
            
            if daily_wage == 0:
                continue  # Skip employees without wage rates
            
            # Calculate attendance for this employee
            present_days = 0
            half_days = 0
            absent_days = 0
            late_days = 0
            attendance_details = {}
            
            for week_date in week_dates:
                date_str = week_date.isoformat()
                employee_status = None
                
                if week_date in attendance_lookup:
                    # Find this employee's status
                    for emp_data in attendance_lookup[week_date]:
                        if str(emp_data.get('employee_id')) == emp_id:
                            employee_status = emp_data.get('status')
                            break
                
                attendance_details[date_str] = employee_status
                
                # Count days by status
                if employee_status == 1:  # Present
                    present_days += 1
                elif employee_status == 2:  # Half day
                    half_days += 1
                elif employee_status == 3:  # Late (treat as present)
                    late_days += 1
                    present_days += 1  # Count late as present for wage calculation
                else:  # Absent or no status
                    absent_days += 1
            
            # Calculate total wages
            total_wages = (present_days * daily_wage) + (half_days * daily_wage / 2)
            
            # Store employee data in the format you want
            employee_payment_data = {
                'employee_id': emp_id,
                'employee_name': employee.name,
                'present_days': present_days,
                'half_days': half_days,
                'absent_days': absent_days,
                'late_days': late_days,
                'daily_wage': float(daily_wage),
                'total_wages': float(total_wages),
                'attendance_details': attendance_details,
                'payment_date': timezone.now().isoformat()
            }
            
            employee_payments.append(employee_payment_data)
            total_amount += total_wages
        
        if not employee_payments:
            return Response(
                {'error': 'No employees found with valid wage rates'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get payment details from request
        payment_mode = request.data.get('payment_mode', 'Cash')
        payment_reference = request.data.get('payment_reference', '')
        remarks = request.data.get('remarks', f'Bulk wage payment for week {week_start_date}')
        
        with transaction.atomic():
            # Create bulk payment record - stores employee_payments as a single JSON array
            bulk_payment = BulkWagePayment.create_bulk_payment(
                week_start_date=week_start_date,
                employee_data=employee_payments,  # This is stored as JSON array
                payment_mode=payment_mode,
                payment_reference=payment_reference,
                remarks=remarks,
                paid_by=request.user if request.user.is_authenticated else None
            )
            
            # Create expense record for the bulk payment - FIXED TO MATCH YOUR MODEL
            expense = Expense.objects.create(
                expense_name=f'Bulk Wages - Week {week_start_date}',
                date=timezone.now().date(),
                category='Weekly Wages',  # Using your model's category choice
                description=f'Bulk wage payment for week {week_start_date} to {week_end_date} ({len(employee_payments)} employees)',
                amount=total_amount,
                spent_by=request.user.username if request.user.is_authenticated else 'System',
                mode_of_payment=payment_mode,  # Using your model's field name
                # expense_image_url can be left as default (blank/null)
            )
        
        return Response({
            'message': f'Bulk wage payment processed successfully for {len(employee_payments)} employees',
            'bulk_payment_id': bulk_payment.id,
            'expense_id': expense.id,  # Include expense ID in response
            'total_amount_paid': float(total_amount),
            'total_employees': len(employee_payments),
            'week_start_date': week_start_date.isoformat(),
            'week_end_date': week_end_date.isoformat(),
            'payment_mode': payment_mode,
            'payment_reference': payment_reference,
            'employee_data_storage': 'single_record_with_array',
            'expense_recorded': True,
            'expense_category': 'Weekly Wages'
        })
        
    except Exception as e:
        print(f"Error in _pay_all_wages_bulk: {str(e)}")
        return Response(
            {'error': f'Bulk payment failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _pay_individual_wage(request, week_start_date):
    """Pay wages to individual employee - FIXED VERSION WITHOUT DUPLICATE EXPENSES"""
    try:
        serializer = PayWageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        employee_id = serializer.validated_data['employee_id']
        amount = serializer.validated_data['amount']
        payment_mode = serializer.validated_data['payment_mode']
        payment_reference = serializer.validated_data.get('payment_reference', '')
        remarks = serializer.validated_data.get('remarks', '')
        
        print(f"Processing individual payment: Employee={employee_id}, Amount={amount}")
        
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get or create weekly wage payment (individual record)
        with transaction.atomic():
            try:
                wage_payment = WeeklyWagePayment.objects.get(
                    employee=employee,
                    week_start_date=week_start_date
                )
                print(f"Found existing payment record: Status={wage_payment.payment_status}, Remaining={wage_payment.remaining_amount}")
            except WeeklyWagePayment.DoesNotExist:
                # Only generate payments if none exist for this employee and week
                print(f"No payment record found, generating for employee {employee.name}")
                payments = WeeklyWagePayment.generate_weekly_payments(week_start_date)
                print(f"Generated {len(payments)} payment records for week {week_start_date}")
                
                # Get the payment record that was just created
                wage_payment = WeeklyWagePayment.objects.get(
                    employee=employee,
                    week_start_date=week_start_date
                )
            
            if wage_payment.remaining_amount < amount:
                return Response(
                    {'error': f'Payment amount ({amount}) exceeds remaining balance ({wage_payment.remaining_amount})'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Process the payment - this already handles the payment tracking
            old_status = wage_payment.payment_status
            old_paid = wage_payment.paid_amount
            
            wage_payment.make_payment(
                amount, 
                payment_mode=payment_mode,
                reference=payment_reference,
                remarks=remarks
            )
            
            print(f"Payment processed successfully:")
            print(f"   Status: {old_status} -> {wage_payment.payment_status}")
            print(f"   Paid: {old_paid} -> {wage_payment.paid_amount}")
            print(f"   Remaining: {wage_payment.remaining_amount}")
            
            # REMOVED: No longer creating separate Expense record
            # The WeeklyWagePayment record is sufficient for tracking individual payments
        
        return Response({
            'message': 'Individual payment processed successfully',
            'employee_id': str(employee.id),
            'employee_name': employee.name,
            'amount_paid': float(amount),
            'total_paid': float(wage_payment.paid_amount),
            'remaining_amount': float(wage_payment.remaining_amount),
            'payment_status': wage_payment.payment_status,
            'week_start_date': week_start_date.isoformat(),
            'note': 'Payment tracked in WeeklyWagePayment record only'
        })
        
    except Exception as e:
        print(f"Error in _pay_individual_wage: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Individual payment failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(['GET'])
def weekly_data(request):
    """Get weekly attendance data for all employees"""
    try:
        week_start = request.query_params.get('week_start')
        
        if week_start:
            try:
                week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Default to current week's Monday
            week_start_date = get_monday_of_week(date.today())
        
        week_dates = get_week_dates(week_start_date)
        week_end_date = week_dates[-1]
        
        # Check if bulk payment exists for this week (efficient single record)
        bulk_payment = BulkWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        # Check for individual payments (separate records per employee)
        wage_payments = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        ).select_related('employee')
        
        # Get all active employees
        employees = Employee.objects.filter(status=True)
        
        # Get attendance records for the week
        attendance_records = AttendanceRecord.objects.filter(
            date__in=week_dates
        )
        
        # Create attendance lookup by date
        attendance_lookup = {record.date: record.attendance_data for record in attendance_records}
        
        # Build daily counts
        daily_counts = defaultdict(int)
        for record_date, attendance_data in attendance_lookup.items():
            if attendance_data:  # Check if attendance_data is not None
                present_count = len([emp for emp in attendance_data if emp.get('status') == 1])
                daily_counts[record_date.isoformat()] = present_count
        
        # Build employee data
        employees_data = []
        total_wages = 0
        wages_paid = False
        payment_type = 'none'  # 'bulk', 'individual', or 'none'
        
        # PRIORITY 1: Check for bulk payment first
        if bulk_payment:
            print(f"Using BULK payment data for week {week_start_date}")
            wages_paid = True
            payment_type = 'bulk'
            
            # Create a lookup from bulk payment data
            bulk_payment_lookup = {emp['employee_id']: emp for emp in bulk_payment.employee_payments}
            
            for employee in employees:
                emp_id = str(employee.id)
                current_wage = Wage.get_current_wage(employee)
                daily_wage = current_wage.amount if current_wage else Decimal('0')
                
                # Get data from bulk payment if exists
                bulk_emp_data = bulk_payment_lookup.get(emp_id)
                
                if bulk_emp_data:
                    # Use data from bulk payment
                    employee_attendance = bulk_emp_data.get('attendance_details', {})
                    present_days = bulk_emp_data.get('present_days', 0)
                    half_days = bulk_emp_data.get('half_days', 0)
                    total_wage = Decimal(str(bulk_emp_data.get('total_wages', 0)))
                    payment_status = 'paid'
                    partial_payment = total_wage
                    remaining_amount = Decimal('0')
                else:
                    # Employee not in bulk payment - build from attendance
                    employee_attendance, present_days, half_days, total_wage = _build_employee_attendance_data(
                        emp_id, week_dates, attendance_lookup, daily_wage
                    )
                    payment_status = 'pending'
                    partial_payment = Decimal('0')
                    remaining_amount = total_wage
                
                employees_data.append({
                    'employee_id': emp_id,
                    'employee_name': employee.name,
                    'daily_wage': float(daily_wage),
                    'attendance': employee_attendance,
                    'present_days': present_days,
                    'half_days': half_days,
                    'total_wages': float(total_wage),
                    'payment_status': payment_status,
                    'partial_payment': float(partial_payment),
                    'remaining_amount': float(remaining_amount)
                })
                
                total_wages += float(total_wage)
        
        # PRIORITY 2: Check for individual payments
        elif wage_payments.exists():
            print(f"Using INDIVIDUAL payment data for week {week_start_date}")
            payment_type = 'individual'
            
            # Create payment lookup
            payment_lookup = {wp.employee.id: wp for wp in wage_payments}
            
            # Check if all wages are paid
            wages_paid = all(wp.payment_status == 'paid' for wp in wage_payments)
            
            for employee in employees:
                emp_id = str(employee.id)
                current_wage = Wage.get_current_wage(employee)
                daily_wage = current_wage.amount if current_wage else Decimal('0')
                
                # Get individual payment information
                payment = payment_lookup.get(employee.id)
                
                if payment:
                    # CRITICAL FIX: Use payment record data when available
                    print(f"Found payment record for {employee.name}: Status={payment.payment_status}, Paid={payment.paid_amount}")
                    
                    # Use stored attendance data from payment record if available
                    # If your WeeklyWagePayment model stores attendance, use it
                    # Otherwise, rebuild from attendance records
                    employee_attendance, present_days, half_days, calculated_total_wage = _build_employee_attendance_data(
                        emp_id, week_dates, attendance_lookup, daily_wage
                    )
                    
                    # Use payment record for payment information
                    payment_status = payment.payment_status
                    partial_payment = payment.paid_amount
                    remaining_amount = payment.remaining_amount
                    
                    # Use the higher of calculated or payment record total (in case of discrepancies)
                    total_wage = max(calculated_total_wage, payment.gross_amount)
                    
                else:
                    # No payment record - build from attendance
                    employee_attendance, present_days, half_days, total_wage = _build_employee_attendance_data(
                        emp_id, week_dates, attendance_lookup, daily_wage
                    )
                    
                    payment_status = 'pending'
                    partial_payment = Decimal('0')
                    remaining_amount = total_wage
                
                employees_data.append({
                    'employee_id': emp_id,
                    'employee_name': employee.name,
                    'daily_wage': float(daily_wage),
                    'attendance': employee_attendance,
                    'present_days': present_days,
                    'half_days': half_days,
                    'total_wages': float(total_wage),
                    'payment_status': payment_status,
                    'partial_payment': float(partial_payment),
                    'remaining_amount': float(remaining_amount)
                })
                
                total_wages += float(total_wage)
        
        # PRIORITY 3: No payments exist - build from attendance only
        else:
            print(f"Building from ATTENDANCE data only for week {week_start_date}")
            payment_type = 'none'
            wages_paid = False
            
            for employee in employees:
                emp_id = str(employee.id)
                current_wage = Wage.get_current_wage(employee)
                daily_wage = current_wage.amount if current_wage else Decimal('0')
                
                # Build attendance dictionary for this employee
                employee_attendance, present_days, half_days, total_wage = _build_employee_attendance_data(
                    emp_id, week_dates, attendance_lookup, daily_wage
                )
                
                employees_data.append({
                    'employee_id': emp_id,
                    'employee_name': employee.name,
                    'daily_wage': float(daily_wage),
                    'attendance': employee_attendance,
                    'present_days': present_days,
                    'half_days': half_days,
                    'total_wages': float(total_wage),
                    'payment_status': 'pending',
                    'partial_payment': 0.0,
                    'remaining_amount': float(total_wage)
                })
                
                total_wages += float(total_wage)
        
        response_data = {
            'week_start_date': week_start_date.isoformat(),
            'week_end_date': week_end_date.isoformat(),
            'employees': employees_data,
            'daily_counts': dict(daily_counts),
            'total_wages': total_wages,
            'wages_paid': wages_paid,
            'payment_type': payment_type,
            'weekly_employee_count': len(employees_data)
        }
        
        # Add bulk payment info if exists
        if bulk_payment:
            response_data['bulk_payment_info'] = {
                'id': bulk_payment.id,
                'payment_date': bulk_payment.payment_date.isoformat(),
                'payment_mode': bulk_payment.payment_mode,
                'payment_reference': bulk_payment.payment_reference,
                'total_amount': float(bulk_payment.total_amount),
                'employees_in_single_record': len(bulk_payment.employee_payments)
            }
        
        print(f"Weekly data response built successfully: {len(employees_data)} employees, payment_type={payment_type}")
        return Response(response_data)
        
    except Exception as e:
        print(f"Error in weekly_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Failed to fetch weekly data: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
def _build_employee_attendance_data(emp_id, week_dates, attendance_lookup, daily_wage):
    """Helper function to build employee attendance data from attendance records"""
    employee_attendance = {}
    present_days = 0
    half_days = 0
    late_days = 0
    
    for week_date in week_dates:
        date_str = week_date.isoformat()
        employee_status = None
        
        if week_date in attendance_lookup and attendance_lookup[week_date]:
            # Find this employee's status in the attendance data
            for emp_data in attendance_lookup[week_date]:
                if str(emp_data.get('employee_id')) == emp_id:
                    employee_status = emp_data.get('status')
                    break
        
        employee_attendance[date_str] = employee_status
        
        # Count days by status
        if employee_status == 1:  # Present
            present_days += 1
        elif employee_status == 2:  # Half day
            half_days += 1
        elif employee_status == 3:  # Late (treat as present)
            late_days += 1
            present_days += 1  # Count late as present for wage calculation
    
    # Calculate total wage
    total_wage = (present_days * daily_wage) + (half_days * daily_wage / 2)
    
    return employee_attendance, present_days, half_days, total_wage

@api_view(['GET'])
def bulk_payment_history(request):
    """Get bulk payment history"""
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    
    queryset = BulkWagePayment.objects.all()
    
    if from_date:
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            queryset = queryset.filter(week_start_date__gte=from_date)
        except ValueError:
            return Response({'error': 'Invalid from_date format'}, status=400)
    
    if to_date:
        try:
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            queryset = queryset.filter(week_start_date__lte=to_date)
        except ValueError:
            return Response({'error': 'Invalid to_date format'}, status=400)
    
    bulk_payments = queryset.order_by('-payment_date')
    
    payment_history = []
    for payment in bulk_payments:
        payment_history.append({
            'id': payment.id,
            'week_start_date': payment.week_start_date.isoformat(),
            'week_end_date': payment.week_end_date.isoformat(),
            'payment_date': payment.payment_date.isoformat(),
            'total_employees': payment.total_employees,
            'total_amount': float(payment.total_amount),
            'payment_mode': payment.payment_mode,
            'payment_reference': payment.payment_reference,
            'remarks': payment.remarks,
            'paid_by': payment.paid_by.username if payment.paid_by else None
        })
    
    return Response({
        'bulk_payments': payment_history,
        'total_records': len(payment_history)
    })


@api_view(['GET'])
def bulk_payment_details(request, payment_id):
    """Get detailed view of a specific bulk payment"""
    try:
        bulk_payment = BulkWagePayment.objects.get(id=payment_id)
    except BulkWagePayment.DoesNotExist:
        return Response({'error': 'Bulk payment not found'}, status=404)
    
    return Response({
        'id': bulk_payment.id,
        'week_start_date': bulk_payment.week_start_date.isoformat(),
        'week_end_date': bulk_payment.week_end_date.isoformat(),
        'payment_date': bulk_payment.payment_date.isoformat(),
        'total_employees': bulk_payment.total_employees,
        'total_amount': float(bulk_payment.total_amount),
        'payment_mode': bulk_payment.payment_mode,
        'payment_reference': bulk_payment.payment_reference,
        'remarks': bulk_payment.remarks,
        'paid_by': bulk_payment.paid_by.username if bulk_payment.paid_by else None,
        'employee_payments': bulk_payment.employee_payments  # Full employee payment details
    })


@api_view(['GET'])
def export_attendance(request):
    """Export attendance data for a date range"""
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    
    if not from_date or not to_date:
        return Response(
            {'error': 'from_date and to_date are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get attendance data for the date range
    attendance_records = AttendanceRecord.objects.filter(
        date__range=[from_date, to_date]
    )
    
    export_data = []
    for record in attendance_records:
        for emp_data in record.attendance_data:
            status_map = {0: 'Absent', 1: 'Present', 2: 'Half Day', 3: 'Late'}
            export_data.append({
                'date': record.date.isoformat(),
                'employee_id': emp_data.get('employee_id'),
                'employee_name': emp_data.get('employee_name'),
                'status': status_map.get(emp_data.get('status'), 'Unknown'),
                'wage_amount': emp_data.get('wage_amount', 0)
            })
    
    return Response({
        'data': export_data,
        'from_date': from_date.isoformat(),
        'to_date': to_date.isoformat(),
        'total_records': len(export_data)
    })


@api_view(['GET'])
def wage_summary(request):
    """Get wage summary for a specific week"""
    week_start = request.query_params.get('week_start')
    
    if not week_start:
        return Response(
            {'error': 'week_start date is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get weekly wage payments
    wage_payments = WeeklyWagePayment.objects.filter(
        week_start_date=week_start_date
    ).select_related('employee')
    
    payments_data = []
    for payment in wage_payments:
        payments_data.append({
            'employee_id': str(payment.employee.id),
            'employee_name': payment.employee_name,
            'present_days': payment.total_present_days,
            'half_days': payment.total_half_days,
            'daily_wage': float(payment.daily_wage_amount),
            'gross_amount': float(payment.gross_amount),
            'net_amount': float(payment.net_amount),
            'paid_amount': float(payment.paid_amount),
            'remaining_amount': float(payment.remaining_amount),
            'payment_status': payment.payment_status
        })
    
    summary = {
        'week_start_date': week_start_date.isoformat(),
        'total_employees': wage_payments.count(),
        'total_gross_wages': float(wage_payments.aggregate(Sum('gross_amount'))['gross_amount__sum'] or 0),
        'total_paid_amount': float(wage_payments.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0),
        'total_remaining_amount': float(wage_payments.aggregate(Sum('remaining_amount'))['remaining_amount__sum'] or 0),
        'fully_paid_count': wage_payments.filter(payment_status='paid').count(),
        'partially_paid_count': wage_payments.filter(payment_status='partial').count(),
        'pending_count': wage_payments.filter(payment_status='pending').count(),
        'payments': payments_data
    }
    
    return Response(summary)