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

@api_view(['GET'])
def employee_report(request):
    """
    Get comprehensive employee attendance and wages report for last 28 days
    Includes individual employee details, weekly breakdowns, and overall summary
    """
    try:
        # Get date range - last 28 days
        end_date = date.today()
        start_date = end_date - timedelta(days=27)  # 28 days including today
        
        # Allow custom date range via query parameters
        custom_start = request.query_params.get('start_date')
        custom_end = request.query_params.get('end_date')
        
        if custom_start:
            try:
                start_date = datetime.strptime(custom_start, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid start_date format. Use YYYY-MM-DD'}, status=400)
        
        if custom_end:
            try:
                end_date = datetime.strptime(custom_end, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid end_date format. Use YYYY-MM-DD'}, status=400)
        
        # Get all active employees
        employees = Employee.objects.filter(status=True).order_by('name')
        
        # Get attendance records for the date range
        attendance_records = AttendanceRecord.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        # Create attendance lookup by date
        attendance_lookup = {}
        for record in attendance_records:
            attendance_lookup[record.date] = {
                emp['employee_id']: emp for emp in record.attendance_data
            }
        
        # Get all weeks in the date range
        weeks_data = []
        current_date = start_date
        while current_date <= end_date:
            week_start = get_monday_of_week(current_date)
            if week_start not in [w['week_start'] for w in weeks_data]:
                weeks_data.append({
                    'week_start': week_start,
                    'week_end': week_start + timedelta(days=6)
                })
            current_date += timedelta(days=7)
        
        # Get wage payment records for all weeks
        wage_records = {}
        for week in weeks_data:
            wage_record = WeeklyWagePayment.objects.filter(
                week_start_date=week['week_start']
            ).first()
            if wage_record:
                wage_records[week['week_start']] = wage_record
        
        # Build employee reports
        employees_report = []
        overall_stats = {
            'total_employees': len(employees),
            'total_working_days': 0,
            'total_present_days': 0,
            'total_half_days': 0,
            'total_absent_days': 0,
            'total_wages_earned': 0,
            'total_wages_paid': 0,
            'total_wages_pending': 0
        }
        
        for employee in employees:
            emp_id = str(employee.id)
            current_wage = Wage.get_current_wage(employee)
            daily_wage = current_wage.amount if current_wage else Decimal('0')
            
            # Employee daily attendance and wages
            daily_data = []
            emp_present_days = 0
            emp_half_days = 0
            emp_absent_days = 0
            emp_total_wages = Decimal('0')
            
            # Process each day in the date range
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.isoformat()
                
                # Get attendance status for this employee on this date
                attendance_status = None
                wage_earned = Decimal('0')
                
                if current_date in attendance_lookup and emp_id in attendance_lookup[current_date]:
                    emp_attendance = attendance_lookup[current_date][emp_id]
                    attendance_status = emp_attendance.get('status')
                    
                    # Calculate wage for this day
                    if attendance_status == 1:  # Present
                        wage_earned = daily_wage
                        emp_present_days += 1
                    elif attendance_status == 2:  # Half day
                        wage_earned = daily_wage / 2
                        emp_half_days += 1
                    elif attendance_status == 3:  # Late (treat as present)
                        wage_earned = daily_wage
                        emp_present_days += 1
                    elif attendance_status == 0:  # Absent
                        emp_absent_days += 1
                else:
                    # No attendance record for this date - consider as absent
                    emp_absent_days += 1
                
                emp_total_wages += wage_earned
                
                # Map status to readable format
                status_map = {0: 'Absent', 1: 'Present', 2: 'Half Day', 3: 'Late', None: 'No Record'}
                
                daily_data.append({
                    'date': date_str,
                    'day_name': current_date.strftime('%A'),
                    'status': status_map.get(attendance_status),
                    'status_code': attendance_status,
                    'wage_earned': float(wage_earned)
                })
                
                current_date += timedelta(days=1)
            
            # Weekly breakdown for this employee
            weekly_breakdown = []
            emp_total_paid = Decimal('0')
            emp_total_pending = Decimal('0')
            
            for week in weeks_data:
                week_start = week['week_start']
                week_end = week['week_end']
                
                # Filter daily data for this week
                week_daily_data = [
                    day for day in daily_data 
                    if week_start <= datetime.strptime(day['date'], '%Y-%m-%d').date() <= week_end
                ]
                
                # Calculate week totals
                week_present = len([d for d in week_daily_data if d['status_code'] in [1, 3]])
                week_half_days = len([d for d in week_daily_data if d['status_code'] == 2])
                week_absent = len([d for d in week_daily_data if d['status_code'] in [0, None]])
                week_wages = sum(Decimal(str(d['wage_earned'])) for d in week_daily_data)
                
                # Get payment info from wage record
                week_paid_amount = Decimal('0')
                week_payment_status = 'pending'
                
                if week_start in wage_records:
                    wage_record = wage_records[week_start]
                    emp_wage_data = wage_record.get_employee_wage_data(emp_id)
                    if emp_wage_data:
                        week_paid_amount = Decimal(str(emp_wage_data.get('paid_amount', 0)))
                        week_payment_status = emp_wage_data.get('payment_status', 'pending')
                
                emp_total_paid += week_paid_amount
                week_pending = week_wages - week_paid_amount
                emp_total_pending += week_pending
                
                weekly_breakdown.append({
                    'week_start': week_start.isoformat(),
                    'week_end': week_end.isoformat(),
                    'present_days': week_present,
                    'half_days': week_half_days,
                    'absent_days': week_absent,
                    'total_wages_earned': float(week_wages),
                    'wages_paid': float(week_paid_amount),
                    'wages_pending': float(week_pending),
                    'payment_status': week_payment_status,
                    'daily_details': week_daily_data
                })
            
            # Add to overall stats
            total_working_days = emp_present_days + emp_half_days + emp_absent_days
            overall_stats['total_working_days'] += total_working_days
            overall_stats['total_present_days'] += emp_present_days
            overall_stats['total_half_days'] += emp_half_days
            overall_stats['total_absent_days'] += emp_absent_days
            overall_stats['total_wages_earned'] += float(emp_total_wages)
            overall_stats['total_wages_paid'] += float(emp_total_paid)
            overall_stats['total_wages_pending'] += float(emp_total_pending)
            
            # Build employee report
            employees_report.append({
                'employee_id': emp_id,
                'employee_name': employee.name,
                'daily_wage': float(daily_wage),
                'period_summary': {
                    'total_days': total_working_days,
                    'present_days': emp_present_days,
                    'half_days': emp_half_days,
                    'absent_days': emp_absent_days,
                    'attendance_percentage': round((emp_present_days + emp_half_days * 0.5) / max(total_working_days, 1) * 100, 2),
                    'total_wages_earned': float(emp_total_wages),
                    'total_wages_paid': float(emp_total_paid),
                    'total_wages_pending': float(emp_total_pending),
                    'payment_percentage': round(float(emp_total_paid) / max(float(emp_total_wages), 1) * 100, 2)
                },
                'weekly_breakdown': weekly_breakdown,
                'daily_attendance': daily_data
            })
        
        # Calculate overall percentages
        if overall_stats['total_working_days'] > 0:
            overall_stats['overall_attendance_percentage'] = round(
                (overall_stats['total_present_days'] + overall_stats['total_half_days'] * 0.5) / 
                overall_stats['total_working_days'] * 100, 2
            )
        else:
            overall_stats['overall_attendance_percentage'] = 0
        
        if overall_stats['total_wages_earned'] > 0:
            overall_stats['overall_payment_percentage'] = round(
                overall_stats['total_wages_paid'] / overall_stats['total_wages_earned'] * 100, 2
            )
        else:
            overall_stats['overall_payment_percentage'] = 0
        
        # Weekly summary across all employees
        weekly_summary = []
        for week in weeks_data:
            week_start = week['week_start']
            week_employees_data = []
            week_totals = {
                'total_employees': len(employees),
                'total_present_days': 0,
                'total_half_days': 0,
                'total_wages_earned': 0,
                'total_wages_paid': 0,
                'employees_fully_paid': 0,
                'employees_partially_paid': 0,
                'employees_unpaid': 0
            }
            
            # Get wage record for this week
            wage_record = wage_records.get(week_start)
            
            for employee in employees:
                emp_id = str(employee.id)
                
                # Find this employee's data for this week from the individual reports
                emp_week_data = None
                for emp_report in employees_report:
                    if emp_report['employee_id'] == emp_id:
                        for week_data in emp_report['weekly_breakdown']:
                            if week_data['week_start'] == week_start.isoformat():
                                emp_week_data = week_data
                                break
                        break
                
                if emp_week_data:
                    week_totals['total_present_days'] += emp_week_data['present_days']
                    week_totals['total_half_days'] += emp_week_data['half_days']
                    week_totals['total_wages_earned'] += emp_week_data['total_wages_earned']
                    week_totals['total_wages_paid'] += emp_week_data['wages_paid']
                    
                    # Count payment statuses
                    if emp_week_data['payment_status'] == 'paid':
                        week_totals['employees_fully_paid'] += 1
                    elif emp_week_data['payment_status'] == 'partial':
                        week_totals['employees_partially_paid'] += 1
                    else:
                        week_totals['employees_unpaid'] += 1
            
            weekly_summary.append({
                'week_start': week_start.isoformat(),
                'week_end': week['week_end'].isoformat(),
                'week_totals': week_totals,
                'wage_record_id': wage_record.id if wage_record else None,
                'wage_record_status': wage_record.payment_status if wage_record else 'No Record'
            })
        
        return Response({
            'report_period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'total_days': (end_date - start_date).days + 1,
                'total_weeks': len(weeks_data)
            },
            'overall_summary': overall_stats,
            'weekly_summary': weekly_summary,
            'employees_detailed_report': employees_report,
            'report_generated_at': timezone.now().isoformat(),
            'data_structure': 'comprehensive_employee_report'
        })
        
    except Exception as e:
        print(f"Error generating employee report: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Failed to generate employee report: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def single_employee_report(request, employee_id):
    """
    Get comprehensive employee attendance and wages report for a specific employee
    URL: /api/employee/{employee_id}/report/
    """
    try:
        # Validate employee exists
        try:
            employee = Employee.objects.get(id=employee_id, status=True)
        except Employee.DoesNotExist:
            return Response(
                {'error': f'Employee with ID {employee_id} not found or inactive'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get date range - last 28 days by default
        end_date = date.today()
        start_date = end_date - timedelta(days=27)  # 28 days including today
        
        # Allow custom date range via query parameters
        custom_start = request.query_params.get('start_date')
        custom_end = request.query_params.get('end_date')
        
        if custom_start:
            try:
                start_date = datetime.strptime(custom_start, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid start_date format. Use YYYY-MM-DD'}, status=400)
        
        if custom_end:
            try:
                end_date = datetime.strptime(custom_end, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid end_date format. Use YYYY-MM-DD'}, status=400)
        
        # Validate date range
        if start_date > end_date:
            return Response({'error': 'Start date cannot be after end date'}, status=400)
        
        emp_id = str(employee.id)
        current_wage = Wage.get_current_wage(employee)
        daily_wage = current_wage.amount if current_wage else Decimal('0')
        
        # Get attendance records for the date range
        attendance_records = AttendanceRecord.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        # Create attendance lookup by date
        attendance_lookup = {}
        for record in attendance_records:
            attendance_lookup[record.date] = {
                emp['employee_id']: emp for emp in record.attendance_data
            }
        
        # Get all weeks in the date range
        weeks_data = []
        current_date = start_date
        while current_date <= end_date:
            week_start = get_monday_of_week(current_date)
            if week_start not in [w['week_start'] for w in weeks_data]:
                weeks_data.append({
                    'week_start': week_start,
                    'week_end': week_start + timedelta(days=6)
                })
            current_date += timedelta(days=7)
        
        # Get wage payment records for all weeks
        wage_records = {}
        for week in weeks_data:
            wage_record = WeeklyWagePayment.objects.filter(
                week_start_date=week['week_start']
            ).first()
            if wage_record:
                wage_records[week['week_start']] = wage_record
        
        # Employee daily attendance and wages
        daily_data = []
        emp_present_days = 0
        emp_half_days = 0
        emp_absent_days = 0
        emp_total_wages = Decimal('0')
        
        # Process each day in the date range
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.isoformat()
            
            # Get attendance status for this employee on this date
            attendance_status = None
            wage_earned = Decimal('0')
            
            if current_date in attendance_lookup and emp_id in attendance_lookup[current_date]:
                emp_attendance = attendance_lookup[current_date][emp_id]
                attendance_status = emp_attendance.get('status')
                
                # Calculate wage for this day
                if attendance_status == 1:  # Present
                    wage_earned = daily_wage
                    emp_present_days += 1
                elif attendance_status == 2:  # Half day
                    wage_earned = daily_wage / 2
                    emp_half_days += 1
                elif attendance_status == 3:  # Late (treat as present)
                    wage_earned = daily_wage
                    emp_present_days += 1
                elif attendance_status == 0:  # Absent
                    emp_absent_days += 1
            else:
                # No attendance record for this date - consider as absent
                emp_absent_days += 1
            
            emp_total_wages += wage_earned
            
            # Map status to readable format
            status_map = {0: 'Absent', 1: 'Present', 2: 'Half Day', 3: 'Late', None: 'No Record'}
            
            daily_data.append({
                'date': date_str,
                'day_name': current_date.strftime('%A'),
                'status': status_map.get(attendance_status),
                'status_code': attendance_status,
                'wage_earned': float(wage_earned)
            })
            
            current_date += timedelta(days=1)
        
        # Weekly breakdown for this employee
        weekly_breakdown = []
        emp_total_paid = Decimal('0')
        emp_total_pending = Decimal('0')
        
        for week in weeks_data:
            week_start = week['week_start']
            week_end = week['week_end']
            
            # Filter daily data for this week
            week_daily_data = [
                day for day in daily_data 
                if week_start <= datetime.strptime(day['date'], '%Y-%m-%d').date() <= week_end
            ]
            
            # Calculate week totals
            week_present = len([d for d in week_daily_data if d['status_code'] in [1, 3]])
            week_half_days = len([d for d in week_daily_data if d['status_code'] == 2])
            week_absent = len([d for d in week_daily_data if d['status_code'] in [0, None]])
            week_wages = sum(Decimal(str(d['wage_earned'])) for d in week_daily_data)
            
            # Get payment info from wage record
            week_paid_amount = Decimal('0')
            week_payment_status = 'pending'
            
            if week_start in wage_records:
                wage_record = wage_records[week_start]
                emp_wage_data = wage_record.get_employee_wage_data(emp_id)
                if emp_wage_data:
                    week_paid_amount = Decimal(str(emp_wage_data.get('paid_amount', 0)))
                    week_payment_status = emp_wage_data.get('payment_status', 'pending')
            
            emp_total_paid += week_paid_amount
            week_pending = week_wages - week_paid_amount
            emp_total_pending += week_pending
            
            weekly_breakdown.append({
                'week_start': week_start.isoformat(),
                'week_end': week_end.isoformat(),
                'present_days': week_present,
                'half_days': week_half_days,
                'absent_days': week_absent,
                'total_wages_earned': float(week_wages),
                'wages_paid': float(week_paid_amount),
                'wages_pending': float(week_pending),
                'payment_status': week_payment_status
            })
        
        # Calculate totals and percentages
        total_working_days = emp_present_days + emp_half_days + emp_absent_days
        attendance_percentage = 0
        payment_percentage = 0
        
        if total_working_days > 0:
            attendance_percentage = round((emp_present_days + emp_half_days * 0.5) / total_working_days * 100, 2)
        
        if float(emp_total_wages) > 0:
            payment_percentage = round(float(emp_total_paid) / float(emp_total_wages) * 100, 2)
        
        # Build response data structure that matches what Flutter expects
        response_data = {
            'success': True,
            'data': {
                'employee_id': emp_id,
                'employee_name': employee.name,
                'daily_wage': float(daily_wage),
                'period_summary': {
                    'total_days': total_working_days,
                    'present_days': emp_present_days,
                    'half_days': emp_half_days,
                    'absent_days': emp_absent_days,
                    'attendance_percentage': attendance_percentage,
                    'total_wages_earned': float(emp_total_wages),
                    'total_wages_paid': float(emp_total_paid),
                    'total_wages_pending': float(emp_total_pending),
                    'payment_percentage': payment_percentage
                },
                'daily_attendance': daily_data,
                'weekly_breakdown': weekly_breakdown,
                'report_period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'total_days': (end_date - start_date).days + 1,
                    'total_weeks': len(weeks_data)
                },
                'report_generated_at': timezone.now().isoformat()
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        print(f"Error generating single employee report: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': f'Failed to generate employee report: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def employee_summary_report(request):
    """
    Get a simplified summary report of employees for quick overview
    """
    try:
        # Get date range - last 28 days by default
        end_date = date.today()
        start_date = end_date - timedelta(days=27)
        
        # Allow custom date range
        custom_start = request.query_params.get('start_date')
        custom_end = request.query_params.get('end_date')
        
        if custom_start:
            start_date = datetime.strptime(custom_start, '%Y-%m-%d').date()
        if custom_end:
            end_date = datetime.strptime(custom_end, '%Y-%m-%d').date()
        
        employees = Employee.objects.filter(status=True)
        attendance_records = AttendanceRecord.objects.filter(
            date__range=[start_date, end_date]
        )
        
        # Create attendance lookup
        attendance_lookup = {}
        for record in attendance_records:
            attendance_lookup[record.date] = {
                emp['employee_id']: emp['status'] for emp in record.attendance_data
            }
        
        # Get recent wage payments
        recent_wage_records = WeeklyWagePayment.objects.filter(
            week_start_date__gte=start_date - timedelta(days=7)
        )
        
        employees_summary = []
        for employee in employees:
            emp_id = str(employee.id)
            current_wage = Wage.get_current_wage(employee)
            daily_wage = current_wage.amount if current_wage else Decimal('0')
            
            # Count attendance for the period
            present_days = 0
            half_days = 0
            total_possible_days = 0
            
            current_date = start_date
            while current_date <= end_date:
                total_possible_days += 1
                if (current_date in attendance_lookup and 
                    emp_id in attendance_lookup[current_date]):
                    status = attendance_lookup[current_date][emp_id]
                    if status in [1, 3]:  # Present or Late
                        present_days += 1
                    elif status == 2:  # Half day
                        half_days += 1
                current_date += timedelta(days=1)
            
            # Calculate recent payments
            recent_payments = Decimal('0')
            payment_status = 'No Recent Payments'
            
            for wage_record in recent_wage_records:
                emp_wage_data = wage_record.get_employee_wage_data(emp_id)
                if emp_wage_data:
                    recent_payments += Decimal(str(emp_wage_data.get('paid_amount', 0)))
                    if emp_wage_data.get('payment_status') in ['paid', 'partial']:
                        payment_status = 'Recent Payments Found'
            
            attendance_rate = round((present_days + half_days * 0.5) / max(total_possible_days, 1) * 100, 2)
            estimated_wages = (present_days * daily_wage) + (half_days * daily_wage / 2)
            
            employees_summary.append({
                'employee_id': emp_id,
                'employee_name': employee.name,
                'daily_wage': float(daily_wage),
                'present_days': present_days,
                'half_days': half_days,
                'attendance_rate': attendance_rate,
                'estimated_wages': float(estimated_wages),
                'recent_payments': float(recent_payments),
                'payment_status': payment_status,
                'has_current_wage': current_wage is not None
            })
        
        return Response({
            'report_period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'total_days': total_possible_days
            },
            'employees_summary': employees_summary,
            'total_employees': len(employees_summary),
            'report_generated_at': timezone.now().isoformat()
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate summary report: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def weekly_wages_report(request):
    """
    Get weekly wages report for all employees across multiple weeks
    """
    try:
        # Get number of weeks to look back (default 4 weeks)
        weeks_back = int(request.query_params.get('weeks_back', 4))
        
        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(weeks=weeks_back)
        
        # Get all Monday dates in the range
        week_starts = []
        current_date = get_monday_of_week(start_date)
        while current_date <= get_monday_of_week(end_date):
            week_starts.append(current_date)
            current_date += timedelta(weeks=1)
        
        employees = Employee.objects.filter(status=True)
        
        weekly_reports = []
        grand_totals = {
            'total_gross_wages': 0,
            'total_paid_wages': 0,
            'total_pending_wages': 0,
            'total_employees_across_weeks': 0
        }
        
        for week_start in week_starts:
            week_end = week_start + timedelta(days=6)
            
            # Get wage record for this week
            wage_record = WeeklyWagePayment.objects.filter(
                week_start_date=week_start
            ).first()
            
            week_data = {
                'week_start': week_start.isoformat(),
                'week_end': week_end.isoformat(),
                'wage_record_exists': wage_record is not None,
                'employees_data': [],
                'week_totals': {
                    'total_employees': 0,
                    'total_gross_wages': 0,
                    'total_paid_wages': 0,
                    'total_pending_wages': 0,
                    'fully_paid_employees': 0,
                    'partially_paid_employees': 0,
                    'unpaid_employees': 0
                }
            }
            
            if wage_record:
                # Use optimized wage record data
                for emp_wage_data in wage_record.employee_wages:
                    emp_data = {
                        'employee_id': emp_wage_data.get('employee_id'),
                        'employee_name': emp_wage_data.get('employee_name'),
                        'present_days': emp_wage_data.get('present_days', 0),
                        'half_days': emp_wage_data.get('half_days', 0),
                        'daily_wage': emp_wage_data.get('daily_wage', 0),
                        'gross_wages': emp_wage_data.get('gross_amount', 0),
                        'net_wages': emp_wage_data.get('net_amount', 0),
                        'paid_amount': emp_wage_data.get('paid_amount', 0),
                        'pending_amount': emp_wage_data.get('remaining_amount', 0),
                        'payment_status': emp_wage_data.get('payment_status', 'pending')
                    }
                    
                    week_data['employees_data'].append(emp_data)
                    
                    # Update week totals
                    week_data['week_totals']['total_gross_wages'] += emp_data['gross_wages']
                    week_data['week_totals']['total_paid_wages'] += emp_data['paid_amount']
                    week_data['week_totals']['total_pending_wages'] += emp_data['pending_amount']
                    
                    if emp_data['payment_status'] == 'paid':
                        week_data['week_totals']['fully_paid_employees'] += 1
                    elif emp_data['payment_status'] == 'partial':
                        week_data['week_totals']['partially_paid_employees'] += 1
                    else:
                        week_data['week_totals']['unpaid_employees'] += 1
                
                week_data['week_totals']['total_employees'] = len(wage_record.employee_wages)
                week_data['wage_record_id'] = wage_record.id
                week_data['payment_status'] = wage_record.payment_status
                
            else:
                # No wage record exists - build from attendance data
                week_dates = [week_start + timedelta(days=i) for i in range(7)]
                attendance_records = AttendanceRecord.objects.filter(date__in=week_dates)
                
                attendance_lookup = {}
                for record in attendance_records:
                    attendance_lookup[record.date] = {
                        emp['employee_id']: emp for emp in record.attendance_data
                    }
                
                for employee in employees:
                    emp_id = str(employee.id)
                    current_wage = Wage.get_current_wage(employee)
                    daily_wage = current_wage.amount if current_wage else Decimal('0')
                    
                    # Calculate attendance for this week
                    present_days = 0
                    half_days = 0
                    
                    for day_date in week_dates:
                        if (day_date in attendance_lookup and 
                            emp_id in attendance_lookup[day_date]):
                            status = attendance_lookup[day_date][emp_id].get('status')
                            if status in [1, 3]:  # Present or Late
                                present_days += 1
                            elif status == 2:  # Half day
                                half_days += 1
                    
                    gross_wages = (present_days * daily_wage) + (half_days * daily_wage / 2)
                    
                    emp_data = {
                        'employee_id': emp_id,
                        'employee_name': employee.name,
                        'present_days': present_days,
                        'half_days': half_days,
                        'daily_wage': float(daily_wage),
                        'gross_wages': float(gross_wages),
                        'net_wages': float(gross_wages),
                        'paid_amount': 0,
                        'pending_amount': float(gross_wages),
                        'payment_status': 'pending'
                    }
                    
                    if gross_wages > 0:  # Only include if employee worked
                        week_data['employees_data'].append(emp_data)
                        week_data['week_totals']['total_gross_wages'] += float(gross_wages)
                        week_data['week_totals']['total_pending_wages'] += float(gross_wages)
                        week_data['week_totals']['unpaid_employees'] += 1
                
                week_data['week_totals']['total_employees'] = len(week_data['employees_data'])
                week_data['payment_status'] = 'No Record'
            
            # Update grand totals
            grand_totals['total_gross_wages'] += week_data['week_totals']['total_gross_wages']
            grand_totals['total_paid_wages'] += week_data['week_totals']['total_paid_wages']
            grand_totals['total_pending_wages'] += week_data['week_totals']['total_pending_wages']
            grand_totals['total_employees_across_weeks'] += week_data['week_totals']['total_employees']
            
            weekly_reports.append(week_data)
        
        return Response({
            'report_period': {
                'weeks_covered': len(week_starts),
                'start_date': week_starts[0].isoformat() if week_starts else None,
                'end_date': (week_starts[-1] + timedelta(days=6)).isoformat() if week_starts else None
            },
            'grand_totals': grand_totals,
            'weekly_reports': weekly_reports,
            'report_generated_at': timezone.now().isoformat()
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate weekly wages report: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
