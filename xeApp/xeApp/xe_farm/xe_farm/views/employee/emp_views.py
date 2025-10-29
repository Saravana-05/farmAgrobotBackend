from venv import logger
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from ...models import Employee
from ...serializers import EmployeeSerializer
from ...utils import get_default_avatar_local
import uuid
import os
from django.core.paginator import Paginator 
from django.db.models import Q 
from django.shortcuts import get_object_or_404  
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view

@api_view(['POST'])
def save_employee_data(request):
    """
    Save employee data with optional image upload to local Django storage
    """
    try:
        # Check if request has any data
        if not request.data and not request.FILES:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Debug logging
        print(f"Request data: {request.data}")
        print(f"Request files: {request.FILES}")
        
        # Validate the employee data
        serializer = EmployeeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Check if contact number already exists
        contact = validated_data.get('contact')
        if contact and contact != 'N/A':
            # Check for existing employee with same contact number
            existing_employee = Employee.objects.filter(
                contact=contact
            ).first()
            
            if existing_employee:
                return Response({
                    'status': 'error',
                    'message': 'Employee with this contact number already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle image upload
        image_url = ''
        
        # Try multiple field names for the image file
        file = (request.FILES.get('file') or 
                request.FILES.get('image') or 
                validated_data.pop('file', None))
        
        # Check for default avatar flag
        default_avatar = (request.data.get('default_avatar') == 'true' or 
                         validated_data.pop('default_avatar', False))
        
        if file:
            try:
                # Ensure the directory exists
                employee_images_dir = os.path.join(settings.MEDIA_ROOT, 'employee_images')
                os.makedirs(employee_images_dir, exist_ok=True)
                
                # Generate unique filename
                file_extension = os.path.splitext(file.name)[1] if file.name else '.jpg'
                filename = f"employee_images/{uuid.uuid4()}{file_extension}"
                
                # Save file to Django storage
                saved_path = default_storage.save(filename, file)
                
                # Generate the relative URL
                image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                
                print(f"Image saved successfully: {image_url}")
                
            except Exception as upload_error:
                print(f"Upload error: {upload_error}")
                return Response({
                    'status': 'error',
                    'message': f'File upload failed: {str(upload_error)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        elif default_avatar:
            try:
                default_avatar_content = get_default_avatar_local()
                if default_avatar_content:
                    # Ensure the directory exists
                    employee_images_dir = os.path.join(settings.MEDIA_ROOT, 'employee_images')
                    os.makedirs(employee_images_dir, exist_ok=True)
                    
                    # Generate unique filename for default avatar
                    filename = f"employee_images/default_{uuid.uuid4()}.jpg"
                    
                    # If default_avatar_content is bytes, wrap it in ContentFile
                    if isinstance(default_avatar_content, bytes):
                        default_avatar_content = ContentFile(default_avatar_content, name=filename)
                    
                    # Save default avatar
                    saved_path = default_storage.save(filename, default_avatar_content)
                    
                    # Generate the relative URL
                    image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                    
                    print(f"Default avatar saved: {image_url}")
                    
            except Exception as e:
                print(f"Default avatar error: {e}")
                # Don't fail the entire request for default avatar issues
                pass
        
        # Add image_url to validated_data
        validated_data['image_url'] = image_url
        
        # Create employee record
        employee = Employee.objects.create(**validated_data)
        
        # Return success response
        response_serializer = EmployeeSerializer(employee)
        return Response({
            'status': 'success',
            'message': 'Employee data saved successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_employee_list(request):
    """
    Get list of all employees with optional filtering, searching, and pagination
    
    Query Parameters:
    - page: Page number for pagination (default: 1)
    - limit: Number of items per page (default: 10, max: 100)
    - search: Search term to filter by name, tamil_name, or contact
    - emp_type: Filter by employee type (Regular, Contract, Others)
    - gender: Filter by gender (Male, Female, Other)
    - is_active: Filter by status (true/false)
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 10)), 100)  # Max 100 items per page
        search = request.GET.get('search', '').strip()
        is_active = request.GET.get('is_active', '').strip().lower()
        
        # Start with all employees
        employees = Employee.objects.all()
        
        # Apply search filter
        if search:
            employees = employees.filter(
                Q(name__icontains=search) |
                Q(tamil_name__icontains=search) |
                Q(contact__icontains=search)
            )
        
        # Apply employee type filter
        emp_type = request.GET.get('emp_type', '').strip()
        if emp_type:
            employees = employees.filter(emp_type__iexact=emp_type)
        
        # Apply gender filter
        gender = request.GET.get('gender', '').strip()
        if gender:
            employees = employees.filter(gender__iexact=gender)
        
        # Apply status filter
        if is_active in ['true', 'false']:
            employees = employees.filter(status=(is_active == 'true'))
        
        # Order by creation date (newest first)
        employees = employees.order_by('-created_at')
        
        # Apply pagination
        paginator = Paginator(employees, limit)
        
        # Validate page number
        if page < 1:
            page = 1
        elif page > paginator.num_pages and paginator.num_pages > 0:
            page = paginator.num_pages
        
        page_obj = paginator.get_page(page)
        
        # Serialize the data
        serializer = EmployeeSerializer(page_obj.object_list, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Employees retrieved successfully',
            'data': {
                'employees': serializer.data,
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
        
    except ValueError as e:
        return Response({
            'status': 'error',
            'message': 'Invalid parameter values'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def get_employee_detail(request, employee_id):
    """
    Get detailed information for a specific employee by ID
    """
    try:
        # Get employee by ID or return 404
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Serialize the employee data
        serializer = EmployeeSerializer(employee)
        
        return Response({
            'status': 'success',
            'message': 'Employee details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_employee_statistics(request):
    """
    Get employee statistics and summary information
    """
    try:
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(status=True).count()
        inactive_employees = total_employees - active_employees
        
        # Get employee type-wise count
        emp_type_stats = []
        for choice in Employee.EMP_TYPE_CHOICES:
            count = Employee.objects.filter(emp_type=choice[0]).count()
            if count > 0:
                emp_type_stats.append({
                    'emp_type': choice[0],
                    'count': count
                })
        
        # Get gender-wise count
        gender_stats = []
        for choice in Employee.GENDER_CHOICES:
            count = Employee.objects.filter(gender=choice[0]).count()
            if count > 0:
                gender_stats.append({
                    'gender': choice[0],
                    'count': count
                })
        
        # Get recent hires (last 30 days)
        from django.utils import timezone
        from datetime import timedelta
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_hires = Employee.objects.filter(joining_date__gte=thirty_days_ago).count()
        
        return Response({
            'status': 'success',
            'message': 'Employee statistics retrieved successfully',
            'data': {
                'summary': {
                    'total_employees': total_employees,
                    'active_employees': active_employees,
                    'inactive_employees': inactive_employees,
                    'recent_hires': recent_hires
                },
                'emp_type_stats': emp_type_stats,
                'gender_stats': gender_stats
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@csrf_exempt
@api_view(['PUT'])
def edit_employee_data(request, employee_id):
    """
    Edit employee data with optional image upload to local Django storage
    Model fields: name, tamil_name, joining_date, emp_type, gender, 
                 image_url, contact, status, created_at, updated_at
    """
    try:
        # Get the employee instance
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Employee not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if request has any data
        if not request.data and not request.FILES:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate the employee data (partial update allowed)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # # Check if contact number already exists (excluding current employee)
        # contact = validated_data.get('contact')
        # if contact:
        #     existing_employee = Employee.objects.filter(
        #         contact=contact
        #     ).exclude(id=employee_id).first()
            
        #     if existing_employee:
        #         return Response({
        #             'status': 'error',
        #             'message': 'Employee with this contact number already exists'
        #         }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate choice fields if they're being updated
        emp_type = validated_data.get('emp_type')
        if emp_type and emp_type not in [choice[0] for choice in Employee.EMP_TYPE_CHOICES]:
            return Response({
                'status': 'error',
                'message': f'Invalid employee type. Must be one of: {[choice[0] for choice in Employee.EMP_TYPE_CHOICES]}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        gender = validated_data.get('gender')
        if gender and gender not in [choice[0] for choice in Employee.GENDER_CHOICES]:
            return Response({
                'status': 'error',
                'message': f'Invalid gender. Must be one of: {[choice[0] for choice in Employee.GENDER_CHOICES]}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle image upload/update
        image_url = employee.image_url  # Keep existing image by default
        
        # Get file from request or validated data
        file = request.FILES.get('file') or validated_data.pop('file', None)
        default_avatar = validated_data.pop('default_avatar', False)
        remove_image = request.data.get('remove_image', False)
        
        # Handle image removal
        if remove_image:
            # Remove old image file if it exists
            if employee.image_url:
                old_image_path = employee.image_url.replace(settings.MEDIA_URL, '')
                old_file_path = os.path.join(settings.MEDIA_ROOT, old_image_path)
                if os.path.exists(old_file_path):
                    try:
                        os.remove(old_file_path)
                    except Exception:
                        pass  # Don't fail if file removal fails
            image_url = ''
            
        elif file:
            try:
                # Remove old image file if it exists
                if employee.image_url:
                    old_image_path = employee.image_url.replace(settings.MEDIA_URL, '')
                    old_file_path = os.path.join(settings.MEDIA_ROOT, old_image_path)
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except Exception:
                            pass  # Don't fail if old file removal fails
                
                # Ensure the directory exists
                employee_images_dir = os.path.join(settings.MEDIA_ROOT, 'employee_images')
                os.makedirs(employee_images_dir, exist_ok=True)
                
                # Generate unique filename
                file_extension = os.path.splitext(file.name)[1] if file.name else '.jpg'
                filename = f"employee_images/{uuid.uuid4()}{file_extension}"
                
                # Save file to Django storage
                saved_path = default_storage.save(filename, file)
                
                # Generate the relative URL
                image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                
            except Exception as upload_error:
                return Response({
                    'status': 'error',
                    'message': f'File upload failed: {str(upload_error)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        elif default_avatar:
            try:
                # Remove old image file if it exists
                if employee.image_url:
                    old_image_path = employee.image_url.replace(settings.MEDIA_URL, '')
                    old_file_path = os.path.join(settings.MEDIA_ROOT, old_image_path)
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except Exception:
                            pass
                
                default_avatar_content = get_default_avatar_local()
                if default_avatar_content:
                    # Ensure the directory exists
                    employee_images_dir = os.path.join(settings.MEDIA_ROOT, 'employee_images')
                    os.makedirs(employee_images_dir, exist_ok=True)
                    
                    # Generate unique filename for default avatar
                    filename = f"employee_images/default_{uuid.uuid4()}.jpg"
                    
                    # If default_avatar_content is bytes, wrap it in ContentFile
                    if isinstance(default_avatar_content, bytes):
                        default_avatar_content = ContentFile(default_avatar_content, name=filename)
                    
                    # Save default avatar
                    saved_path = default_storage.save(filename, default_avatar_content)
                    
                    # Generate the relative URL
                    image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                    
            except Exception:
                # Don't fail the entire request for default avatar issues
                pass
        
        # Add image_url to validated_data
        validated_data['image_url'] = image_url
        
        # Update employee record
        for attr, value in validated_data.items():
            setattr(employee, attr, value)
        
        employee.save()
        
        # Return success response
        response_serializer = EmployeeSerializer(employee)
        return Response({
            'status': 'success',
            'message': 'Employee data updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete_employee(request, employee_id):
    """
    Delete employee - supports both soft delete and hard delete
    
    Query Parameters:
    - hard_delete: true/false (default: false for soft delete)
    
    Soft Delete: Sets status to False, keeps record in database
    Hard Delete: Permanently removes record and associated image file
    """
    try:
        # Get the employee object
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Check if hard delete is requested
        hard_delete = request.query_params.get('hard_delete', '').lower() == 'true'
        
        if hard_delete:
            # Hard delete - permanently remove the record
            return _hard_delete_employee(employee)
        else:
            # Soft delete - set status to False
            return _soft_delete_employee(employee)
            
    except Employee.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Employee not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error deleting employee {employee_id}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _soft_delete_employee(employee):
    """
    Perform soft delete by setting status to False
    """
    try:
        # Check if already soft deleted
        if not employee.status:
            return Response({
                'status': 'warning',
                'message': 'Employee is already inactive/deleted'
            }, status=status.HTTP_200_OK)
        
        # Set status to False (soft delete)
        employee.status = False
        employee.save(update_fields=['status', 'updated_at'])
        
        return Response({
            'status': 'success',
            'message': 'Employee soft deleted successfully',
            'data': {
                'employee_id': employee.id,
                'name': employee.name,
                'status': employee.status,
                'deleted_at': employee.updated_at
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        raise Exception(f"Soft delete failed: {str(e)}")


def _hard_delete_employee(employee):
    """
    Perform hard delete by permanently removing the record and associated files
    """
    try:
        # Store employee data for response before deletion
        employee_data = {
            'employee_id': employee.id,
            'name': employee.name,
            'contact': employee.contact,
            'image_url': employee.image_url
        }
        
        # Delete associated image file if exists
        if employee.image_url:
            _delete_employee_image(employee.image_url)
        
        # Permanently delete the employee record
        employee.delete()
        
        return Response({
            'status': 'success',
            'message': 'Employee permanently deleted successfully',
            'data': employee_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        raise Exception(f"Hard delete failed: {str(e)}")


def _delete_employee_image(image_url):
    """
    Delete the employee image file from storage
    """
    try:
        if not image_url:
            return
            
        # Extract file path from URL
        # Remove MEDIA_URL prefix to get the relative path
        media_url = settings.MEDIA_URL.rstrip('/')
        if image_url.startswith(media_url):
            relative_path = image_url[len(media_url):].lstrip('/')
            
            # Delete file if it exists
            if default_storage.exists(relative_path):
                default_storage.delete(relative_path)
                logger.info(f"Deleted image file: {relative_path}")
        
    except Exception as e:
        # Don't fail the entire operation if image deletion fails
        logger.warning(f"Failed to delete image file {image_url}: {str(e)}")


@api_view(['POST'])
def restore_employee(request, employee_id):
    """
    Restore a soft-deleted employee by setting status back to True
    """
    try:
        # Get the employee object
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Check if employee is soft deleted
        if employee.status:
            return Response({
                'status': 'warning',
                'message': 'Employee is already active'
            }, status=status.HTTP_200_OK)
        
        # Restore the employee
        employee.status = True
        employee.save(update_fields=['status', 'updated_at'])
        
        return Response({
            'status': 'success',
            'message': 'Employee restored successfully',
            'data': {
                'employee_id': employee.id,
                'name': employee.name,
                'status': employee.status,
                'restored_at': employee.updated_at
            }
        }, status=status.HTTP_200_OK)
        
    except Employee.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Employee not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error restoring employee {employee_id}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def change_employee_status(request, employee_id):
    """
    Change employee status between active and inactive
    
    Request Body:
    {
        "status": true/false  # true for active, false for inactive
    }
    
    OR
    
    {
        "action": "activate"/"deactivate"  # Alternative format
    }
    """
    try:
        # Get the employee object
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Check if request has data
        if not request.data:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the new status from request
        new_status = None
        
        # Check for 'status' field (boolean)
        if 'status' in request.data:
            status_value = request.data.get('status')
            if isinstance(status_value, bool):
                new_status = status_value
            elif isinstance(status_value, str):
                if status_value.lower() in ['true', '1', 'yes', 'active']:
                    new_status = True
                elif status_value.lower() in ['false', '0', 'no', 'inactive']:
                    new_status = False
        
        # Check for 'action' field (string)
        elif 'action' in request.data:
            action = request.data.get('action', '').lower()
            if action == 'activate':
                new_status = True
            elif action == 'deactivate':
                new_status = False
        
        # Validate status value
        if new_status is None:
            return Response({
                'status': 'error',
                'message': 'Invalid or missing status. Use "status": true/false or "action": "activate"/"deactivate"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if status is already the same
        if employee.status == new_status:
            action_word = 'active' if new_status else 'inactive'
            return Response({
                'status': 'warning',
                'message': f'Employee is already {action_word}',
                'data': {
                    'employee_id': employee.id,
                    'name': employee.name,
                    'current_status': employee.status
                }
            }, status=status.HTTP_200_OK)
        
        # Store old status for response
        old_status = employee.status
        
        # Update the status
        employee.status = new_status
        employee.save(update_fields=['status', 'updated_at'])
        
        # Prepare response message
        action_performed = 'activated' if new_status else 'deactivated'
        
        return Response({
            'status': 'success',
            'message': f'Employee {action_performed} successfully',
            'data': {
                'employee_id': employee.id,
                'name': employee.name,
                'old_status': old_status,
                'new_status': employee.status,
                'updated_at': employee.updated_at
            }
        }, status=status.HTTP_200_OK)
        
    except Employee.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Employee not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error changing employee status {employee_id}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def toggle_employee_status(request, employee_id):
    """
    Toggle employee status (active <-> inactive)
    No request body needed - automatically toggles current status
    """
    try:
        # Get the employee object
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Store old status for response
        old_status = employee.status
        
        # Toggle the status
        employee.status = not employee.status
        employee.save(update_fields=['status', 'updated_at'])
        
        # Prepare response message
        action_performed = 'activated' if employee.status else 'deactivated'
        
        return Response({
            'status': 'success',
            'message': f'Employee status toggled - {action_performed} successfully',
            'data': {
                'employee_id': employee.id,
                'name': employee.name,
                'old_status': old_status,
                'new_status': employee.status,
                'updated_at': employee.updated_at
            }
        }, status=status.HTTP_200_OK)
        
    except Employee.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Employee not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error toggling employee status {employee_id}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)