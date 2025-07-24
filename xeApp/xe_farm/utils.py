import os
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
import io
import logging

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