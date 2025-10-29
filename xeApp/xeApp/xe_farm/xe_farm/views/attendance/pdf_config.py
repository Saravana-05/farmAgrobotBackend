# Configuration file for PDF generation settings - XE Organics Style
from reportlab.lib import colors
from reportlab.lib.colors import Color

# Custom Colors matching XE Organics branding
CUSTOM_COLORS = {
    'xe_green': Color(0.2, 0.7, 0.2),  # XE Organics green
    'xe_yellow': Color(1, 0.9, 0),     # XE Organics yellow
    'light_gray': Color(0.95, 0.95, 0.95),
    'dark_gray': Color(0.3, 0.3, 0.3),
    'present_green': Color(0, 0.8, 0),  # For attendance "1"
    'absent_red': Color(0.8, 0, 0),     # For attendance "0"
}

# Company Information
COMPANY_INFO = {
    'name': 'XE Organics',
    'address': 'Sirumalai\nDindigul - 624201',
    'phone': 'Phone: +91 - 7871594753',
    'email': 'info@xeorganics.com',
    'website': 'www.xeorganics.com'
}

# PDF Styling Configuration
PDF_STYLES = {
    'company_name': {
        'fontSize': 20,
        'textColor': colors.black,
        'fontName': 'Helvetica-Bold',
        'alignment': 'RIGHT'  # Right align company name
    },
    'address': {
        'fontSize': 10,
        'textColor': colors.black,
        'fontName': 'Helvetica',
        'alignment': 'RIGHT'  # Right align address
    },
    'title': {
        'fontSize': 16,
        'textColor': colors.black,
        'fontName': 'Helvetica-Bold',
        'alignment': 'CENTER'  # Center align title
    },
    'date_range': {
        'fontSize': 12,
        'textColor': colors.black,
        'fontName': 'Helvetica',
        'alignment': 'CENTER'  # Center align date range
    },
    'table_header': {
        'fontSize': 10,
        'backgroundColor': colors.white,
        'textColor': colors.black,
        'fontName': 'Helvetica-Bold',
        'border': True,
        'borderColor': colors.black,
        'borderWidth': 1
    },
    'table_data': {
        'fontSize': 9,
        'fontName': 'Helvetica',
        'textColor': colors.black,
        'border': True,
        'borderColor': colors.black,
        'borderWidth': 0.5
    },
    'table_data_present': {
        'fontSize': 9,
        'fontName': 'Helvetica-Bold',
        'textColor': CUSTOM_COLORS['present_green']
    },
    'table_data_absent': {
        'fontSize': 9,
        'fontName': 'Helvetica-Bold',
        'textColor': CUSTOM_COLORS['absent_red']
    },
    'footer': {
        'fontSize': 8,
        'textColor': colors.grey,
        'fontName': 'Helvetica',
        'alignment': 'LEFT'
    },
    'totals': {
        'fontSize': 11,
        'textColor': colors.black,
        'fontName': 'Helvetica-Bold',
        'backgroundColor': colors.white
    }
}

# Table Configuration
TABLE_CONFIG = {
    'max_days_attendance_register': 15,
    'row_colors': [colors.white, colors.white],  # All rows white like in image
    'grid_color': colors.black,
    'grid_width': 1,  # Thicker grid lines
    'header_background': colors.white,
    'total_row_background': colors.white,
    'name_column_width': 80,  # Wider name column
    'day_column_width': 35,   # Consistent day column width
    'wages_column_width': 60,  # Wages column width
    'padding': {
        'top': 8,
        'bottom': 8,
        'left': 8,
        'right': 8
    },
    'cell_alignment': 'CENTER',  # Center align all table content
    'border_style': 'GRID'  # Full grid borders
}

# Logo Configuration
LOGO_CONFIG = {
    'enabled': True,
    'path': 'media/xe_logo.png',  # Path to your logo file
    'width': 60,    # Logo width in points
    'height': 60,   # Logo height in points
    'x_position': 50,  # X position from left margin
    'y_position': 750, # Y position from bottom (adjust based on page size)
    'maintain_aspect_ratio': True,
    'fallback_text': 'XE',  # Fallback text if logo not found
    'fallback_style': {
        'fontSize': 24,
        'fontName': 'Helvetica-Bold',
        'textColor': CUSTOM_COLORS['xe_green'],
        'backgroundColor': CUSTOM_COLORS['xe_yellow'],
        'border': True,
        'borderRadius': 5
    }
}

# Tamil Font Configuration (if available)
TAMIL_FONT_CONFIG = {
    'font_name': 'Tamil',
    'font_path': 'static/fonts/tamil-font.ttf',
    'use_tamil_font': False
}

# Currency and Locale Settings
CURRENCY_CONFIG = {
    'symbol': '₹',
    'decimal_places': 0,  # No decimals for wages as shown in image
    'thousands_separator': '',  # No thousands separator in image
    'position': 'suffix'  # Currency symbol after number (if needed)
}

# Page Layout Settings
PAGE_CONFIG = {
    'pagesize': 'A4',
    'margins': {
        'top': 25,
        'bottom': 25,
        'left': 25,
        'right': 25
    },
    'header_height': 100,  # Space for logo and company info
    'footer_height': 30,   # Space for generated timestamp
    'content_start_y': 650  # Where main content starts
}

# Report Configuration
REPORT_CONFIG = {
    'show_employee_id': False,
    'show_payment_mode': False,  # Not shown in the image
    'show_attendance_details': True,
    'date_format': '%d %b %Y',  # Format like "18 Aug 2025"
    'time_format': '%H:%M',     # 24-hour format
    'week_start_day': 'monday',
    'max_rows_per_page': 25,
    'show_page_numbers': False,  # Not visible in image
    'watermark_text': None,
    'show_total_row': True,      # Show total row like in image
    'total_row_label': 'Total',  # Label for total row
    'generated_timestamp_format': 'Generated on: %d %b %Y %H:%M',
    'report_types': {
        'weekly_wage': {
            'filename_prefix': 'weekly_wages_xe_organics',
            'title': 'Weekly Wages Report'
        },
        'wage_range': {
            'filename_prefix': 'wage_report_xe_organics',
            'title': 'Employee Wage Report'
        },
        'attendance_register': {
            'filename_prefix': 'attendance_register_xe_organics',
            'title': 'Daily Attendance Register'
        },
        'payroll_summary': {
            'filename_prefix': 'payroll_summary_xe_organics',
            'title': 'Payroll Summary Report'
        },
        'employee_detail': {
            'filename_prefix': 'employee_wage_detail_xe_organics',
            'title': 'Employee Wage Detail Report'
        }
    }
}

# Attendance Status Configuration
ATTENDANCE_STATUS = {
    0: {
        'label': 'Absent', 
        'short': '0', 
        'color': CUSTOM_COLORS['absent_red'],
        'style': 'table_data_absent'
    },
    1: {
        'label': 'Present', 
        'short': '1', 
        'color': CUSTOM_COLORS['present_green'],
        'style': 'table_data_present'
    },
    2: {
        'label': 'Half Day', 
        'short': 'H', 
        'color': colors.orange,
        'style': 'table_data'
    },
    3: {
        'label': 'Late', 
        'short': 'L', 
        'color': colors.darkorange,
        'style': 'table_data'
    },
    None: {
        'label': 'No Record', 
        'short': '-', 
        'color': colors.grey,
        'style': 'table_data'
    }
}

# Payment Status Configuration
PAYMENT_STATUS = {
    'pending': {'label': 'Pending', 'color': colors.orange},
    'partial': {'label': 'Partial', 'color': colors.yellow},
    'paid': {'label': 'Paid', 'color': colors.green},
    'cancelled': {'label': 'Cancelled', 'color': colors.red}
}

# PDF Generation Settings
PDF_GENERATION = {
    'buffer_size': 8192,
    'compression': True,
    'author': 'XE Organics Farm Management System',
    'subject': 'Farm Wage and Attendance Report - XE Organics',
    'creator': 'XE Organics Django System',
    'title_template': 'XE Organics - {report_type} - {date_range}',
    'filename_timestamp_format': '%Y%m%d_%H%M%S',
    'metadata': {
        'Producer': 'XE Organics Management System',
        'Keywords': 'wages, attendance, farm, organics'
    }
}

# Header Layout Configuration
HEADER_LAYOUT = {
    'logo_section': {
        'width': 100,  # Width for logo section
        'alignment': 'LEFT'
    },
    'company_section': {
        'width': 400,  # Width for company info section
        'alignment': 'RIGHT'
    },
    'spacing': {
        'after_header': 30,  # Space after header before title
        'after_title': 20,   # Space after title before table
        'before_footer': 20  # Space before footer
    }
}

# Table Column Configuration for Weekly Wages Report
WEEKLY_REPORT_COLUMNS = {
    'Name': {'width': 80, 'alignment': 'LEFT'},
    'Mon': {'width': 35, 'alignment': 'CENTER'},
    'Tue': {'width': 35, 'alignment': 'CENTER'},
    'Wed': {'width': 35, 'alignment': 'CENTER'},
    'Thu': {'width': 35, 'alignment': 'CENTER'},
    'Fri': {'width': 35, 'alignment': 'CENTER'},
    'Sat': {'width': 35, 'alignment': 'CENTER'},
    'Sun': {'width': 35, 'alignment': 'CENTER'},
    'Days': {'width': 40, 'alignment': 'CENTER'},
    'Wages': {'width': 60, 'alignment': 'CENTER'}
}

# Export Configuration
EXPORT_CONFIG = {
    'default_content_type': 'application/pdf',
    'default_file_extension': '.pdf',
    'max_file_size_mb': 50,
    'cache_duration_hours': 24,
    'allow_inline_viewing': True,
    'force_download': False,
    'filename_format': 'XE_Organics_{report_type}_{timestamp}'
}

# Color scheme for different report types
REPORT_COLOR_SCHEMES = {
    'weekly_wage': {
        'primary': colors.black,
        'secondary': colors.grey,
        'accent': CUSTOM_COLORS['xe_green']
    },
    'attendance': {
        'primary': colors.black,
        'secondary': colors.grey,
        'present': CUSTOM_COLORS['present_green'],
        'absent': CUSTOM_COLORS['absent_red']
    }
}