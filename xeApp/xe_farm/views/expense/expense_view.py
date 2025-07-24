from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime, timedelta
from ...models import Expense
from ...serializers import ExpenseSerializer
from ...utils import get_default_expense_image_local  # Assuming you have this utility
import uuid
import os
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def save_expense_data(request):
    """
    Save expense data with optional image upload to local Django storage
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
        
        # Validate the expense data
        serializer = ExpenseSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Handle image upload
        image_url = ''
        
        # Try multiple field names for the image file
        file = (request.FILES.get('file') or 
                request.FILES.get('image') or 
                request.FILES.get('expense_image') or 
                validated_data.pop('file', None))
        
        # Check for default image flag
        default_exp_image = (request.data.get('default_exp_image') == 'true' or 
                           request.data.get('defaultExpImage') == 'true' or
                           validated_data.pop('default_exp_image', False))
        
        if file:
            try:
                # Ensure the directory exists
                expense_images_dir = os.path.join(settings.MEDIA_ROOT, 'expense_images')
                os.makedirs(expense_images_dir, exist_ok=True)
                
                # Generate unique filename
                file_extension = os.path.splitext(file.name)[1] if file.name else '.jpg'
                filename = f"expense_images/{uuid.uuid4()}{file_extension}"
                
                # Save file to Django storage
                saved_path = default_storage.save(filename, file)
                
                # Generate the relative URL
                image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                
                print(f"Expense image saved successfully: {image_url}")
                
            except Exception as upload_error:
                print(f"Upload error: {upload_error}")
                return Response({
                    'status': 'error',
                    'message': f'File upload failed: {str(upload_error)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        elif default_exp_image:
            try:
                default_image_content = get_default_expense_image_local()
                if default_image_content:
                    # Ensure the directory exists
                    expense_images_dir = os.path.join(settings.MEDIA_ROOT, 'expense_images')
                    os.makedirs(expense_images_dir, exist_ok=True)
                    
                    # Generate unique filename for default image
                    filename = f"expense_images/default_{uuid.uuid4()}.jpg"
                    
                    # If default_image_content is bytes, wrap it in ContentFile
                    if isinstance(default_image_content, bytes):
                        default_image_content = ContentFile(default_image_content, name=filename)
                    
                    # Save default image
                    saved_path = default_storage.save(filename, default_image_content)
                    
                    # Generate the relative URL
                    image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                    
                    print(f"Default expense image saved: {image_url}")
                    
            except Exception as e:
                print(f"Default expense image error: {e}")
                # Don't fail the entire request for default image issues
                pass
        
        # Add image_url to validated_data
        validated_data['expense_image_url'] = image_url
        
        # Create expense record
        expense = Expense.objects.create(**validated_data)
        
        # Return success response
        response_serializer = ExpenseSerializer(expense)
        return Response({
            'status': 'success',
            'message': 'Expense data saved successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Server error: {e}")
        logger.error(f"Error saving expense: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_expense_list(request):
    """
    Get list of all expenses with optional filtering, searching, and pagination
    
    Query Parameters:
    - page: Page number for pagination (default: 1)
    - limit: Number of items per page (default: 10, max: 100)
    - search: Search term to filter by expense_name, description, or spent_by
    - category: Filter by category
    - mode_of_payment: Filter by payment mode
    - date_from: Filter expenses from this date (YYYY-MM-DD)
    - date_to: Filter expenses to this date (YYYY-MM-DD)
    - spent_by: Filter by who spent the money
    - min_amount: Filter by minimum amount
    - max_amount: Filter by maximum amount
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 10)), 100)  # Max 100 items per page
        search = request.GET.get('search', '').strip()
        
        # Start with all expenses (removed status filter)
        expenses = Expense.objects.all()
        
        # Apply search filter
        if search:
            expenses = expenses.filter(
                Q(expense_name__icontains=search) |
                Q(description__icontains=search) |
                Q(spent_by__icontains=search)
            )
        
        # Apply category filter
        category = request.GET.get('category', '').strip()
        if category:
            expenses = expenses.filter(category__iexact=category)
        
        # Apply payment mode filter
        mode_of_payment = request.GET.get('mode_of_payment', '').strip()
        if mode_of_payment:
            expenses = expenses.filter(mode_of_payment__iexact=mode_of_payment)
        
        # Apply spent_by filter
        spent_by = request.GET.get('spent_by', '').strip()
        if spent_by:
            expenses = expenses.filter(spent_by__icontains=spent_by)
        
        # Apply date range filter
        date_from = request.GET.get('date_from', '').strip()
        date_to = request.GET.get('date_to', '').strip()
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                expenses = expenses.filter(date__gte=date_from_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid date_from format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                expenses = expenses.filter(date__lte=date_to_obj)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid date_to format. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Apply amount range filter
        min_amount = request.GET.get('min_amount', '').strip()
        max_amount = request.GET.get('max_amount', '').strip()
        
        if min_amount:
            try:
                min_amount_val = float(min_amount)
                expenses = expenses.filter(amount__gte=min_amount_val)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid min_amount format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if max_amount:
            try:
                max_amount_val = float(max_amount)
                expenses = expenses.filter(amount__lte=max_amount_val)
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid max_amount format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Order by date (newest first)
        expenses = expenses.order_by('-date', '-created_at')
        
        # Apply pagination
        paginator = Paginator(expenses, limit)
        
        # Validate page number
        if page < 1:
            page = 1
        elif page > paginator.num_pages and paginator.num_pages > 0:
            page = paginator.num_pages
        
        page_obj = paginator.get_page(page)
        
        # Serialize the data
        serializer = ExpenseSerializer(page_obj.object_list, many=True)
        
        # Calculate total amount for current filter
        total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'status': 'success',
            'message': 'Expenses retrieved successfully',
            'data': {
                'expenses': serializer.data,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': paginator.count,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'per_page': limit
                },
                'summary': {
                    'total_amount': float(total_amount),
                    'count': paginator.count
                }
            }
        }, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response({
            'status': 'error',
            'message': 'Invalid parameter values'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        logger.error(f"Error retrieving expenses: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_expense_detail(request, expense_id):
    """
    Get detailed information for a specific expense by ID
    """
    try:
        # Get expense by ID or return 404
        expense = get_object_or_404(Expense, id=expense_id)
        
        # Serialize the expense data
        serializer = ExpenseSerializer(expense)
        
        return Response({
            'status': 'success',
            'message': 'Expense details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving expense detail: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_expense_statistics(request):
    """
    Get expense statistics and summary information
    """
    try:
        # Get current date info
        today = timezone.now().date()
        current_month_start = today.replace(day=1)
        current_year_start = today.replace(month=1, day=1)
        last_30_days = today - timedelta(days=30)
        
        # Basic statistics (removed status filter)
        total_expenses = Expense.objects.count()
        total_amount = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        
        # Monthly statistics
        monthly_count = Expense.objects.filter(
            date__gte=current_month_start
        ).count()
        monthly_amount = Expense.objects.filter(
            date__gte=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Yearly statistics
        yearly_count = Expense.objects.filter(
            date__gte=current_year_start
        ).count()
        yearly_amount = Expense.objects.filter(
            date__gte=current_year_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Last 30 days statistics
        last_30_days_count = Expense.objects.filter(
            date__gte=last_30_days
        ).count()
        last_30_days_amount = Expense.objects.filter(
            date__gte=last_30_days
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Category-wise statistics
        category_stats = []
        for choice in Expense.CATEGORY_CHOICES:
            category_expenses = Expense.objects.filter(
                category=choice[0]
            )
            count = category_expenses.count()
            amount = category_expenses.aggregate(total=Sum('amount'))['total'] or 0
            
            if count > 0:
                category_stats.append({
                    'category': choice[0],
                    'count': count,
                    'amount': float(amount)
                })
        
        # Payment mode statistics
        payment_mode_stats = []
        for choice in Expense.PAYMENT_MODE_CHOICES:
            mode_expenses = Expense.objects.filter(
                mode_of_payment=choice[0]
            )
            count = mode_expenses.count()
            amount = mode_expenses.aggregate(total=Sum('amount'))['total'] or 0
            
            if count > 0:
                payment_mode_stats.append({
                    'mode_of_payment': choice[0],
                    'count': count,
                    'amount': float(amount)
                })
        
        # Top spenders
        from django.db.models import Count
        top_spenders = Expense.objects.values('spent_by').annotate(
            total_count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('-total_amount')[:5]
        
        top_spenders_list = []
        for spender in top_spenders:
            top_spenders_list.append({
                'spent_by': spender['spent_by'],
                'count': spender['total_count'],
                'amount': float(spender['total_amount'])
            })
        
        return Response({
            'status': 'success',
            'message': 'Expense statistics retrieved successfully',
            'data': {
                'summary': {
                    'total_expenses': total_expenses,
                    'total_amount': float(total_amount),
                    'monthly_count': monthly_count,
                    'monthly_amount': float(monthly_amount),
                    'yearly_count': yearly_count,
                    'yearly_amount': float(yearly_amount),
                    'last_30_days_count': last_30_days_count,
                    'last_30_days_amount': float(last_30_days_amount)
                },
                'category_stats': category_stats,
                'payment_mode_stats': payment_mode_stats,
                'top_spenders': top_spenders_list
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving expense statistics: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['PUT'])
def edit_expense_data(request, expense_id):
    """
    Edit expense data with optional image upload to local Django storage
    """
    try:
        # Get the expense instance
        try:
            expense = Expense.objects.get(id=expense_id)
        except Expense.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Expense not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if request has any data
        if not request.data and not request.FILES:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate the expense data (partial update allowed)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Handle image upload/update
        image_url = expense.expense_image_url  # Keep existing image by default
        
        # Get file from request or validated data
        file = (request.FILES.get('file') or 
                request.FILES.get('image') or 
                request.FILES.get('expense_image') or
                validated_data.pop('file', None))
        
        default_exp_image = (request.data.get('default_exp_image') == 'true' or 
                           request.data.get('defaultExpImage') == 'true' or
                           validated_data.pop('default_exp_image', False))
        
        remove_image = request.data.get('remove_image', False)
        
        # Handle image removal
        if remove_image:
            # Remove old image file if it exists
            if expense.expense_image_url:
                _delete_expense_image(expense.expense_image_url)
            image_url = ''
            
        elif file:
            try:
                # Remove old image file if it exists
                if expense.expense_image_url:
                    _delete_expense_image(expense.expense_image_url)
                
                # Ensure the directory exists
                expense_images_dir = os.path.join(settings.MEDIA_ROOT, 'expense_images')
                os.makedirs(expense_images_dir, exist_ok=True)
                
                # Generate unique filename
                file_extension = os.path.splitext(file.name)[1] if file.name else '.jpg'
                filename = f"expense_images/{uuid.uuid4()}{file_extension}"
                
                # Save file to Django storage
                saved_path = default_storage.save(filename, file)
                
                # Generate the relative URL
                image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                
            except Exception as upload_error:
                logger.error(f"File upload error: {upload_error}")
                return Response({
                    'status': 'error',
                    'message': f'File upload failed: {str(upload_error)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        elif default_exp_image:
            try:
                # Remove old image file if it exists
                if expense.expense_image_url:
                    _delete_expense_image(expense.expense_image_url)
                
                default_image_content = get_default_expense_image_local()
                if default_image_content:
                    # Ensure the directory exists
                    expense_images_dir = os.path.join(settings.MEDIA_ROOT, 'expense_images')
                    os.makedirs(expense_images_dir, exist_ok=True)
                    
                    # Generate unique filename for default image
                    filename = f"expense_images/default_{uuid.uuid4()}.jpg"
                    
                    # If default_image_content is bytes, wrap it in ContentFile
                    if isinstance(default_image_content, bytes):
                        default_image_content = ContentFile(default_image_content, name=filename)
                    
                    # Save default image
                    saved_path = default_storage.save(filename, default_image_content)
                    
                    # Generate the relative URL
                    image_url = f"{settings.MEDIA_URL.rstrip('/')}/{saved_path}"
                    
            except Exception as e:
                logger.warning(f"Default image error: {e}")
                # Don't fail the entire request for default image issues
                pass
        
        # Add image_url to validated_data
        validated_data['expense_image_url'] = image_url
        
        # Update expense record
        for attr, value in validated_data.items():
            setattr(expense, attr, value)
        
        expense.save()
        
        # Return success response
        response_serializer = ExpenseSerializer(expense)
        return Response({
            'status': 'success',
            'message': 'Expense data updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error updating expense: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_expense(request, expense_id):
    """
    Delete expense - permanently removes record and associated image file
    """
    try:
        # Get the expense object
        expense = get_object_or_404(Expense, id=expense_id)
        
        # Store expense data for response before deletion
        expense_data = {
            'expense_id': expense.id,
            'expense_name': expense.expense_name,
            'amount': float(expense.amount),
            'expense_image_url': expense.expense_image_url
        }
        
        # Delete associated image file if exists
        if expense.expense_image_url:
            _delete_expense_image(expense.expense_image_url)
        
        # Permanently delete the expense record
        expense.delete()
        
        return Response({
            'status': 'success',
            'message': 'Expense deleted successfully',
            'data': expense_data
        }, status=status.HTTP_200_OK)
            
    except Expense.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Expense not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error deleting expense {expense_id}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Helper function
def _delete_expense_image(image_url):
    """
    Delete the expense image file from storage
    """
    try:
        if not image_url:
            return
            
        # Extract file path from URL
        # Remove MEDIA_URL prefix to get the relative path
        media_url = settings.MEDIA_URL.rstrip('/')
        if image_url.startswith(media_url):
            relative_path = image_url[len(media_url):].lstrip('/')
        else:
            # Handle cases where image_url might be just the relative path
            relative_path = image_url.lstrip('/')
        
        # Delete file from storage
        if default_storage.exists(relative_path):
            default_storage.delete(relative_path)
            print(f"Deleted expense image: {relative_path}")
        else:
            print(f"Image file not found: {relative_path}")
            
    except Exception as e:
        print(f"Error deleting image {image_url}: {e}")
        logger.warning(f"Failed to delete expense image {image_url}: {str(e)}")