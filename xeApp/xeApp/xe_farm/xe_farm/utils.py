from datetime import date, timedelta
import os
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
import io
import logging
from .models import Employee, Wage

logger = logging.getLogger(__name__)

def get_default_avatar_local():
    """
    Generate default avatar image and return as ContentFile for Django storage
    """
    try:
        logger.info("Generating default avatar for local storage")
        
        # Create a simple default avatar
        img = Image.new('RGB', (200, 200), color='#E5E7EB')  # Light gray
        
        # Convert to bytes
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        
        # Create ContentFile for Django storage
        content_file = ContentFile(img_io.getvalue(), name='default_avatar.jpg')
        
        logger.info(f"Default avatar generated. Size: {len(img_io.getvalue())} bytes")
        
        return content_file
        
    except Exception as e:
        logger.error(f"Failed to generate default avatar: {str(e)}", exc_info=True)
        raise Exception(f"Failed to generate default avatar: {str(e)}")

def get_image_url(image_field):
    """
    Get the URL for an image field
    """
    if image_field:
        return image_field.url
    return None

def get_default_expense_image_local():
    """
    Get default expense image content for local storage
    You can customize this function based on your needs
    """
    try:
        # Option 1: Return a default image file from static files
        default_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'default_expense.jpg')
        
        if os.path.exists(default_image_path):
            with open(default_image_path, 'rb') as f:
                return ContentFile(f.read(), name='default_expense.jpg')
        
        # Option 2: Create a simple colored rectangle as default image
        # This requires Pillow (PIL) library: pip install Pillow
        try:
            from PIL import Image, ImageDraw, ImageFont
            import io
            
            # Create a simple default image
            img = Image.new('RGB', (400, 300), color='#f0f0f0')
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                # Try to use a default font
                font = ImageFont.load_default()
            except:
                font = None
            
            text = "Default\nExpense Image"
            
            # Get text bounding box
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the text
            x = (400 - text_width) // 2
            y = (300 - text_height) // 2
            
            draw.text((x, y), text, fill='#666666', font=font)
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr.seek(0)
            
            return ContentFile(img_byte_arr.read(), name='default_expense.jpg')
            
        except ImportError:
            logger.warning("Pillow not installed, cannot create default image")
            return None
        
    except Exception as e:
        logger.error(f"Error creating default expense image: {str(e)}")
        return None
    
def get_week_dates(week_start_date):
    """Get all 7 dates for the week starting from week_start_date"""
    return [week_start_date + timedelta(days=i) for i in range(7)]


def get_monday_of_week(target_date):
    """Get Monday of the week containing target_date"""
    days_since_monday = target_date.weekday()
    monday = target_date - timedelta(days=days_since_monday)
    return monday


def validate_employees_exist(attendance_records):
    """Validate that all employees in attendance records exist and are active"""
    employee_ids = [record['employee_id'] for record in attendance_records]
    
    # Check if all employee IDs exist and are active
    existing_employees = Employee.objects.filter(
        id__in=employee_ids, 
        status=True
    ).values('id', 'name')
    
    existing_ids = {str(emp['id']) for emp in existing_employees}
    existing_names = {str(emp['id']): emp['name'] for emp in existing_employees}
    
    errors = []
    
    for record in attendance_records:
        emp_id = str(record['employee_id'])
        emp_name = record['employee_name']
        
        # Check if employee exists
        if emp_id not in existing_ids:
            errors.append(f"Employee with ID {emp_id} does not exist or is inactive")
            continue
            
        # Check if employee name matches
        if existing_names[emp_id] != emp_name:
            errors.append(
                f"Employee name mismatch for ID {emp_id}. "
                f"Expected: {existing_names[emp_id]}, Got: {emp_name}"
            )
    
    return errors




def validate_wage_date_ranges(employee_id, new_effective_from, new_effective_to=None, exclude_wage_id=None):
    """
    Validate that a new wage date range doesn't overlap with existing wages
    
    Args:
        employee_id: ID of the employee
        new_effective_from: Start date of new wage period
        new_effective_to: End date of new wage period (None for ongoing)
        exclude_wage_id: ID of wage to exclude from validation (for updates)
    
    Returns:
        tuple: (is_valid, error_message)
    """
    existing_wages = Wage.objects.filter(employee_id=employee_id)
    
    if exclude_wage_id:
        existing_wages = existing_wages.exclude(id=exclude_wage_id)
    
    for wage in existing_wages:
        # Check for overlap
        existing_start = wage.effective_from
        existing_end = wage.effective_to
        
        # If either period has no end date, treat as ongoing
        if new_effective_to is None:
            new_end = date.max
        else:
            new_end = new_effective_to
            
        if existing_end is None:
            existing_end = date.max
        
        # Check for overlap
        if new_effective_from <= existing_end and existing_start <= new_end:
            return False, f"Wage period overlaps with existing wage from {existing_start} to {wage.effective_to or 'present'}"
    
    return True, None

