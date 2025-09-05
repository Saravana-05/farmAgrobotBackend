from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q
from django.utils import timezone
from django.db import transaction as db_transaction
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
from ...models import AttendanceRecord, BulkWagePayment, Employee, Wage, WeeklyWagePayment, WeeklyWagePaymentManager,Expense
from xe_farm import models


def get_wage_for_date(employee, target_date):
    """
    Get the wage rate that was effective for an employee on a specific date.
    
    Args:
        employee: Employee instance
        target_date: date object for which to find the wage rate
    
    Returns:
        Wage instance that was effective on target_date, or None if no wage found
    """
    # FIX: Use Q from django.db.models instead of models.Q
    wage = Wage.objects.filter(
        employee=employee,
        effective_from__lte=target_date
    ).filter(
        Q(effective_to__isnull=True) | Q(effective_to__gte=target_date)
    ).order_by('-effective_from').first()
    
    return wage

@api_view(['POST'])
def mark_attendance(request):
    """Mark attendance for multiple employees on a specific date with historical wages"""
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
    """Update attendance for a single employee on a specific date with historical wages"""
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
        employee = Employee.objects.get(id=employee_id, status=True)
        
        if employee.name != employee_name:
            return Response(
                {'error': f'Employee name mismatch. Expected: {employee.name}, Got: {employee_name}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except (ValueError, Employee.DoesNotExist):
        return Response(
            {'error': 'Invalid date format, employee not found, or employee is inactive'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # FIXED: Use historical wage rate for the attendance date
    historical_wage = get_wage_for_date(employee, attendance_date)
    if not historical_wage:
        return Response(
            {'error': f'Employee {employee_name} did not have a wage rate on {attendance_date_str}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if wages are already paid for this week
    week_start = get_monday_of_week(attendance_date)
    wage_records = WeeklyWagePayment.objects.filter(
        week_start_date=week_start,
        payment_status='paid'
    )
    
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
    
    with db_transaction.atomic():
        attendance_record, created = AttendanceRecord.objects.get_or_create(
            date=attendance_date,
            defaults={'attendance_data': []}
        )
        
        # Use historical wage amount
        wage_amount = historical_wage.amount
        
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
        'status': attendance_status,
        'wage_rate_used': float(wage_amount),
        'wage_effective_from': historical_wage.effective_from.isoformat(),
        'wage_effective_to': historical_wage.effective_to.isoformat() if historical_wage.effective_to else None
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
    """Validate employees before marking attendance with historical wage check"""
    serializer = EmployeeAttendanceValidationSerializer(data=request.data)
    
    if serializer.is_valid():
        employee_ids = serializer.validated_data['employee_ids']
        attendance_date_str = request.data.get('date')
        
        if not attendance_date_str:
            return Response(
                {'error': 'date is required for historical wage validation'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        employees = Employee.objects.filter(
            id__in=employee_ids, 
            status=True
        ).prefetch_related('wage_set')
        
        valid_employees = []
        invalid_employees = []
        
        for employee in employees:
            # FIXED: Get historical wage for the attendance date
            historical_wage = get_wage_for_date(employee, attendance_date)
            
            employee_data = {
                'employee_id': str(employee.id),
                'employee_name': employee.name,
                'daily_wage': float(historical_wage.amount) if historical_wage else 0.0,
                'has_wage': historical_wage is not None,
                'wage_period': {
                    'from': historical_wage.effective_from.isoformat() if historical_wage else None,
                    'to': historical_wage.effective_to.isoformat() if historical_wage and historical_wage.effective_to else None
                }
            }
            
            if historical_wage:
                valid_employees.append(employee_data)
            else:
                invalid_employees.append({
                    **employee_data,
                    'issue': f'No wage rate effective on {attendance_date_str}'
                })
        
        return Response({
            'attendance_date': attendance_date_str,
            'valid_employees': valid_employees,
            'invalid_employees': invalid_employees,
            'can_mark_attendance': len(invalid_employees) == 0,
            'message': 'All employees have valid wage rates for this date' if len(invalid_employees) == 0 
                      else f'{len(invalid_employees)} employees have wage rate issues for {attendance_date_str}',
            'historical_wage_validation': True
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
    """Pay all wages using optimized WeeklyWagePayment structure with historical wages"""
    try:
        print("=" * 80)
        print(f"STARTING BULK WAGE PAYMENT PROCESS")
        print(f"Week Start Date: {week_start_date}")
        print(f"Process Started At: {timezone.now()}")
        print("=" * 80)
        
        # Check if wage record already exists
        existing_wage_record = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        print(f"\nEXISTING RECORD CHECK:")
        if existing_wage_record:
            print(f"   Found existing wage record: ID = {existing_wage_record.id}")
            print(f"   Current payment status: {existing_wage_record.payment_status}")
            print(f"   Total employees in record: {existing_wage_record.total_employees}")
            print(f"   Total net amount: ${existing_wage_record.total_net_amount}")
            print(f"   Total paid amount: ${existing_wage_record.total_paid_amount}")
            print(f"   Total remaining: ${existing_wage_record.total_remaining_amount}")
            
            if existing_wage_record.payment_status == 'paid':
                print("   ERROR: Wages already fully paid for this week")
                return Response(
                    {'error': 'Wages already fully paid for this week'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            print(f"   No existing wage record found for week {week_start_date}")
        
        print(f"\nWAGE RECORD GENERATION/VALIDATION:")
        
        # FIXED: Always use historical wage generation method
        if not existing_wage_record:
            print(f"   Creating new wage record with historical rates...")
            print(f"   Calling: WeeklyWagePayment.generate_weekly_wage_record_with_historical_rates({week_start_date})")
            wage_record = WeeklyWagePaymentManager.generate_weekly_wage_record_with_historical_rates(week_start_date)
            print(f"   New wage record created: ID = {wage_record.id}")
        else:
            print(f"   Validating existing record for historical rates...")
            # Check if existing record uses historical rates
            if not validate_historical_wages_in_record(existing_wage_record):
                print("   WARNING: Existing record doesn't use historical rates. Recalculating...")
                existing_wage_record.recalculate_with_historical_rates()
                print("   Recalculation with historical rates completed")
            else:
                print("   Existing record already uses historical rates")
            wage_record = existing_wage_record
        
        # Print detailed wage record information
        print(f"\nWAGE RECORD DETAILS:")
        print(f"   Record ID: {wage_record.id}")
        print(f"   Week Period: {wage_record.week_start_date} to {wage_record.week_end_date}")
        print(f"   Total Employees: {wage_record.total_employees}")
        print(f"   Total Gross Amount: ${wage_record.total_gross_amount}")
        print(f"   Total Net Amount: ${wage_record.total_net_amount}")
        print(f"   Total Paid Amount: ${wage_record.total_paid_amount}")
        print(f"   Total Remaining: ${wage_record.total_remaining_amount}")
        print(f"   Payment Status: {wage_record.payment_status}")
        print(f"   Data Structure: optimized_single_record_with_json_array")
        
        # Print detailed employee wage data being stored
        print(f"\nEMPLOYEE WAGES DATA BEING STORED:")
        print(f"   Number of employees in JSON array: {len(wage_record.employee_wages)}")
        
        # Initialize historical wage info tracking
        historical_wage_info = {
            'employees_with_historical_calculation': 0,
            'employees_with_multiple_rates': 0,
            'wage_rate_changes_detected': []
        }
        
        for i, emp_data in enumerate(wage_record.employee_wages, 1):
            print(f"\n   Employee #{i}:")
            print(f"      ID: {emp_data.get('employee_id')}")
            print(f"      Name: {emp_data.get('employee_name')}")
            print(f"      Daily Wage: ${emp_data.get('daily_wage', 0)}")
            print(f"      Present Days: {emp_data.get('present_days', 0)}")
            print(f"      Half Days: {emp_data.get('half_days', 0)}")
            print(f"      Gross Amount: ${emp_data.get('gross_amount', 0)}")
            print(f"      Net Amount: ${emp_data.get('net_amount', 0)}")
            print(f"      Paid Amount: ${emp_data.get('paid_amount', 0)}")
            print(f"      Remaining: ${emp_data.get('remaining_amount', 0)}")
            print(f"      Payment Status: {emp_data.get('payment_status', 'pending')}")
            
            # Print historical wage calculation details
            historical_calc = emp_data.get('historical_wage_calculation', {})
            print(f"      Historical Calc Enabled: {historical_calc.get('enabled', False)}")
            if historical_calc.get('wage_changes'):
                print(f"      Wage Changes Detected: {len(historical_calc['wage_changes'])}")
                for change in historical_calc['wage_changes']:
                    print(f"         Date: {change['date']}, Rate: ${change['rate']}")
            
            # Print attendance details with daily wage rates
            attendance_details = emp_data.get('attendance_details', {})
            print(f"      Attendance Details ({len(attendance_details)} days):")
            for date_str, day_data in sorted(attendance_details.items()):
                status_map = {0: 'Absent', 1: 'Present', 2: 'Half Day', 3: 'Late'}
                status_text = status_map.get(day_data.get('status'), 'Unknown')
                print(f"         {date_str}: {status_text} (Rate: ${day_data.get('wage_rate', 0)})")
        
        # Validate that the wage record now has historical rates
        validation_result = validate_historical_wages_in_record(wage_record)
        print(f"\nHISTORICAL WAGE VALIDATION:")
        print(f"   Validation Result: {validation_result}")
        
        if not validation_result:
            print("   CRITICAL ERROR: Failed to generate wage record with historical rates")
            return Response(
                {'error': 'Failed to generate wage record with historical rates'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get payment details from request
        payment_mode = request.data.get('payment_mode', 'Cash')
        payment_reference = request.data.get('payment_reference', '')
        remarks = request.data.get('remarks', f'Bulk wage payment for week {week_start_date}')
        
        print(f"\nPAYMENT DETAILS FROM REQUEST:")
        print(f"   Payment Mode: {payment_mode}")
        print(f"   Payment Reference: '{payment_reference}'")
        print(f"   Remarks: '{remarks}'")
        print(f"   Request Data Keys: {list(request.data.keys())}")
        print(f"   Full Request Data: {dict(request.data)}")
        
        # Store BEFORE payment state for detailed comparison
        before_payment_state = {
            'total_paid_amount': float(wage_record.total_paid_amount),
            'payment_status': wage_record.payment_status,
            'individual_payments': {}
        }
        
        for emp_data in wage_record.employee_wages:
            emp_id = emp_data.get('employee_id')
            before_payment_state['individual_payments'][emp_id] = {
                'paid_amount': emp_data.get('paid_amount', 0),
                'remaining_amount': emp_data.get('remaining_amount', 0),
                'payment_status': emp_data.get('payment_status', 'pending')
            }
        
        print(f"\nDETAILED BEFORE PAYMENT STATE:")
        print(f"   Total Paid: ${before_payment_state['total_paid_amount']}")
        print(f"   Overall Status: {before_payment_state['payment_status']}")
        print(f"   Individual Employee States:")
        for emp_id, emp_state in before_payment_state['individual_payments'].items():
            emp_name = next((emp['employee_name'] for emp in wage_record.employee_wages 
                           if emp['employee_id'] == emp_id), 'Unknown')
            print(f"      {emp_name}: Paid=${emp_state['paid_amount']}, Remaining=${emp_state['remaining_amount']}, Status={emp_state['payment_status']}")
        
        # FIX: Use db_transaction instead of transaction to avoid naming conflict
        with db_transaction.atomic():
            print(f"\nEXECUTING ATOMIC TRANSACTION:")
            print(f"   Calling: wage_record.make_bulk_payment()")
            print(f"   Transaction started...")
            
            # Pay all pending wages
            total_payment = wage_record.make_bulk_payment(
                payment_mode=payment_mode,
                reference=payment_reference,
                remarks=remarks
            )
            
            print(f"   Bulk payment method returned: ${total_payment}")
            print(f"   Transaction completed successfully")
            
            if total_payment == 0:
                print("   ERROR: No pending payments found")
                return Response(
                    {'error': 'No pending payments found'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Refresh record from database and show AFTER state
        wage_record.refresh_from_db()
        
        print(f"\nAFTER PAYMENT STATE (Fresh from DB):")
        print(f"   Total Paid Amount: ${wage_record.total_paid_amount}")
        print(f"   Payment Status: {wage_record.payment_status}")
        print(f"   Total Remaining: ${wage_record.total_remaining_amount}")
        
        # Show changes in individual employee payments
        print(f"\nPAYMENT CHANGES PER EMPLOYEE:")
        for emp_data in wage_record.employee_wages:
            emp_id = emp_data.get('employee_id')
            emp_name = emp_data.get('employee_name')
            
            before_state = before_payment_state['individual_payments'].get(emp_id, {})
            after_paid = emp_data.get('paid_amount', 0)
            after_remaining = emp_data.get('remaining_amount', 0)
            after_payment_status = emp_data.get('payment_status', 'pending')
            
            before_paid = before_state.get('paid_amount', 0)
            payment_change = after_paid - before_paid
            
            print(f"   {emp_name}:")
            print(f"      Paid: ${before_paid} → ${after_paid} (Change: +${payment_change})")
            print(f"      Remaining: ${before_state.get('remaining_amount', 0)} → ${after_remaining}")
            print(f"      Status: {before_state.get('payment_status', 'pending')} → {after_payment_status}")
        
        # Print expense entry details if created
        if wage_record.expense_entry:
            print(f"\nEXPENSE ENTRY DETAILS:")
            expense = wage_record.expense_entry
            print(f"   Expense ID: {expense.id}")
            print(f"   Amount: ${expense.amount}")
            print(f"   Description: {expense.description}")
            print(f"   Date: {expense.date}")
            print(f"   Category: {expense.category}")
            print(f"   Payment Mode: {getattr(expense, 'payment_mode', 'N/A')}")
            print(f"   Reference: {getattr(expense, 'reference', 'N/A')}")
        
        # Print transaction records if any were created
        payment_transaction_records = wage_record.payment_transactions.all()
        if payment_transaction_records.exists():
            print(f"\nPAYMENT TRANSACTION RECORDS:")
            print(f"   Total transactions: {payment_transaction_records.count()}")
            for i, payment_transaction in enumerate(payment_transaction_records, 1):
                print(f"   Transaction #{i}:")
                print(f"      ID: {payment_transaction.id}")
                print(f"      Employee: {payment_transaction.employee_name} (ID: {payment_transaction.employee_id})")
                print(f"      Amount: ${payment_transaction.amount}")
                print(f"      Type: {payment_transaction.transaction_type}")
                print(f"      Mode: {payment_transaction.payment_mode}")
                print(f"      Reference: {payment_transaction.reference_number}")
                print(f"      Date: {payment_transaction.transaction_date}")
                print(f"      Remarks: {payment_transaction.remarks}")
        
        # Verify historical wage usage in the response
        print(f"\nFINAL HISTORICAL WAGE VERIFICATION:")
        
        for emp_data in wage_record.employee_wages:
            emp_name = emp_data.get('employee_name')
            historical_calc = emp_data.get('historical_wage_calculation', {})
            
            if historical_calc.get('enabled', False):
                historical_wage_info['employees_with_historical_calculation'] += 1
                print(f"   {emp_name}: Historical calculation verified")
                
                # Check for multiple wage rates in attendance details
                attendance_details = emp_data.get('attendance_details', {})
                wage_rates_used = set()
                for date_str, day_data in attendance_details.items():
                    if 'wage_rate' in day_data:
                        wage_rates_used.add(day_data['wage_rate'])
                
                if len(wage_rates_used) > 1:
                    historical_wage_info['employees_with_multiple_rates'] += 1
                    historical_wage_info['wage_rate_changes_detected'].append({
                        'employee_id': emp_data.get('employee_id'),
                        'employee_name': emp_data.get('employee_name'),
                        'wage_rates_used': list(wage_rates_used)
                    })
                    print(f"   {emp_name}: Multiple wage rates used - {sorted(list(wage_rates_used))}")
                    
                    # Print detailed rate usage by date
                    print(f"      Daily rate breakdown:")
                    for date_str, day_data in sorted(attendance_details.items()):
                        if 'wage_rate' in day_data:
                            status_map = {0: 'Absent', 1: 'Present', 2: 'Half Day', 3: 'Late'}
                            attendance_status = status_map.get(day_data.get('status'), 'Unknown')
                            print(f"         {date_str}: ${day_data['wage_rate']} ({attendance_status})")
                else:
                    print(f"   {emp_name}: Single wage rate used - ${list(wage_rates_used)[0] if wage_rates_used else 0}")
            else:
                print(f"   {emp_name}: Historical calculation NOT enabled")
        
        print(f"\nHISTORICAL WAGE SUMMARY:")
        print(f"   Employees with historical calculation: {historical_wage_info['employees_with_historical_calculation']}")
        print(f"   Employees with multiple rates: {historical_wage_info['employees_with_multiple_rates']}")
        print(f"   Total wage rate changes detected: {len(historical_wage_info['wage_rate_changes_detected'])}")
        
        # Print detailed wage change information
        if historical_wage_info['wage_rate_changes_detected']:
            print(f"\nDETAILED WAGE RATE CHANGES:")
            for change_info in historical_wage_info['wage_rate_changes_detected']:
                print(f"   {change_info['employee_name']} (ID: {change_info['employee_id']}):")
                print(f"      Rates used: {change_info['wage_rates_used']}")
        
        # Print complete JSON data structure being stored
        print(f"\nCOMPLETE JSON DATA STRUCTURE BEING STORED:")
        print(f"   WeeklyWagePayment Model Fields:")
        print(f"      id: {wage_record.id}")
        print(f"      week_start_date: {wage_record.week_start_date}")
        print(f"      week_end_date: {wage_record.week_end_date}")
        print(f"      total_employees: {wage_record.total_employees}")
        print(f"      total_gross_amount: {wage_record.total_gross_amount}")
        print(f"      total_net_amount: {wage_record.total_net_amount}")
        print(f"      total_paid_amount: {wage_record.total_paid_amount}")
        print(f"      total_remaining_amount: {wage_record.total_remaining_amount}")
        print(f"      payment_status: {wage_record.payment_status}")
        print(f"      created_at: {wage_record.created_at}")
        print(f"      updated_at: {wage_record.updated_at}")
        
        # Print complete employee_wages JSON array
        print(f"\nEMPLOYEE_WAGES JSON ARRAY (Complete Structure):")
        import json
        try:
            formatted_json = json.dumps(wage_record.employee_wages, indent=2, default=str)
            print(formatted_json)
        except Exception as json_error:
            print(f"   Error formatting JSON: {json_error}")
            print(f"   Raw employee_wages data: {wage_record.employee_wages}")
        
        # Validate that the wage record now has historical rates
        validation_result = validate_historical_wages_in_record(wage_record)
        print(f"\nFINAL VALIDATION:")
        print(f"   Historical wage validation: {validation_result}")
        
        if not validation_result:
            print("   CRITICAL ERROR: Final validation failed")
            return Response(
                {'error': 'Failed to generate wage record with historical rates'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get payment details from request
        payment_mode = request.data.get('payment_mode', 'Cash')
        payment_reference = request.data.get('payment_reference', '')
        remarks = request.data.get('remarks', f'Bulk wage payment for week {week_start_date}')
        
        print(f"\nPAYMENT DETAILS FROM REQUEST:")
        print(f"   Payment Mode: {payment_mode}")
        print(f"   Payment Reference: '{payment_reference}'")
        print(f"   Remarks: '{remarks}'")
        print(f"   Request Data Keys: {list(request.data.keys())}")
        print(f"   Full Request Data: {dict(request.data)}")
        
        # Store BEFORE payment state for detailed comparison
        before_payment_state = {
            'total_paid_amount': float(wage_record.total_paid_amount),
            'payment_status': wage_record.payment_status,
            'individual_payments': {}
        }
        
        for emp_data in wage_record.employee_wages:
            emp_id = emp_data.get('employee_id')
            before_payment_state['individual_payments'][emp_id] = {
                'paid_amount': emp_data.get('paid_amount', 0),
                'remaining_amount': emp_data.get('remaining_amount', 0),
                'payment_status': emp_data.get('payment_status', 'pending')
            }
        
        print(f"\nDETAILED BEFORE PAYMENT STATE:")
        print(f"   Total Paid: ${before_payment_state['total_paid_amount']}")
        print(f"   Overall Status: {before_payment_state['payment_status']}")
        print(f"   Individual Employee States:")
        for emp_id, emp_state in before_payment_state['individual_payments'].items():
            emp_name = next((emp['employee_name'] for emp in wage_record.employee_wages 
                           if emp['employee_id'] == emp_id), 'Unknown')
            print(f"      {emp_name}: Paid=${emp_state['paid_amount']}, Remaining=${emp_state['remaining_amount']}, Status={emp_state['payment_status']}")
        
        with db_transaction.atomic():
            print(f"\nEXECUTING ATOMIC TRANSACTION:")
            print(f"   Calling: wage_record.make_bulk_payment()")
            print(f"   Transaction started...")
            
            # Pay all pending wages
            total_payment = wage_record.make_bulk_payment(
                payment_mode=payment_mode,
                reference=payment_reference,
                remarks=remarks
            )
            
            print(f"   Bulk payment method returned: ${total_payment}")
            print(f"   Transaction completed successfully")
            
            if total_payment == 0:
                print("   ERROR: No pending payments found")
                return Response(
                    {'error': 'No pending payments found'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Refresh record from database and show AFTER state
        wage_record.refresh_from_db()
        
        print(f"\nAFTER PAYMENT STATE (Fresh from DB):")
        print(f"   Total Paid Amount: ${wage_record.total_paid_amount}")
        print(f"   Payment Status: {wage_record.payment_status}")
        print(f"   Total Remaining: ${wage_record.total_remaining_amount}")
        
        # Show changes in individual employee payments
        print(f"\nPAYMENT CHANGES PER EMPLOYEE:")
        for emp_data in wage_record.employee_wages:
            emp_id = emp_data.get('employee_id')
            emp_name = emp_data.get('employee_name')
            
            before_state = before_payment_state['individual_payments'].get(emp_id, {})
            after_paid = emp_data.get('paid_amount', 0)
            after_remaining = emp_data.get('remaining_amount', 0)
            after_payment_status = emp_data.get('payment_status', 'pending')
            
            before_paid = before_state.get('paid_amount', 0)
            payment_change = after_paid - before_paid
            
            print(f"   {emp_name}:")
            print(f"      Paid: ${before_paid} → ${after_paid} (Change: +${payment_change})")
            print(f"      Remaining: ${before_state.get('remaining_amount', 0)} → ${after_remaining}")
            print(f"      Status: {before_state.get('payment_status', 'pending')} → {after_payment_status}")
        
        # Print expense entry details if created
        if wage_record.expense_entry:
            print(f"\nEXPENSE ENTRY DETAILS:")
            expense = wage_record.expense_entry
            print(f"   Expense ID: {expense.id}")
            print(f"   Amount: ${expense.amount}")
            print(f"   Description: {expense.description}")
            print(f"   Date: {expense.date}")
            print(f"   Category: {expense.category}")
            print(f"   Payment Mode: {getattr(expense, 'payment_mode', 'N/A')}")
            print(f"   Reference: {getattr(expense, 'reference', 'N/A')}")
        
        # Print transaction records if any were created
        payment_transaction_records = wage_record.payment_transactions.all()
        if payment_transaction_records.exists():
            print(f"\nPAYMENT TRANSACTION RECORDS:")
            print(f"   Total transactions: {payment_transaction_records.count()}")
            for i, payment_transaction in enumerate(payment_transaction_records, 1):
                print(f"   Transaction #{i}:")
                print(f"      ID: {payment_transaction.id}")
                print(f"      Employee: {payment_transaction.employee_name} (ID: {payment_transaction.employee_id})")
                print(f"      Amount: ${payment_transaction.amount}")
                print(f"      Type: {payment_transaction.transaction_type}")
                print(f"      Mode: {payment_transaction.payment_mode}")
                print(f"      Reference: {payment_transaction.reference_number}")
                print(f"      Date: {payment_transaction.transaction_date}")
                print(f"      Remarks: {payment_transaction.remarks}")
        
        # Verify historical wage usage in the response
        print(f"\nFINAL HISTORICAL WAGE VERIFICATION:")
        
        for emp_data in wage_record.employee_wages:
            emp_name = emp_data.get('employee_name')
            historical_calc = emp_data.get('historical_wage_calculation', {})
            
            if historical_calc.get('enabled', False):
                historical_wage_info['employees_with_historical_calculation'] += 1
                print(f"   {emp_name}: Historical calculation verified")
                
                # Check for multiple wage rates in attendance details
                attendance_details = emp_data.get('attendance_details', {})
                wage_rates_used = set()
                for date_str, day_data in attendance_details.items():
                    if 'wage_rate' in day_data:
                        wage_rates_used.add(day_data['wage_rate'])
                
                if len(wage_rates_used) > 1:
                    historical_wage_info['employees_with_multiple_rates'] += 1
                    historical_wage_info['wage_rate_changes_detected'].append({
                        'employee_id': emp_data.get('employee_id'),
                        'employee_name': emp_data.get('employee_name'),
                        'wage_rates_used': list(wage_rates_used)
                    })
                    print(f"   {emp_name}: Multiple wage rates used - {sorted(list(wage_rates_used))}")
                    
                    # Print detailed rate usage by date
                    print(f"      Daily rate breakdown:")
                    for date_str, day_data in sorted(attendance_details.items()):
                        if 'wage_rate' in day_data:
                            status_map = {0: 'Absent', 1: 'Present', 2: 'Half Day', 3: 'Late'}
                            attendance_status = status_map.get(day_data.get('status'), 'Unknown')
                            print(f"         {date_str}: ${day_data['wage_rate']} ({attendance_status})")
                else:
                    print(f"   {emp_name}: Single wage rate used - ${list(wage_rates_used)[0] if wage_rates_used else 0}")
            else:
                print(f"   {emp_name}: Historical calculation NOT enabled")
        
        print(f"\nHISTORICAL WAGE SUMMARY:")
        print(f"   Employees with historical calculation: {historical_wage_info['employees_with_historical_calculation']}")
        print(f"   Employees with multiple rates: {historical_wage_info['employees_with_multiple_rates']}")
        print(f"   Total wage rate changes detected: {len(historical_wage_info['wage_rate_changes_detected'])}")
        
        # Print detailed wage change information
        if historical_wage_info['wage_rate_changes_detected']:
            print(f"\nDETAILED WAGE RATE CHANGES:")
            for change_info in historical_wage_info['wage_rate_changes_detected']:
                print(f"   {change_info['employee_name']} (ID: {change_info['employee_id']}):")
                print(f"      Rates used: {change_info['wage_rates_used']}")
        
        # Prepare final response data
        response_data = {
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
            'expense_recorded': wage_record.expense_entry is not None,
            'historical_wages_applied': True,
            'historical_wage_validation': historical_wage_info
        }
        
        print(f"\nFINAL RESPONSE DATA:")
        print(f"   Response Keys: {list(response_data.keys())}")
        print(f"   Total Amount Paid: ${response_data['total_amount_paid']}")
        print(f"   Total Employees: {response_data['total_employees']}")
        print(f"   Data Structure: {response_data['data_structure']}")
        print(f"   Expense Recorded: {response_data['expense_recorded']}")
        print(f"   Historical Wages Applied: {response_data['historical_wages_applied']}")
        
        print(f"\nHISTORICAL WAGE VALIDATION SUMMARY:")
        validation_info = response_data['historical_wage_validation']
        print(f"   Employees with historical calculation: {validation_info['employees_with_historical_calculation']}")
        print(f"   Employees with multiple rates: {validation_info['employees_with_multiple_rates']}")
        print(f"   Wage rate changes detected: {len(validation_info['wage_rate_changes_detected'])}")
        
        print("=" * 80)
        print(f"BULK WAGE PAYMENT PROCESS COMPLETED SUCCESSFULLY")
        print(f"Total Payment Processed: ${total_payment}")
        print(f"Week: {week_start_date} to {wage_record.week_end_date}")
        print(f"Process Completed At: {timezone.now()}")
        print("=" * 80)
        
        return Response(response_data)
        
    except Exception as e:
        print("=" * 80)
        print(f"CRITICAL ERROR IN BULK WAGE PAYMENT:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        print(f"   Week Start Date: {week_start_date}")
        print(f"   Error Time: {timezone.now()}")
        
        import traceback
        print(f"\nFULL STACK TRACE:")
        traceback.print_exc()
        print("=" * 80)
        
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
            wage_record = WeeklyWagePaymentManager.generate_weekly_wage_record_with_historical_rates(week_start_date)
            print(f"New wage record created: ID = {wage_record.id}")
        else:
            print(f"Using existing wage record: ID = {wage_record.id}")
        
        # Print BEFORE state
        emp_data_before = wage_record.get_employee_wage_data(employee_id)
        print(f"BEFORE UPDATE - Employee data: {emp_data_before}")
        
        with db_transaction.atomic():
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
    """Get weekly attendance data using historical wage rates"""
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
        
        wage_record = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        bulk_payment = BulkWagePayment.objects.filter(
            week_start_date=week_start_date
        ).first()
        
        employees = Employee.objects.filter(status=True)
        
        attendance_records = AttendanceRecord.objects.filter(
            date__in=week_dates
        )
        
        attendance_lookup = {record.date: record.attendance_data for record in attendance_records}
        
        daily_counts = defaultdict(int)
        for record_date, attendance_data in attendance_lookup.items():
            if attendance_data:
                present_count = len([emp for emp in attendance_data if emp.get('status') == 1])
                daily_counts[record_date.isoformat()] = present_count
        
        employees_data = []
        total_wages = 0
        wages_paid = False
        payment_type = 'none'
        
        if wage_record:
            wages_paid = wage_record.payment_status in ['Fully Paid', 'Partial']
            payment_type = 'optimized'
            
            wage_employee_lookup = {emp['employee_id']: emp for emp in wage_record.employee_wages}
            
            for employee in employees:
                emp_id = str(employee.id)
                
                # FIXED: Get historical wage for the week start date
                historical_wage = get_wage_for_date(employee, week_start_date)
                daily_wage = historical_wage.amount if historical_wage else Decimal('0')
                
                wage_emp_data = wage_employee_lookup.get(emp_id)
                
                if wage_emp_data:
                    employee_attendance = wage_emp_data.get('attendance_details', {})
                    present_days = wage_emp_data.get('present_days', 0)
                    half_days = wage_emp_data.get('half_days', 0)
                    total_wage = Decimal(str(wage_emp_data.get('net_amount', 0)))
                    payment_status = wage_emp_data.get('payment_status', 'pending')
                    partial_payment = Decimal(str(wage_emp_data.get('paid_amount', 0)))
                    remaining_amount = Decimal(str(wage_emp_data.get('remaining_amount', 0)))
                else:
                    # Build from attendance with historical wage
                    employee_attendance, present_days, half_days, total_wage = _build_employee_attendance_data(
                        emp_id, week_dates, attendance_lookup, week_start_date
                    )
                    payment_status = 'pending'
                    partial_payment = Decimal('0')
                    remaining_amount = total_wage
                
                employees_data.append({
                    'employee_id': emp_id,
                    'employee_name': employee.name,
                    'daily_wage': float(daily_wage),
                    'wage_effective_period': {
                        'from': historical_wage.effective_from.isoformat() if historical_wage else None,
                        'to': historical_wage.effective_to.isoformat() if historical_wage and historical_wage.effective_to else None
                    },
                    'attendance': employee_attendance,
                    'present_days': present_days,
                    'half_days': half_days,
                    'total_wages': float(total_wage),
                    'payment_status': payment_status,
                    'partial_payment': float(partial_payment),
                    'remaining_amount': float(remaining_amount)
                })
                
                total_wages += float(total_wage)
        
        elif bulk_payment:
            wages_paid = True
            payment_type = 'bulk'
            
            bulk_payment_lookup = {emp['employee_id']: emp for emp in bulk_payment.employee_payments}
            
            for employee in employees:
                emp_id = str(employee.id)
                
                # FIXED: Get historical wage for the week start date
                historical_wage = get_wage_for_date(employee, week_start_date)
                daily_wage = historical_wage.amount if historical_wage else Decimal('0')
                
                bulk_emp_data = bulk_payment_lookup.get(emp_id)
                
                if bulk_emp_data:
                    employee_attendance = bulk_emp_data.get('attendance_details', {})
                    present_days = bulk_emp_data.get('present_days', 0)
                    half_days = bulk_emp_data.get('half_days', 0)
                    total_wage = Decimal(str(bulk_emp_data.get('total_wages', 0)))
                    payment_status = 'paid'
                    partial_payment = total_wage
                    remaining_amount = Decimal('0')
                else:
                    # Build from attendance with historical wage
                    employee_attendance, present_days, half_days, total_wage = _build_employee_attendance_data(
                        emp_id, week_dates, attendance_lookup, week_start_date
                    )
                    payment_status = 'pending'
                    partial_payment = Decimal('0')
                    remaining_amount = total_wage
                
                employees_data.append({
                    'employee_id': emp_id,
                    'employee_name': employee.name,
                    'daily_wage': float(daily_wage),
                    'wage_effective_period': {
                        'from': historical_wage.effective_from.isoformat() if historical_wage else None,
                        'to': historical_wage.effective_to.isoformat() if historical_wage and historical_wage.effective_to else None
                    },
                    'attendance': employee_attendance,
                    'present_days': present_days,
                    'half_days': half_days,
                    'total_wages': float(total_wage),
                    'payment_status': payment_status,
                    'partial_payment': float(partial_payment),
                    'remaining_amount': float(remaining_amount)
                })
                
                total_wages += float(total_wage)
        
        else:
            # No payments exist - build from attendance with historical wages
            payment_type = 'none'
            wages_paid = False
            
            for employee in employees:
                emp_id = str(employee.id)
                
                # FIXED: Get historical wage for the week start date
                historical_wage = get_wage_for_date(employee, week_start_date)
                daily_wage = historical_wage.amount if historical_wage else Decimal('0')
                
                employee_attendance, present_days, half_days, total_wage = _build_employee_attendance_data(
                    emp_id, week_dates, attendance_lookup, week_start_date
                )
                
                employees_data.append({
                    'employee_id': emp_id,
                    'employee_name': employee.name,
                    'daily_wage': float(daily_wage),
                    'wage_effective_period': {
                        'from': historical_wage.effective_from.isoformat() if historical_wage else None,
                        'to': historical_wage.effective_to.isoformat() if historical_wage and historical_wage.effective_to else None
                    },
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
            'weekly_employee_count': len(employees_data),
            'historical_wages_applied': True
        }
        
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
        
        return Response(response_data)
        
    except Exception as e:
        print(f"Error in weekly_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Failed to fetch weekly data: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        

def _build_employee_attendance_data(emp_id, week_dates, attendance_lookup, target_date=None):
    """
    Helper function to build employee attendance data with historical wages
    
    Args:
        emp_id: Employee ID
        week_dates: List of dates in the week
        attendance_lookup: Dictionary mapping dates to attendance data
        target_date: Optional specific date for wage calculation (uses first week date if not provided)
    """
    employee = Employee.objects.get(id=emp_id)
    
    # Use the first date of the week for wage calculation if no specific date provided
    wage_date = target_date or week_dates[0]
    historical_wage = get_wage_for_date(employee, wage_date)
    daily_wage = historical_wage.amount if historical_wage else Decimal('0')
    
    employee_attendance = {}
    present_days = 0
    half_days = 0
    late_days = 0
    
    for week_date in week_dates:
        date_str = week_date.isoformat()
        employee_status = None
        
        if week_date in attendance_lookup and attendance_lookup[week_date]:
            for emp_data in attendance_lookup[week_date]:
                if str(emp_data.get('employee_id')) == emp_id:
                    employee_status = emp_data.get('status')
                    break
        
        employee_attendance[date_str] = employee_status
        
        if employee_status == 1:  # Present
            present_days += 1
        elif employee_status == 2:  # Half day
            half_days += 1
        elif employee_status == 3:  # Late (treat as present)
            late_days += 1
            present_days += 1
    
    total_wage = (present_days * daily_wage) + (half_days * daily_wage / 2)
    
    return employee_attendance, present_days, half_days, total_wage



@api_view(['GET'])
def wage_payment_history(request):
    """Get optimized wage payment history"""
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    
    queryset = WeeklyWagePaymentManager.objects.all()
    
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
        wage_record = WeeklyWagePaymentManager.objects.get(id=record_id)
    except WeeklyWagePaymentManager.DoesNotExist:
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
        wage_record = WeeklyWagePaymentManager.generate_weekly_wage_record_with_historical_rates(week_start_date)
        
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
    Get comprehensive employee report with historical wage rates
    """
    try:
        try:
            employee = Employee.objects.get(id=employee_id, status=True)
        except Employee.DoesNotExist:
            return Response(
                {'error': f'Employee with ID {employee_id} not found or inactive'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get date range
        end_date = date.today()
        start_date = end_date - timedelta(days=27)
        
        custom_start = request.query_params.get('start_date')
        custom_end = request.query_params.get('end_date')
        
        if custom_start:
            start_date = datetime.strptime(custom_start, '%Y-%m-%d').date()
        if custom_end:
            end_date = datetime.strptime(custom_end, '%Y-%m-%d').date()
        
        emp_id = str(employee.id)
        
        # Get attendance records
        attendance_records = AttendanceRecord.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('date')
        
        attendance_lookup = {}
        for record in attendance_records:
            attendance_lookup[record.date] = {
                emp['employee_id']: emp for emp in record.attendance_data
            }
        
        # Build daily data with historical wage rates
        daily_data = []
        emp_present_days = 0
        emp_half_days = 0
        emp_absent_days = 0
        emp_total_wages = Decimal('0')
        wage_changes = []  # Track wage rate changes
        
        current_date = start_date
        last_wage_rate = None
        
        while current_date <= end_date:
            date_str = current_date.isoformat()
            
            # Get the historical wage rate for this specific date
            historical_wage = get_wage_for_date(employee, current_date)
            daily_wage = historical_wage.amount if historical_wage else Decimal('0')
            
            # Track wage rate changes
            if last_wage_rate != daily_wage and historical_wage:
                wage_changes.append({
                    'date': date_str,
                    'wage_rate': float(daily_wage),
                    'effective_from': historical_wage.effective_from.isoformat(),
                    'effective_to': historical_wage.effective_to.isoformat() if historical_wage.effective_to else None
                })
                last_wage_rate = daily_wage
            
            # Get attendance status
            attendance_status = None
            wage_earned = Decimal('0')
            
            if current_date in attendance_lookup and emp_id in attendance_lookup[current_date]:
                emp_attendance = attendance_lookup[current_date][emp_id]
                attendance_status = emp_attendance.get('status')
                
                # Calculate wage using the historical rate for this date
                if attendance_status == 1:  # Present
                    wage_earned = daily_wage
                    emp_present_days += 1
                elif attendance_status == 2:  # Half day
                    wage_earned = daily_wage / 2
                    emp_half_days += 1
                elif attendance_status == 3:  # Late
                    wage_earned = daily_wage
                    emp_present_days += 1
                elif attendance_status == 0:  # Absent
                    emp_absent_days += 1
            else:
                emp_absent_days += 1
            
            emp_total_wages += wage_earned
            
            status_map = {0: 'Absent', 1: 'Present', 2: 'Half Day', 3: 'Late', None: 'No Record'}
            
            daily_data.append({
                'date': date_str,
                'day_name': current_date.strftime('%A'),
                'status': status_map.get(attendance_status),
                'status_code': attendance_status,
                'wage_earned': float(wage_earned),
                'daily_wage_rate': float(daily_wage),
                'wage_effective_from': historical_wage.effective_from.isoformat() if historical_wage else None,
                'wage_effective_to': historical_wage.effective_to.isoformat() if historical_wage and historical_wage.effective_to else None
            })
            
            current_date += timedelta(days=1)
        
        # Get weeks and calculate payments
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
        
        # Get wage payment records
        wage_records = {}
        for week in weeks_data:
            wage_record = WeeklyWagePayment.objects.filter(
                week_start_date=week['week_start']
            ).first()
            if wage_record:
                wage_records[week['week_start']] = wage_record
        
        # Build weekly breakdown with historical wages
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
            
            # Get payment info
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
            
            # Check if multiple wage rates were used in this week
            week_wage_rates = list(set(d['daily_wage_rate'] for d in week_daily_data if d['daily_wage_rate'] > 0))
            
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
                'wage_rates_used': week_wage_rates,
                'multiple_rates': len(week_wage_rates) > 1
            })
        
        # Calculate totals and percentages
        total_working_days = emp_present_days + emp_half_days + emp_absent_days
        attendance_percentage = 0
        payment_percentage = 0
        
        if total_working_days > 0:
            attendance_percentage = round((emp_present_days + emp_half_days * 0.5) / total_working_days * 100, 2)
        
        if float(emp_total_wages) > 0:
            payment_percentage = round(float(emp_total_paid) / float(emp_total_wages) * 100, 2)
        
        response_data = {
            'success': True,
            'data': {
                'employee_id': emp_id,
                'employee_name': employee.name,
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
                'wage_rate_changes': wage_changes,
                'historical_wage_calculation': {
                    'enabled': True,
                    'total_wage_changes': len(wage_changes),
                    'date_range_checked': f"{start_date.isoformat()} to {end_date.isoformat()}"
                },
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
        print(f"Error generating historical employee report: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'success': False,
            'error': f'Failed to generate employee report: {str(e)}',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def employee_wage_history(request, employee_id):
    """
    Get complete wage history for an employee
    """
    try:
        employee = Employee.objects.get(id=employee_id, status=True)
    except Employee.DoesNotExist:
        return Response(
            {'error': f'Employee with ID {employee_id} not found or inactive'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get all wage records for this employee
    wage_records = Wage.objects.filter(
        employee=employee
    ).order_by('effective_from')
    
    wage_history = []
    for wage in wage_records:
        wage_history.append({
            'id': wage.id,
            'amount': float(wage.amount),
            'effective_from': wage.effective_from.isoformat(),
            'effective_to': wage.effective_to.isoformat() if wage.effective_to else None,
            'is_current': wage.effective_to is None,
            'duration_days': (wage.effective_to - wage.effective_from).days if wage.effective_to else 'Ongoing',
            'remarks': wage.remarks,
            'created_at': wage.created_at.isoformat()
        })
    
    # Calculate wage statistics
    if wage_history:
        amounts = [w['amount'] for w in wage_history]
        wage_stats = {
            'total_wage_changes': len(wage_history),
            'highest_wage': max(amounts),
            'lowest_wage': min(amounts),
            'current_wage': wage_history[-1]['amount'] if wage_history else 0,
            'first_wage': wage_history[0]['amount'],
            'total_increase': wage_history[-1]['amount'] - wage_history[0]['amount'] if len(wage_history) > 1 else 0
        }
    else:
        wage_stats = {
            'total_wage_changes': 0,
            'highest_wage': 0,
            'lowest_wage': 0,
            'current_wage': 0,
            'first_wage': 0,
            'total_increase': 0
        }
    
    return Response({
        'employee_id': str(employee.id),
        'employee_name': employee.name,
        'wage_history': wage_history,
        'wage_statistics': wage_stats,
        'report_generated_at': timezone.now().isoformat()
    })

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
    
def validate_historical_wages_in_record(wage_record):
    """
    Validate that a wage record uses historical wage rates
    Returns True if valid, False if needs recalculation
    """
    for emp_data in wage_record.employee_wages:
        # Check if historical wage calculation flag exists
        if not emp_data.get('historical_wage_calculation', {}).get('enabled', False):
            return False
        
        # Check if attendance_details contain daily wage rates
        attendance_details = emp_data.get('attendance_details', {})
        if not attendance_details:
            return False
        
        # Verify that daily wage rates exist for each day
        for date_str, day_data in attendance_details.items():
            if 'wage_rate' not in day_data:
                return False
    
    return True

@api_view(['GET'])
def validate_wage_record_historical_rates(request, record_id):
    """
    Validate that a wage record uses historical rates and fix if needed
    """
    try:
        wage_record = WeeklyWagePaymentManager.objects.get(id=record_id)
        
        is_valid = validate_historical_wages_in_record(wage_record)
        
        if not is_valid:
            print(f"Wage record {record_id} needs historical rate recalculation")
            wage_record.recalculate_with_historical_rates()
            is_valid = True
            message = "Wage record recalculated with historical rates"
        else:
            message = "Wage record already uses historical rates"
        
        return Response({
            'wage_record_id': record_id,
            'uses_historical_rates': is_valid,
            'message': message,
            'total_employees': wage_record.total_employees,
            'total_net_amount': float(wage_record.total_net_amount),
            'validation_details': {
                'employees_with_historical_data': len([
                    emp for emp in wage_record.employee_wages 
                    if emp.get('historical_wage_calculation', {}).get('enabled', False)
                ]),
                'total_employees': len(wage_record.employee_wages)
            }
        })
        
    except WeeklyWagePaymentManager.DoesNotExist:
        return Response(
            {'error': 'Wage record not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Validation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def fix_all_wage_records_historical_rates(request):
    """
    Fix all existing wage records to use historical rates
    """
    try:
        # Get all wage records that might need fixing
        wage_records = WeeklyWagePaymentManager.objects.all()
        
        fixed_records = []
        skipped_records = []
        
        for wage_record in wage_records:
            try:
                if not validate_historical_wages_in_record(wage_record):
                    print(f"Fixing wage record {wage_record.id} for week {wage_record.week_start_date}")
                    wage_record.recalculate_with_historical_rates()
                    fixed_records.append({
                        'id': wage_record.id,
                        'week_start': wage_record.week_start_date.isoformat(),
                        'employees': wage_record.total_employees,
                        'new_total': float(wage_record.total_net_amount)
                    })
                else:
                    skipped_records.append({
                        'id': wage_record.id,
                        'week_start': wage_record.week_start_date.isoformat(),
                        'reason': 'Already uses historical rates'
                    })
                    
            except Exception as e:
                print(f"Error fixing wage record {wage_record.id}: {str(e)}")
                skipped_records.append({
                    'id': wage_record.id,
                    'week_start': wage_record.week_start_date.isoformat(),
                    'reason': f'Error: {str(e)}'
                })
        
        return Response({
            'message': f'Fixed {len(fixed_records)} wage records with historical rates',
            'fixed_records': fixed_records,
            'skipped_records': skipped_records,
            'total_processed': len(wage_records),
            'success_rate': len(fixed_records) / len(wage_records) * 100 if wage_records else 0
        })
        
    except Exception as e:
        return Response(
            {'error': f'Batch fix failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )