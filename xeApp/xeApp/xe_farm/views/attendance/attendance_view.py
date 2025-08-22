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
    
    # FIXED: Check if wages are already paid for this week
    # Remove invalid employee filter and check JSON data instead
    week_start = get_monday_of_week(attendance_date)
    wage_records = WeeklyWagePayment.objects.filter(
        week_start_date=week_start,
        payment_status='paid'
    )
    
    # Check if this specific employee is already fully paid
    employee_wages_paid = False
    for record in wage_records:
        for emp_wage in record.employee_wages:
            if (emp_wage.get('employee_id') == str(employee_id) and 
                emp_wage.get('payment_status') == 'paid'):
                employee_wages_paid = True
                break
        if employee_wages_paid:
            break
    
    if employee_wages_paid:
        return Response(
            {'error': 'Cannot update attendance. Wages already paid for this employee for this week.'}, 
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
    """Pay wages to employees - handles both bulk and individual payments with optimized structure"""
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
            return _pay_all_wages(request, week_start_date)
        else:
            return _pay_individual_wage(request, week_start_date)
            
    except Exception as e:
        print(f"Error in pay_wages: {str(e)}")
        return Response(
            {'error': f'Internal server error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _pay_all_wages(request, week_start_date):
    """Pay all wages using optimized WeeklyWagePayment structure"""
    try:
        # Check if wage record already exists
        existing_wage_record = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        if existing_wage_record and existing_wage_record.payment_status == 'paid':
            return Response(
                {'error': 'Wages already fully paid for this week'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate or get existing wage record
        if not existing_wage_record:
            wage_record = WeeklyWagePayment.generate_weekly_wage_record(week_start_date)
        else:
            wage_record = existing_wage_record
        
        # Get payment details from request
        payment_mode = request.data.get('payment_mode', 'Cash')
        payment_reference = request.data.get('payment_reference', '')
        remarks = request.data.get('remarks', f'Bulk wage payment for week {week_start_date}')
        
        with transaction.atomic():
            # Pay all pending wages
            total_payment = wage_record.make_bulk_payment(
                payment_mode=payment_mode,
                reference=payment_reference,
                remarks=remarks
            )
            
            if total_payment == 0:
                return Response(
                    {'error': 'No pending payments found'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response({
            'message': f'Bulk wage payment processed successfully for {wage_record.total_employees} employees',
            'wage_record_id': wage_record.id,
            'expense_id': wage_record.expense_entry.id if wage_record.expense_entry else None,
            'total_amount_paid': float(total_payment),
            'total_employees': wage_record.total_employees,
            'week_start_date': wage_record.week_start_date.isoformat(),
            'week_end_date': wage_record.week_end_date.isoformat(),
            'payment_mode': payment_mode,
            'payment_reference': payment_reference,
            'data_structure': 'optimized_single_record_with_json_array',
            'expense_recorded': wage_record.expense_entry is not None
        })
        
    except Exception as e:
        print(f"Error in _pay_all_wages: {str(e)}")
        return Response(
            {'error': f'Bulk payment failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _pay_individual_wage(request, week_start_date):
    """Pay individual employee wage with comprehensive debugging"""
    try:
        serializer = PayWageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        employee_id = str(serializer.validated_data['employee_id'])
        amount = Decimal(str(serializer.validated_data['amount']))
        payment_mode = serializer.validated_data['payment_mode']
        payment_reference = serializer.validated_data.get('payment_reference', '')
        remarks = serializer.validated_data.get('remarks', '')
        
        print(f"=== PAYMENT DEBUG START ===")
        print(f"Employee ID: {employee_id}")
        print(f"Amount: {amount}")
        print(f"Week Start Date: {week_start_date}")
        
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check existing payments
        existing_wage_records = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date,
            payment_status='paid'
        )
        
        employee_already_paid = False
        for record in existing_wage_records:
            for emp_wage in record.employee_wages:
                if emp_wage.get('employee_id') == employee_id and emp_wage.get('payment_status') == 'paid':
                    employee_already_paid = True
                    break
            if employee_already_paid:
                break
        
        if employee_already_paid:
            return Response(
                {'error': f'Wages already fully paid for employee {employee.name} for this week.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create wage record BEFORE transaction
        wage_record = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        if not wage_record:
            print("Creating new wage record...")
            wage_record = WeeklyWagePayment.generate_weekly_wage_record(week_start_date)
            print(f"New wage record created: ID = {wage_record.id}")
        else:
            print(f"Using existing wage record: ID = {wage_record.id}")
        
        # Print BEFORE state
        emp_data_before = wage_record.get_employee_wage_data(employee_id)
        print(f"BEFORE UPDATE - Employee data: {emp_data_before}")
        
        with transaction.atomic():
            print("=== STARTING ATOMIC TRANSACTION ===")
            
            try:
                # Call the update method
                print("Calling update_employee_payment...")
                wage_record.update_employee_payment(
                    employee_id=employee_id,
                    payment_amount=amount,
                    payment_mode=payment_mode,
                    reference=payment_reference,
                    remarks=remarks
                )
                print("update_employee_payment completed successfully")
                
                # Force a database refresh to ensure we get the latest data
                wage_record.refresh_from_db()
                print("Record refreshed from database")
                
            except ValueError as e:
                print(f"ValueError in update_employee_payment: {str(e)}")
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                print(f"Unexpected error in payment update: {str(e)}")
                import traceback
                traceback.print_exc()
                raise
            
        print("=== TRANSACTION COMMITTED ===")
        
        # CRITICAL: Verify the data was actually saved by fetching fresh from DB
        print("=== VERIFYING DATABASE STATE ===")
        fresh_record = WeeklyWagePayment.objects.get(id=wage_record.id)
        emp_data_after = fresh_record.get_employee_wage_data(employee_id)
        print(f"AFTER UPDATE - Fresh from DB: {emp_data_after}")
        
        # Additional verification - check if the JSON field was actually updated
        print(f"Record total_paid_amount: {fresh_record.total_paid_amount}")
        print(f"Record payment_status: {fresh_record.payment_status}")
        
        # Double-check by counting paid employees
        paid_employees = [e for e in fresh_record.employee_wages if e.get('payment_status') in ['paid', 'partial']]
        print(f"Employees with payments: {len(paid_employees)}")
        
        # Create transaction record (simplified)
        try:
            print("Creating transaction record...")
            from ...models import WagePaymentTransaction
            
            # Create with minimal required fields
            transaction_record = WagePaymentTransaction.objects.create(
                wage_payment=fresh_record,
                transaction_type='payment',
                amount=amount,
                payment_mode=payment_mode,
                remarks=f'Payment to {employee.name}' + (f': {remarks}' if remarks else ''),
            )
            print(f"Transaction record created successfully: ID = {transaction_record.id}")
            
        except Exception as transaction_error:
            print(f"Transaction record creation failed (non-critical): {transaction_error}")
            # Don't fail the payment
            pass
        
        # Prepare response with fresh data
        response_data = {
            'success': True,
            'message': 'Individual payment processed successfully',
            'employee_id': employee_id,
            'employee_name': employee.name,
            'amount_paid': float(amount),
            'total_paid': emp_data_after.get('paid_amount', 0) if emp_data_after else 0,
            'remaining_amount': emp_data_after.get('remaining_amount', 0) if emp_data_after else 0,
            'payment_status': emp_data_after.get('payment_status', 'pending') if emp_data_after else 'pending',
            'week_start_date': week_start_date.isoformat(),
            'wage_record_id': fresh_record.id,
            # Add debugging info
            'debug_info': {
                'before_paid_amount': emp_data_before.get('paid_amount', 0) if emp_data_before else 0,
                'after_paid_amount': emp_data_after.get('paid_amount', 0) if emp_data_after else 0,
                'record_total_paid': float(fresh_record.total_paid_amount),
                'data_updated': emp_data_before != emp_data_after if emp_data_before and emp_data_after else False
            }
        }
        
        print(f"Final response data: {response_data}")
        print("=== PAYMENT DEBUG END ===")
        
        return Response(response_data)
        
    except Exception as e:
        print(f"CRITICAL ERROR in _pay_individual_wage: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'success': False, 'error': f'Individual payment failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Create a separate API endpoint to verify payment data
@api_view(['GET'])
def verify_payment_data(request):
    """Debug endpoint to verify payment data in database"""
    week_start = request.GET.get('week_start')
    employee_id = request.GET.get('employee_id')
    
    if not week_start:
        return Response({'error': 'week_start parameter required'})
    
    try:
        week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
        
        wage_record = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        if not wage_record:
            return Response({'error': 'No wage record found for this week'})
        
        response_data = {
            'wage_record_id': wage_record.id,
            'total_employees': wage_record.total_employees,
            'total_paid_amount': float(wage_record.total_paid_amount),
            'payment_status': wage_record.payment_status,
            'employee_count': len(wage_record.employee_wages) if wage_record.employee_wages else 0,
        }
        
        if employee_id:
            emp_data = wage_record.get_employee_wage_data(employee_id)
            response_data['employee_data'] = emp_data
        else:
            # Return all employee payment statuses
            response_data['all_employees'] = [
                {
                    'employee_id': e.get('employee_id'),
                    'employee_name': e.get('employee_name'),
                    'paid_amount': e.get('paid_amount', 0),
                    'payment_status': e.get('payment_status', 'pending')
                } for e in wage_record.employee_wages
            ]
        
        return Response(response_data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def weekly_data(request):
    """Get weekly attendance data using optimized structure"""
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
            week_start_date = get_monday_of_week(date.today())
        
        week_dates = get_week_dates(week_start_date)
        week_end_date = week_dates[-1]
        
        # Check for optimized wage payment record
        wage_record = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        # Check for old bulk payment (for backward compatibility)
        bulk_payment = BulkWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
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
            if attendance_data:
                present_count = len([emp for emp in attendance_data if emp.get('status') == 1])
                daily_counts[record_date.isoformat()] = present_count
        
        # Build employee data
        employees_data = []
        total_wages = 0
        wages_paid = False
        payment_type = 'none'
        
        # PRIORITY 1: Use optimized WeeklyWagePayment record
        if wage_record:
            print(f"Using OPTIMIZED wage record for week {week_start_date}")
            wages_paid = wage_record.payment_status in ['Fully Paid', 'Partial']
            payment_type = 'optimized'
            
            # Create employee lookup from wage record
            wage_employee_lookup = {emp['employee_id']: emp for emp in wage_record.employee_wages}
            
            for employee in employees:
                emp_id = str(employee.id)
                current_wage = Wage.get_current_wage(employee)
                daily_wage = current_wage.amount if current_wage else Decimal('0')
                
                # Get data from wage record if exists
                wage_emp_data = wage_employee_lookup.get(emp_id)
                
                if wage_emp_data:
                    # Use data from wage record
                    employee_attendance = wage_emp_data.get('attendance_details', {})
                    present_days = wage_emp_data.get('present_days', 0)
                    half_days = wage_emp_data.get('half_days', 0)
                    total_wage = Decimal(str(wage_emp_data.get('net_amount', 0)))
                    payment_status = wage_emp_data.get('payment_status', 'pending')
                    partial_payment = Decimal(str(wage_emp_data.get('paid_amount', 0)))
                    remaining_amount = Decimal(str(wage_emp_data.get('remaining_amount', 0)))
                else:
                    # Employee not in wage record - build from attendance
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
        
        # PRIORITY 2: Check for old bulk payment (backward compatibility)
        elif bulk_payment:
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
        
        # Add optimized wage record info if exists
        if wage_record:
            response_data['wage_record_info'] = {
                'id': wage_record.id,
                'payment_status': wage_record.payment_status,
                'total_employees': wage_record.total_employees,
                'total_net_amount': float(wage_record.total_net_amount),
                'total_paid_amount': float(wage_record.total_paid_amount),
                'total_remaining_amount': float(wage_record.total_remaining_amount),
                'expense_entry_id': wage_record.expense_entry.id if wage_record.expense_entry else None,
                'data_structure': 'optimized_json_array'
            }
        
        # Add bulk payment info if exists (for backward compatibility)
        elif bulk_payment:
            response_data['bulk_payment_info'] = {
                'id': bulk_payment.id,
                'payment_date': bulk_payment.payment_date.isoformat(),
                'payment_mode': bulk_payment.payment_mode,
                'payment_reference': bulk_payment.payment_reference,
                'total_amount': float(bulk_payment.total_amount),
                'employees_in_single_record': len(bulk_payment.employee_payments),
                'data_structure': 'legacy_bulk_payment'
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
def wage_payment_history(request):
    """Get optimized wage payment history"""
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    
    queryset = WeeklyWagePayment.objects.all()
    
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
    
    wage_records = queryset.order_by('-week_start_date')
    
    payment_history = []
    for record in wage_records:
        payment_history.append({
            'id': record.id,
            'week_start_date': record.week_start_date.isoformat(),
            'week_end_date': record.week_end_date.isoformat(),
            'total_employees': record.total_employees,
            'total_gross_amount': float(record.total_gross_amount),
            'total_net_amount': float(record.total_net_amount),
            'total_paid_amount': float(record.total_paid_amount),
            'total_remaining_amount': float(record.total_remaining_amount),
            'payment_status': record.payment_status,
            'expense_entry_id': record.expense_entry.id if record.expense_entry else None,
            'created_at': record.created_at.isoformat(),
            'updated_at': record.updated_at.isoformat(),
            'data_structure': 'optimized_json_array'
        })
    
    return Response({
        'wage_payment_records': payment_history,
        'total_records': len(payment_history)
    })



@api_view(['GET'])
def wage_payment_details(request, record_id):
    """Get detailed view of a specific optimized wage payment record"""
    try:
        wage_record = WeeklyWagePayment.objects.get(id=record_id)
    except WeeklyWagePayment.DoesNotExist:
        return Response({'error': 'Wage payment record not found'}, status=404)
    
    # Get payment transactions for audit trail
    transactions = wage_record.payment_transactions.all().order_by('-transaction_date')
    transaction_data = []
    for transaction in transactions:
        transaction_data.append({
            'id': transaction.id,
            'employee_id': transaction.employee_id,
            'employee_name': transaction.employee_name,
            'transaction_type': transaction.transaction_type,
            'amount': float(transaction.amount),
            'payment_mode': transaction.payment_mode,
            'reference_number': transaction.reference_number,
            'transaction_date': transaction.transaction_date.isoformat(),
            'remarks': transaction.remarks
        })
    
    return Response({
        'id': wage_record.id,
        'week_start_date': wage_record.week_start_date.isoformat(),
        'week_end_date': wage_record.week_end_date.isoformat(),
        'total_employees': wage_record.total_employees,
        'total_gross_amount': float(wage_record.total_gross_amount),
        'total_net_amount': float(wage_record.total_net_amount),
        'total_paid_amount': float(wage_record.total_paid_amount),
        'total_remaining_amount': float(wage_record.total_remaining_amount),
        'payment_status': wage_record.payment_status,
        'expense_entry_id': wage_record.expense_entry.id if wage_record.expense_entry else None,
        'employee_wages': wage_record.employee_wages,  # Full employee wage details
        'payment_transactions': transaction_data,  # Audit trail
        'payment_summary': wage_record.get_payment_summary(),
        'data_structure': 'optimized_json_array',
        'created_at': wage_record.created_at.isoformat(),
        'updated_at': wage_record.updated_at.isoformat()
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
    """Get wage summary using optimized structure"""
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
    
    # Get optimized wage record
    wage_record = WeeklyWagePayment.objects.filter(
        week_start_date=week_start_date
    ).first()
    
    if not wage_record:
        return Response(
            {'error': 'No wage record found for this week'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Build detailed employee summary from JSON array
    employees_summary = []
    for emp_data in wage_record.employee_wages:
        employees_summary.append({
            'employee_id': emp_data.get('employee_id'),
            'employee_name': emp_data.get('employee_name'),
            'present_days': emp_data.get('present_days', 0),
            'half_days': emp_data.get('half_days', 0),
            'daily_wage': emp_data.get('daily_wage', 0),
            'gross_amount': emp_data.get('gross_amount', 0),
            'net_amount': emp_data.get('net_amount', 0),
            'paid_amount': emp_data.get('paid_amount', 0),
            'remaining_amount': emp_data.get('remaining_amount', 0),
            'payment_status': emp_data.get('payment_status', 'pending')
        })
    
    summary = {
        'week_start_date': wage_record.week_start_date.isoformat(),
        'week_end_date': wage_record.week_end_date.isoformat(),
        'total_employees': wage_record.total_employees,
        'total_gross_wages': float(wage_record.total_gross_amount),
        'total_net_wages': float(wage_record.total_net_amount),
        'total_paid_amount': float(wage_record.total_paid_amount),
        'total_remaining_amount': float(wage_record.total_remaining_amount),
        'payment_status': wage_record.payment_status,
        'fully_paid_count': len([e for e in wage_record.employee_wages if e.get('payment_status') == 'paid']),
        'partially_paid_count': len([e for e in wage_record.employee_wages if e.get('payment_status') == 'partial']),
        'pending_count': len([e for e in wage_record.employee_wages if e.get('payment_status') == 'pending']),
        'employees': employees_summary,
        'data_structure': 'optimized_json_array'
    }
    
    return Response(summary)

def _is_employee_fully_paid(employee_id, week_start_date):
    """
    Helper function to check if an employee is fully paid for a given week
    by examining the JSON data in WeeklyWagePayment records
    """
    wage_records = WeeklyWagePayment.objects.filter(
        week_start_date=week_start_date
    )
    
    for record in wage_records:
        for emp_wage in record.employee_wages:
            if (emp_wage.get('employee_id') == str(employee_id) and 
                emp_wage.get('payment_status') == 'paid'):
                return True
    
    return False

@api_view(['POST'])
def generate_wage_record(request):
    """Generate wage record for a specific week if it doesn't exist"""
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
    
    try:
        # Generate wage record (will return existing one if already exists)
        wage_record = WeeklyWagePayment.generate_weekly_wage_record(week_start_date)
        
        return Response({
            'message': 'Wage record generated successfully',
            'wage_record_id': wage_record.id,
            'week_start_date': wage_record.week_start_date.isoformat(),
            'week_end_date': wage_record.week_end_date.isoformat(),
            'total_employees': wage_record.total_employees,
            'total_net_amount': float(wage_record.total_net_amount),
            'payment_status': wage_record.payment_status,
            'data_structure': 'optimized_json_array'
        })
        
    except Exception as e:
        print(f"Error generating wage record: {str(e)}")
        return Response(
            {'error': f'Failed to generate wage record: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    
