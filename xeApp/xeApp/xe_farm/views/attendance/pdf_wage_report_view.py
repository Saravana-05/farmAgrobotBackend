import os
from django.conf import settings
from rest_framework.decorators import api_view, renderer_classes
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, date, timedelta
from decimal import Decimal
from io import BytesIO

# Import reportlab for PDF generation
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

from ...utils import get_monday_of_week, get_week_dates
from ...models import AttendanceRecord, WeeklyWagePayment, BulkWagePayment, Employee, Wage




@api_view(['GET'])
def generate_weekly_wage_pdf(request):
    """Generate PDF for weekly wage report with enhanced error handling"""
    week_start = request.query_params.get('week_start')
    
    if not week_start:
        # Return JSON error as HttpResponse
        error_response = json.dumps({'error': 'week_start date is required'})
        response = HttpResponse(error_response, content_type='application/json')
        response.status_code = 400
        return response
    
    try:
        week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
        week_end_date = week_start_date + timedelta(days=6)  # 7-day range
    except ValueError:
        error_response = json.dumps({'error': 'Invalid date format. Use YYYY-MM-DD'})
        response = HttpResponse(error_response, content_type='application/json')
        response.status_code = 400
        return response
    
    try:
        # Generate PDF for the full week with error handling
        pdf_buffer = _generate_wage_pdf(week_start_date, week_end_date)
        
        if not pdf_buffer:
            error_response = json.dumps({'error': 'Failed to generate PDF - no data or processing error'})
            response = HttpResponse(error_response, content_type='application/json')
            response.status_code = 500
            return response
        
        # Create PDF response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="weekly_wages_{week_start_date}_to_{week_end_date}.pdf"'
        return response
        
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        error_response = json.dumps({'error': f'Failed to generate PDF: {str(e)}'})
        response = HttpResponse(error_response, content_type='application/json')
        response.status_code = 500
        return response




@api_view(['GET'])
def generate_wage_range_pdf(request):
    """Generate PDF for wage report within a date range"""
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
        
        if from_date > to_date:
            return Response(
                {'error': 'from_date cannot be later than to_date'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Generate PDF for date range
        pdf_buffer = _generate_wage_pdf(from_date, to_date, is_range=True)
        
        # Create HTTP response
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="wage_report_{from_date}_to_{to_date}.pdf"'
        
        return response
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate PDF: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _generate_wage_pdf(start_date, end_date, is_range=False):
    """Generate PDF document for wage report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # Build the story (content)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER
    )
    
    # Add company header
    story.extend(_add_company_header(styles))
    
    # Add title based on report type
    if is_range:
        title = f"Employee Wage Report<br/>From {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}"
    else:
        week_dates = get_week_dates(start_date)
        week_end = week_dates[-1]
        title = f"Weekly Wage Report<br/>Week: {start_date.strftime('%d/%m/%Y')} to {week_end.strftime('%d/%m/%Y')}"
    
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # Generate report based on type
    if is_range:
        report_data, grand_total = _get_range_wage_data(start_date, end_date)
    else:
        report_data, grand_total = _get_weekly_wage_data(start_date)
    
    if not report_data:
        story.append(Paragraph("No wage data found for the specified period.", normal_style))
    else:
        # Add wage table
        wage_table = _create_wage_table(report_data, is_range)
        story.append(wage_table)
        
        # Add grand total
        story.append(Spacer(1, 20))
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=styles['Normal'],
            fontSize=14,
            alignment=TA_RIGHT,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(f"<b>Grand Total Wages: ₹{grand_total:,.2f}</b>", total_style))
    
    # Add footer
    story.append(Spacer(1, 30))
    story.extend(_add_footer(styles))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def _add_company_header(styles):
    """Add company header with XE Organics branding and logo"""
    header_elements = []
    
    # Try to load logo from media files
    logo_path = None
    possible_logo_paths = [
        os.path.join(settings.MEDIA_ROOT, 'logos', 'xe_logo.png'),
        os.path.join(settings.MEDIA_ROOT, 'logos', 'xe_logo.jpg'),
        os.path.join(settings.MEDIA_ROOT, 'logo.png'),
        os.path.join(settings.MEDIA_ROOT, 'logo.jpg'),
        os.path.join(settings.BASE_DIR, 'media', 'logos', 'xe_logo.png'),
        os.path.join(settings.BASE_DIR, 'static', 'images', 'xe_logo.png'),
    ]
    
    for path in possible_logo_paths:
        if os.path.exists(path):
            logo_path = path
            break
    
    # Create header table with logo and company info
    if logo_path:
        try:
            # Create logo image
            logo = Image(logo_path, width=40*mm, height=40*mm)
            
            # Company info
            company_info = Paragraph(
                "<b>XE Organics</b><br/>"
                "Sirumalai<br/>"
                "Dindigul - 624201<br/>"
                "Phone: +91 - 7871594753",
                ParagraphStyle(
                    'CompanyInfo',
                    parent=styles['Normal'],
                    fontSize=12,
                    alignment=TA_RIGHT,
                    fontName='Helvetica'
                )
            )
            
            # Create header table
            header_table = Table(
                [[logo, company_info]], 
                colWidths=[50*mm, 120*mm]
            )
            
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            
            header_elements.append(header_table)
            
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback to text-only header
            header_elements.extend(_add_text_only_header(styles))
    else:
        # Fallback to text-only header
        header_elements.extend(_add_text_only_header(styles))
    
    # Add separator line
    header_elements.append(Spacer(1, 10))
    line_table = Table([['_' * 80]], colWidths=[170*mm])
    line_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    header_elements.append(line_table)
    header_elements.append(Spacer(1, 10))
    
    return header_elements

def _add_text_only_header(styles):
    """Fallback text-only header"""
    header_elements = []
    
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=18,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=5
    )
    
    address_style = ParagraphStyle(
        'AddressStyle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    header_elements.append(Paragraph("<b>XE Organics</b>", company_style))
    header_elements.append(Paragraph(
        "Sirumalai, Dindigul - 624201<br/>"
        "Phone: +91 - 7871594753", 
        address_style
    ))
    
    return header_elements



def _get_weekly_wage_data(week_start_date):
    """Get weekly wage data for PDF generation"""
    week_dates = get_week_dates(week_start_date)
    week_end_date = week_dates[-1] if week_dates else week_start_date + timedelta(days=6)

    # Try to get optimized wage record first
    wage_record = WeeklyWagePayment.objects.filter(
        week_start_date=week_start_date
    ).first()

    employees_data = []
    grand_total = Decimal('0.00')

    if wage_record and wage_record.employee_wages:
        # Use optimized wage record
        try:
            employee_wages_list = wage_record.employee_wages
            # Ensure it's a list
            if not isinstance(employee_wages_list, list):
                employee_wages_list = []
            
            for emp_data in employee_wages_list:
                if not emp_data or not isinstance(emp_data, dict):
                    continue
                    
                try:
                    employee = Employee.objects.get(id=emp_data.get('employee_id'))
                    employee_name = employee.name
                except Employee.DoesNotExist:
                    employee_name = emp_data.get('employee_name', 'Unknown Employee')

                # Safely extract data with defaults
                present_days = int(emp_data.get('present_days', 0))
                half_days = int(emp_data.get('half_days', 0))
                daily_wage_value = emp_data.get('daily_wage', 0)
                net_amount_value = emp_data.get('net_amount', 0)
                
                # Convert to Decimal safely
                try:
                    daily_wage = Decimal(str(daily_wage_value)) if daily_wage_value else Decimal('0')
                    total_wage = Decimal(str(net_amount_value)) if net_amount_value else Decimal('0')
                except (ValueError, TypeError, InvalidOperation):
                    daily_wage = Decimal('0')
                    total_wage = Decimal('0')

                employee_wage_data = {
                    'employee_name': employee_name,
                    'present_days': present_days,
                    'half_days': half_days,
                    'absent_days': max(0, 7 - present_days - half_days),
                    'daily_wage': daily_wage,
                    'total_wage': total_wage,
                    'payment_status': emp_data.get('payment_status', 'pending'),
                    'attendance_details': emp_data.get('attendance_details', {})
                }
                employees_data.append(employee_wage_data)
                grand_total += total_wage
                
        except (TypeError, AttributeError) as e:
            print(f"Error processing wage record: {e}")
            # Fallback to building from attendance
            employees_data, grand_total = _build_wage_data_from_attendance(week_start_date, week_dates)
    else:
        # Fallback: Build from attendance records
        employees_data, grand_total = _build_wage_data_from_attendance(week_start_date, week_dates)

    # Always return safe values
    return employees_data or [], float(grand_total or 0)


def _get_range_wage_data(from_date, to_date):
    """Get wage data for a date range"""
    # Get all weeks that fall within the date range
    current_date = get_monday_of_week(from_date)
    end_date = get_monday_of_week(to_date)
    
    all_employees_data = []
    grand_total = Decimal('0.00')
    
    while current_date <= end_date:
        week_data, week_total = _get_weekly_wage_data(current_date)
        
        # Add week identifier to each employee record
        week_dates = get_week_dates(current_date)
        week_label = f"{current_date.strftime('%d/%m')} - {week_dates[-1].strftime('%d/%m/%Y')}"
        
        for emp_data in week_data:
            emp_data['week_period'] = week_label
            all_employees_data.append(emp_data)
        
        grand_total += Decimal(str(week_total))
        current_date += timedelta(days=7)
    
    return all_employees_data, float(grand_total)


def _build_wage_data_from_attendance(week_start_date, week_dates):
    """Build wage data from attendance records with enhanced error handling"""
    try:
        # Get attendance records for the week
        attendance_records = AttendanceRecord.objects.filter(date__in=week_dates)

        # Ensure attendance_data is iterable and safe
        attendance_lookup = {}
        for record in attendance_records:
            try:
                attendance_data = record.attendance_data
                if attendance_data and isinstance(attendance_data, list):
                    attendance_lookup[record.date] = attendance_data
                else:
                    attendance_lookup[record.date] = []
            except (AttributeError, TypeError):
                attendance_lookup[record.date] = []

        # Get all active employees
        employees = Employee.objects.filter(status=True)

        employees_data = []
        grand_total = Decimal('0.00')

        for employee in employees:
            try:
                emp_id = str(employee.id)

                # Safe wage retrieval
                daily_wage = Decimal('0')
                try:
                    # Try different approaches to get wage
                    if hasattr(Wage, 'get_current_wage'):
                        current_wage_result = Wage.get_current_wage(employee)
                        
                        if current_wage_result:
                            # Handle queryset
                            if hasattr(current_wage_result, 'first'):
                                wage_obj = current_wage_result.first()
                                if wage_obj and hasattr(wage_obj, 'amount'):
                                    daily_wage = Decimal(str(wage_obj.amount))
                            # Handle list
                            elif isinstance(current_wage_result, list) and len(current_wage_result) > 0:
                                wage_obj = current_wage_result[0]
                                if wage_obj and hasattr(wage_obj, 'amount'):
                                    daily_wage = Decimal(str(wage_obj.amount))
                            # Handle single object
                            elif hasattr(current_wage_result, 'amount'):
                                daily_wage = Decimal(str(current_wage_result.amount))
                    
                    # Fallback: try to get latest wage directly
                    if daily_wage == 0:
                        latest_wage = Wage.objects.filter(employee=employee).order_by('-created_at').first()
                        if latest_wage:
                            daily_wage = Decimal(str(latest_wage.amount))
                            
                except Exception as wage_error:
                    print(f"Wage retrieval error for {employee.name}: {wage_error}")
                    daily_wage = Decimal('0')

                if daily_wage <= 0:
                    continue  # Skip employees without valid wage rates

                employee_name = employee.name or f"Employee {emp_id}"
                present_days = 0
                half_days = 0
                attendance_details = {}

                # Process attendance for each day of the week
                for week_date in week_dates:
                    try:
                        date_str = week_date.isoformat()
                        employee_status = None

                        # Look for this employee's attendance on this date
                        for emp_attendance in attendance_lookup.get(week_date, []):
                            try:
                                if emp_attendance and str(emp_attendance.get('employee_id', '')) == emp_id:
                                    employee_status = emp_attendance.get('status')
                                    break
                            except (AttributeError, TypeError):
                                continue

                        attendance_details[date_str] = employee_status

                        # Count attendance
                        if employee_status == 1:  # Present
                            present_days += 1
                        elif employee_status == 2:  # Half day
                            half_days += 1
                        elif employee_status == 3:  # Late (treat as present)
                            present_days += 1
                            
                    except Exception as date_error:
                        print(f"Date processing error for {employee.name} on {week_date}: {date_error}")
                        continue

                # Calculate totals
                try:
                    total_wage = (present_days * daily_wage) + (half_days * daily_wage / 2)
                    absent_days = max(0, 7 - present_days - half_days)

                    employees_data.append({
                        'employee_name': employee_name,
                        'present_days': present_days,
                        'half_days': half_days,
                        'absent_days': absent_days,
                        'daily_wage': daily_wage,
                        'total_wage': total_wage,
                        'payment_status': 'pending',
                        'attendance_details': attendance_details
                    })

                    grand_total += total_wage
                    
                except Exception as calc_error:
                    print(f"Calculation error for {employee.name}: {calc_error}")
                    continue

            except Exception as emp_error:
                print(f"Employee processing error for {employee}: {emp_error}")
                continue

        return employees_data, grand_total
        
    except Exception as general_error:
        print(f"General error in _build_wage_data_from_attendance: {general_error}")
        return [], Decimal('0.00')


def _build_attendance_summary(attendance_details):
    """Build a summary string of attendance for the week"""
    if not attendance_details:
        return "No attendance data"
    
    status_map = {0: 'A', 1: 'P', 2: 'H', 3: 'L', None: '-'}
    summary_parts = []
    
    # Sort by date
    sorted_dates = sorted(attendance_details.keys())
    
    for date_str in sorted_dates:
        status = attendance_details[date_str]
        day_name = datetime.strptime(date_str, '%Y-%m-%d').strftime('%a')
        summary_parts.append(f"{day_name}:{status_map.get(status, '-')}")
    
    return " | ".join(summary_parts)


def _create_wage_table(employees_data, is_range=False):
    """Create wage table matching XE Organics styling"""
    
    if is_range:
        # For range reports, keep the original detailed format
        headers = [
            'S.No', 'Week Period', 'Employee Name', 'Present', 'Half Day', 
            'Absent', 'Daily Wage', 'Total Wage', 'Status'
        ]
        col_widths = [15*mm, 35*mm, 40*mm, 18*mm, 18*mm, 18*mm, 25*mm, 25*mm, 20*mm]
    else:
        # For weekly reports, use the XE Organics format
        headers = [
            'Name', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Days', 'Wages'
        ]
        col_widths = [40*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 20*mm, 25*mm]
    
    # Prepare table data
    table_data = [headers]
    
    for i, emp_data in enumerate(employees_data, 1):
        if is_range:
            # Range report format
            row = [
                str(i),
                emp_data.get('week_period', ''),
                emp_data['employee_name'],
                str(emp_data['present_days']),
                str(emp_data['half_days']),
                str(emp_data['absent_days']),
                f"₹{emp_data['daily_wage']:,.0f}",
                f"₹{emp_data['total_wage']:,.0f}",
                emp_data['payment_status'].title()
            ]
        else:
            # Weekly report format - XE Organics style
            attendance_grid = _parse_attendance_to_grid(emp_data.get('attendance_details', {}))
            
            row = [
                emp_data['employee_name'],
                attendance_grid['Mon'],
                attendance_grid['Tue'],
                attendance_grid['Wed'],
                attendance_grid['Thu'],
                attendance_grid['Fri'],
                attendance_grid['Sat'],
                attendance_grid['Sun'],
                str(emp_data['present_days']),
                str(int(emp_data['total_wage']))  # Remove decimals and currency symbol
            ]
        table_data.append(row)
    
    # Create table
    table = Table(table_data, colWidths=col_widths)
    
    # Apply XE Organics table style
    if is_range:
        # Style for range reports
        table_style = _get_range_table_style()
    else:
        # Style for weekly reports - matching XE Organics design
        table_style = _get_xe_organics_table_style(employees_data)
    
    table.setStyle(table_style)
    return table


def _get_xe_organics_table_style(employees_data):
    """Get table style matching XE Organics design"""
    
    table_style = TableStyle([
        # Header style - light gray background
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E0E0E0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Data rows style
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        
        # Grid lines - black borders
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Employee name column - left aligned
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        
        # Attendance columns - center aligned
        ('ALIGN', (1, 0), (7, -1), 'CENTER'),
        
        # Days and Wages columns - center aligned
        ('ALIGN', (8, 0), (-1, -1), 'CENTER'),
        
        # Padding
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        
        # White background for all data cells
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ])
    
    # Apply conditional formatting for attendance status
    for row_idx, emp_data in enumerate(employees_data, 1):
        attendance_grid = _parse_attendance_to_grid(emp_data.get('attendance_details', {}))
        
        for col_idx, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 1):
            cell_value = attendance_grid[day]
            
            if cell_value == '1':
                # Present - green background
                table_style.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#90EE90'))
                table_style.add('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#006400'))
            elif cell_value == '0':
                # Absent - red background
                table_style.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#FFB6C1'))
                table_style.add('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#8B0000'))
            elif cell_value == '0.5':
                # Half day - yellow background
                table_style.add('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#FFFFE0'))
                table_style.add('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#B8860B'))
    
    return table_style


def _get_range_table_style():
    """Get table style for range reports"""
    return TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E0E0E0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        
        # Data rows style
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F8F8')]),
        
        # Grid lines
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Align specific columns
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # S.No
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # Employee name
        ('ALIGN', (-3, 1), (-1, -1), 'RIGHT'), # Wage columns
        
        # Padding
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])


def _create_total_row_table(grand_total):
    """Create total row table matching XE Organics style"""
    
    total_data = [['Total', '', '', '', '', '', '', '', '', str(int(grand_total))]]
    
    total_table = Table(total_data, colWidths=[40*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 18*mm, 20*mm, 25*mm])
    
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E0E0E0')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    return total_table


def _parse_attendance_to_grid(attendance_details):
    """Convert attendance details to day-wise grid format"""
    # Initialize grid with default values
    grid = {
        'Mon': '0', 'Tue': '0', 'Wed': '0', 'Thu': '0',
        'Fri': '0', 'Sat': '0', 'Sun': '0'
    }
    
    # Status mapping: 1=Present (1), 0=Absent (0), 2=Half day (0.5), 3=Late (1)
    status_display = {0: '0', 1: '1', 2: '0.5', 3: '1', None: '0'}
    
    if not attendance_details:
        return grid
    
    # Parse attendance details and map to days
    for date_str, status in attendance_details.items():
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            day_name = date_obj.strftime('%a')  # Mon, Tue, etc.
            
            # Map day abbreviations to full names
            day_mapping = {
                'Mon': 'Mon', 'Tue': 'Tue', 'Wed': 'Wed', 'Thu': 'Thu',
                'Fri': 'Fri', 'Sat': 'Sat', 'Sun': 'Sun'
            }
            
            if day_name in day_mapping:
                grid[day_mapping[day_name]] = status_display.get(status, '0')
                
        except (ValueError, AttributeError):
            continue
    
    return grid




def _add_footer(styles):
    """Add footer matching XE Organics style"""
    footer_elements = []
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_LEFT,
        textColor=colors.black
    )
    
    # Add generation timestamp
    generation_time = timezone.now().strftime('%d %b %Y %H:%M')
    footer_elements.append(Paragraph(f"Generated on: {generation_time}", footer_style))
    
    return footer_elements



# Additional utility functions for better PDF formatting

@api_view(['GET'])
def download_weekly_wage_summary_pdf(request):
    """Generate a summary PDF with weekly totals"""
    weeks_count = request.query_params.get('weeks', 4)  # Default to 4 weeks
    
    try:
        weeks_count = int(weeks_count)
        if weeks_count < 1 or weeks_count > 52:
            weeks_count = 4
    except (ValueError, TypeError):
        weeks_count = 4
    
    try:
        # Get last N weeks of data
        end_date = date.today()
        start_date = get_monday_of_week(end_date) - timedelta(weeks=(weeks_count-1))
        
        pdf_buffer = _generate_summary_pdf(start_date, weeks_count)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="wage_summary_{weeks_count}_weeks.pdf"'
        
        return response
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate summary PDF: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _generate_summary_pdf(start_date, weeks_count):
    """Generate summary PDF with weekly totals"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Add header
    story.extend(_add_company_header(styles))
    
    # Title
    title_style = ParagraphStyle(
        'SummaryTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    story.append(Paragraph(f"Weekly Wage Summary Report<br/>Last {weeks_count} Weeks", title_style))
    story.append(Spacer(1, 20))
    
    # Collect weekly summaries
    weekly_summaries = []
    current_week = start_date
    total_wages_all_weeks = Decimal('0.00')
    
    for week_num in range(weeks_count):
        week_data, week_total = _get_weekly_wage_data(current_week)
        week_dates = get_week_dates(current_week)
        
        week_summary = {
            'week_number': week_num + 1,
            'week_period': f"{current_week.strftime('%d/%m')} - {week_dates[-1].strftime('%d/%m/%Y')}",
            'total_employees': len(week_data),
            'total_wages': Decimal(str(week_total))
        }
        
        weekly_summaries.append(week_summary)
        total_wages_all_weeks += week_summary['total_wages']
        current_week += timedelta(days=7)
    
    # Create summary table
    summary_headers = ['Week #', 'Week Period', 'Employees', 'Total Wages']
    summary_data = [summary_headers]
    
    for summary in weekly_summaries:
        summary_data.append([
            str(summary['week_number']),
            summary['week_period'],
            str(summary['total_employees']),
            f"₹{summary['total_wages']:,.2f}"
        ])
    
    # Add total row
    summary_data.append([
        'TOTAL',
        f'{weeks_count} Weeks',
        '',
        f"₹{total_wages_all_weeks:,.2f}"
    ])
    
    # Create and style summary table
    summary_table = Table(summary_data, colWidths=[30*mm, 50*mm, 30*mm, 40*mm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 30))
    story.extend(_add_footer(styles))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


@api_view(['GET'])
def download_employee_wage_detail_pdf(request):
    """Generate detailed PDF for a specific employee across multiple weeks"""
    employee_id = request.query_params.get('employee_id')
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    
    if not all([employee_id, from_date, to_date]):
        return Response(
            {'error': 'employee_id, from_date, and to_date are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        employee = Employee.objects.get(id=employee_id, status=True)
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    except (Employee.DoesNotExist, ValueError):
        return Response(
            {'error': 'Invalid employee_id or date format'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        pdf_buffer = _generate_employee_detail_pdf(employee, from_date, to_date)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        filename = f"employee_wage_detail_{employee.name.replace(' ', '_')}_{from_date}_to_{to_date}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate employee detail PDF: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _generate_employee_detail_pdf(employee, from_date, to_date):
    """Generate detailed PDF for specific employee"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Add header
    story.extend(_add_company_header(styles))
    
    # Employee details title
    title_style = ParagraphStyle(
        'EmployeeTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    story.append(Paragraph(
        f"Employee Wage Detail Report<br/>"
        f"Employee: {employee.name}<br/>"
        f"Period: {from_date.strftime('%d/%m/%Y')} to {to_date.strftime('%d/%m/%Y')}", 
        title_style
    ))
    story.append(Spacer(1, 20))
    
    # Get employee wage data for the period
    employee_weekly_data = _get_employee_weekly_data(employee, from_date, to_date)
    
    if not employee_weekly_data:
        story.append(Paragraph("No wage data found for this employee in the specified period.", styles['Normal']))
    else:
        # Create detailed table
        detail_table = _create_employee_detail_table(employee_weekly_data)
        story.append(detail_table)
        
        # Add totals
        total_wages = sum(week['total_wage'] for week in employee_weekly_data)
        total_paid = sum(week['paid_amount'] for week in employee_weekly_data)
        
        story.append(Spacer(1, 20))
        total_style = ParagraphStyle(
            'TotalStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_RIGHT,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph(f"<b>Total Wages Earned: ₹{total_wages:,.2f}</b>", total_style))
        story.append(Paragraph(f"<b>Total Amount Paid: ₹{total_paid:,.2f}</b>", total_style))
        story.append(Paragraph(f"<b>Remaining Balance: ₹{total_wages - total_paid:,.2f}</b>", total_style))
    
    story.append(Spacer(1, 30))
    story.extend(_add_footer(styles))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def _get_employee_weekly_data(employee, from_date, to_date):
    """Get weekly wage data for a specific employee"""
    weekly_data = []
    current_week = get_monday_of_week(from_date)
    end_week = get_monday_of_week(to_date)
    
    while current_week <= end_week:
        # Check for wage record
        wage_record = WeeklyWagePayment.objects.filter(
            week_start_date=current_week
        ).first()
        
        if wage_record:
            emp_data = wage_record.get_employee_wage_data(str(employee.id))
            
            if emp_data:
                week_dates = get_week_dates(current_week)
                attendance_summary = _build_attendance_summary(emp_data.get('attendance_details', {}))
                
                weekly_data.append({
                    'week_period': f"{current_week.strftime('%d/%m')} - {week_dates[-1].strftime('%d/%m/%Y')}",
                    'present_days': emp_data.get('present_days', 0),
                    'half_days': emp_data.get('half_days', 0),
                    'absent_days': 7 - emp_data.get('present_days', 0) - emp_data.get('half_days', 0),
                    'daily_wage': Decimal(str(emp_data.get('daily_wage', 0))),
                    'total_wage': Decimal(str(emp_data.get('net_amount', 0))),
                    'paid_amount': Decimal(str(emp_data.get('paid_amount', 0))),
                    'payment_status': emp_data.get('payment_status', 'pending'),
                    'attendance_summary': attendance_summary
                })
        else:
            # Build from attendance records if no wage record exists
            week_dates = get_week_dates(current_week)
            attendance_records = AttendanceRecord.objects.filter(date__in=week_dates)
            
            present_days = 0
            half_days = 0
            attendance_details = {}
            
            # Safe wage retrieval
            try:
                current_wage = Wage.get_current_wage(employee)
                if hasattr(current_wage, '__iter__') and not isinstance(current_wage, str):
                    # It's a queryset or list
                    if current_wage.exists() if hasattr(current_wage, 'exists') else len(current_wage) > 0:
                        daily_wage = current_wage.first().amount if hasattr(current_wage, 'first') else current_wage[0].amount
                    else:
                        daily_wage = Decimal('0')
                elif current_wage:
                    # It's a single object
                    daily_wage = current_wage.amount if hasattr(current_wage, 'amount') else Decimal('0')
                else:
                    daily_wage = Decimal('0')
            except (IndexError, AttributeError, TypeError) as e:
                print(f"Error getting wage for employee {employee.name}: {e}")
                daily_wage = Decimal('0')
            
            for week_date in week_dates:
                date_str = week_date.isoformat()
                employee_status = None
                
                # Find attendance for this date
                for record in attendance_records:
                    if record.date == week_date:
                        for emp_data in record.attendance_data or []:
                            if str(emp_data.get('employee_id')) == str(employee.id):
                                employee_status = emp_data.get('status')
                                break
                        break
                
                attendance_details[date_str] = employee_status
                
                if employee_status == 1:  # Present
                    present_days += 1
                elif employee_status == 2:  # Half day
                    half_days += 1
                elif employee_status == 3:  # Late (treat as present)
                    present_days += 1
            
            if daily_wage > 0:  # Only include weeks with wage data
                total_wage = (present_days * daily_wage) + (half_days * daily_wage / 2)
                attendance_summary = _build_attendance_summary(attendance_details)
                
                weekly_data.append({
                    'week_period': f"{current_week.strftime('%d/%m')} - {week_dates[-1].strftime('%d/%m/%Y')}",
                    'present_days': present_days,
                    'half_days': half_days,
                    'absent_days': 7 - present_days - half_days,
                    'daily_wage': daily_wage,
                    'total_wage': total_wage,
                    'paid_amount': Decimal('0'),
                    'payment_status': 'pending',
                    'attendance_summary': attendance_summary
                })
        
        current_week += timedelta(days=7)
    
    return weekly_data


def _create_employee_detail_table(weekly_data):
    """Create detailed table for employee wage report"""
    headers = [
        'Week Period', 'Present', 'Half Day', 'Absent', 
        'Daily Wage', 'Total Wage', 'Paid', 'Balance', 'Status'
    ]
    
    col_widths = [40*mm, 20*mm, 20*mm, 20*mm, 25*mm, 25*mm, 25*mm, 25*mm, 25*mm]
    
    table_data = [headers]
    
    for week_data in weekly_data:
        balance = week_data['total_wage'] - week_data['paid_amount']
        row = [
            week_data['week_period'],
            str(week_data['present_days']),
            str(week_data['half_days']),
            str(week_data['absent_days']),
            f"₹{week_data['daily_wage']:,.2f}",
            f"₹{week_data['total_wage']:,.2f}",
            f"₹{week_data['paid_amount']:,.2f}",
            f"₹{balance:,.2f}",
            week_data['payment_status'].title()
        ]
        table_data.append(row)
    
    table = Table(table_data, colWidths=col_widths)
    
    table_style = TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        
        # Align wage columns to right
        ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
        
        # Grid and padding
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])
    
    table.setStyle(table_style)
    return table


@api_view(['GET'])
def download_attendance_register_pdf(request):
    """Generate attendance register PDF (daily attendance view)"""
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
    
    try:
        pdf_buffer = _generate_attendance_register_pdf(from_date, to_date)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="attendance_register_{from_date}_to_{to_date}.pdf"'
        
        return response
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate attendance register PDF: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _generate_attendance_register_pdf(from_date, to_date):
    """Generate attendance register PDF showing daily attendance"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,  # Use letter size for wider table
        rightMargin=15*mm, 
        leftMargin=15*mm, 
        topMargin=20*mm, 
        bottomMargin=20*mm
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Add header
    story.extend(_add_company_header(styles))
    
    # Title
    title_style = ParagraphStyle(
        'RegisterTitle',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    story.append(Paragraph(
        f"Daily Attendance Register<br/>"
        f"From: {from_date.strftime('%d/%m/%Y')} To: {to_date.strftime('%d/%m/%Y')}", 
        title_style
    ))
    story.append(Spacer(1, 20))
    
    # Get attendance data
    date_range = []
    current_date = from_date
    while current_date <= to_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    # Get all employees
    employees = Employee.objects.filter(status=True).order_by('name')
    
    # Get attendance records
    attendance_records = AttendanceRecord.objects.filter(
        date__in=date_range
    )
    
    # Create attendance lookup
    attendance_lookup = {}
    for record in attendance_records:
        if record.attendance_data:  # Ensure attendance_data exists
            attendance_lookup[record.date] = {
                str(emp_data['employee_id']): emp_data['status'] 
                for emp_data in record.attendance_data
                if emp_data and 'employee_id' in emp_data  # Additional safety check
            }
    
    # Build table data
    headers = ['S.No', 'Employee Name']
    
    # Add date columns (limit to reasonable number of columns)
    max_days = 15  # Limit to 15 days for readability
    display_dates = date_range[:max_days] if len(date_range) > max_days else date_range
    
    for date_obj in display_dates:
        headers.append(date_obj.strftime('%d/%m'))
    
    headers.extend(['Present', 'Half Day', 'Absent', 'Daily Wage', 'Total Wage'])
    
    table_data = [headers]
    
    total_wages_all = Decimal('0.00')
    
    for i, employee in enumerate(employees, 1):
        # Safe wage retrieval
        try:
            current_wage = Wage.get_current_wage(employee)
            if hasattr(current_wage, '__iter__') and not isinstance(current_wage, str):
                # It's a queryset or list
                if current_wage.exists() if hasattr(current_wage, 'exists') else len(current_wage) > 0:
                    daily_wage = current_wage.first().amount if hasattr(current_wage, 'first') else current_wage[0].amount
                else:
                    daily_wage = Decimal('0')
            elif current_wage:
                # It's a single object
                daily_wage = current_wage.amount if hasattr(current_wage, 'amount') else Decimal('0')
            else:
                daily_wage = Decimal('0')
        except (IndexError, AttributeError, TypeError) as e:
            print(f"Error getting wage for employee {employee.name}: {e}")
            daily_wage = Decimal('0')
        
        if daily_wage == 0:
            continue
        
        row = [str(i), employee.name]
        
        present_count = 0
        half_day_count = 0
        absent_count = 0
        
        # Add attendance status for each date
        for date_obj in display_dates:
            if date_obj in attendance_lookup:
                emp_status = attendance_lookup[date_obj].get(str(employee.id))
                if emp_status == 1:
                    row.append('P')
                    present_count += 1
                elif emp_status == 2:
                    row.append('H')
                    half_day_count += 1
                elif emp_status == 3:
                    row.append('L')
                    present_count += 1  # Late counts as present
                else:
                    row.append('A')
                    absent_count += 1
            else:
                row.append('-')
                absent_count += 1
        
        # Calculate total wage for displayed period
        total_wage = (present_count * daily_wage) + (half_day_count * daily_wage / 2)
        total_wages_all += total_wage
        
        # Add summary columns
        row.extend([
            str(present_count),
            str(half_day_count),
            str(absent_count),
            f"₹{daily_wage:,.0f}",
            f"₹{total_wage:,.2f}"
        ])
        
        table_data.append(row)
    
    # Add total row
    total_row = ['', 'TOTAL'] + [''] * len(display_dates) + ['', '', '', '', f"₹{total_wages_all:,.2f}"]
    table_data.append(total_row)
    
    # Create table with dynamic column widths
    base_width = 15*mm
    name_width = 35*mm
    date_col_width = max(12*mm, (letter[0] - 30*mm - name_width - 4*base_width) / len(display_dates))
    
    col_widths = [base_width, name_width] + [date_col_width] * len(display_dates) + [base_width] * 5
    
    table = Table(table_data, colWidths=col_widths)
    
    # Apply comprehensive table styling
    table_style = TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 7),
        ('ALIGN', (0, 1), (-1, -2), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
        
        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 8),
        
        # Grid and borders
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        
        # Employee name alignment
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        
        # Wage columns alignment
        ('ALIGN', (-2, 1), (-1, -1), 'RIGHT'),
    ])
    
    table.setStyle(table_style)
    story.append(table)
    
    # Add legend
    story.append(Spacer(1, 15))
    legend_style = ParagraphStyle(
        'LegendStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_LEFT
    )
    
    story.append(Paragraph(
        "<b>Legend:</b> P = Present, A = Absent, H = Half Day, L = Late, - = No Record", 
        legend_style
    ))
    
    if len(date_range) > max_days:
        story.append(Paragraph(
            f"<b>Note:</b> Showing first {max_days} days only. Total period: {len(date_range)} days", 
            legend_style
        ))
    
    story.append(Spacer(1, 20))
    story.extend(_add_footer(styles))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

@api_view(['GET'])
def download_payroll_summary_pdf(request):
    """Generate comprehensive payroll summary PDF"""
    month = request.query_params.get('month')  # Format: YYYY-MM
    year = request.query_params.get('year')    # Format: YYYY
    
    if month:
        try:
            year_month = datetime.strptime(month, '%Y-%m')
            start_date = year_month.date()
            # Get last day of month
            if start_date.month == 12:
                end_date = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
        except ValueError:
            return Response({'error': 'Invalid month format. Use YYYY-MM'}, status=400)
    
    elif year:
        try:
            year_int = int(year)
            start_date = date(year_int, 1, 1)
            end_date = date(year_int, 12, 31)
        except ValueError:
            return Response({'error': 'Invalid year format. Use YYYY'}, status=400)
    
    else:
        # Default to current month
        today = date.today()
        start_date = today.replace(day=1)
        if start_date.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
    
    try:
        pdf_buffer = _generate_payroll_summary_pdf(start_date, end_date)
        
        period_str = f"{start_date.strftime('%Y-%m')}" if month else f"{start_date.year}"
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payroll_summary_{period_str}.pdf"'
        
        return response
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate payroll summary PDF: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _generate_payroll_summary_pdf(start_date, end_date):
    """Generate comprehensive payroll summary"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Add header
    story.extend(_add_company_header(styles))
    
    # Title
    title_style = ParagraphStyle(
        'PayrollTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    period_type = "Monthly" if (end_date - start_date).days <= 31 else "Annual"
    story.append(Paragraph(
        f"{period_type} Payroll Summary<br/>"
        f"Period: {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}", 
        title_style
    ))
    story.append(Spacer(1, 20))
    
    # Get all wage records in the period
    all_mondays = []
    current_monday = get_monday_of_week(start_date)
    end_monday = get_monday_of_week(end_date)
    
    while current_monday <= end_monday:
        all_mondays.append(current_monday)
        current_monday += timedelta(days=7)
    
    # Collect payroll data
    payroll_data = []
    total_gross_wages = Decimal('0.00')
    total_paid_wages = Decimal('0.00')
    total_pending_wages = Decimal('0.00')
    
    for monday in all_mondays:
        wage_record = WeeklyWagePayment.objects.filter(week_start_date=monday).first()
        
        if wage_record:
            week_dates = get_week_dates(monday)
            payroll_data.append({
                'week_period': f"{monday.strftime('%d/%m')} - {week_dates[-1].strftime('%d/%m/%Y')}",
                'total_employees': wage_record.total_employees,
                'gross_wages': wage_record.total_gross_amount,
                'paid_wages': wage_record.total_paid_amount,
                'pending_wages': wage_record.total_remaining_amount,
                'payment_status': wage_record.payment_status
            })
            
            total_gross_wages += wage_record.total_gross_amount
            total_paid_wages += wage_record.total_paid_amount
            total_pending_wages += wage_record.total_remaining_amount
    
    if not payroll_data:
        story.append(Paragraph("No payroll data found for the specified period.", styles['Normal']))
    else:
        # Create payroll summary table
        payroll_table = _create_payroll_summary_table(payroll_data)
        story.append(payroll_table)
        
        # Add totals section
        story.append(Spacer(1, 20))
        
        totals_data = [
            ['Total Gross Wages:', f"₹{total_gross_wages:,.2f}"],
            ['Total Paid Wages:', f"₹{total_paid_wages:,.2f}"],
            ['Total Pending Wages:', f"₹{total_pending_wages:,.2f}"],
            ['Payment Completion:', f"{(total_paid_wages/total_gross_wages*100) if total_gross_wages > 0 else 0:.1f}%"]
        ]
        
        totals_table = Table(totals_data, colWidths=[60*mm, 40*mm])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(totals_table)
    
    story.append(Spacer(1, 30))
    story.extend(_add_footer(styles))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def _create_payroll_summary_table(payroll_data):
    """Create payroll summary table"""
    headers = ['Week Period', 'Employees', 'Gross Wages', 'Paid Wages', 'Pending Wages', 'Status']
    
    table_data = [headers]
    
    for data in payroll_data:
        row = [
            data['week_period'],
            str(data['total_employees']),
            f"₹{data['gross_wages']:,.2f}",
            f"₹{data['paid_wages']:,.2f}",
            f"₹{data['pending_wages']:,.2f}",
            data['payment_status'].title()
        ]
        table_data.append(row)
    
    table = Table(table_data, colWidths=[40*mm, 25*mm, 30*mm, 30*mm, 30*mm, 25*mm])
    
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        
        # Wage columns - right align
        ('ALIGN', (2, 1), (4, -1), 'RIGHT'),
        
        # Grid and borders
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    return table