from calendar import monthrange
from django.db.models import Count
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
from ...utils import get_default_expense_image_local  
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



@api_view(['GET'])
def get_expense_dashboard_stats(request):
    """
    Get comprehensive expense statistics for dashboard
    Including: current year, last year, current month, last month, whole year data
    """
    try:
        # Get current date info
        today = timezone.now().date()
        current_year = today.year
        current_month = today.month
        
        # Date ranges
        current_year_start = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)
        
        last_year = current_year - 1
        last_year_start = today.replace(year=last_year, month=1, day=1)
        last_year_end = today.replace(year=last_year, month=12, day=31)
        
        current_month_start = today.replace(day=1)
        # Get last day of current month
        last_day_current_month = monthrange(current_year, current_month)[1]
        current_month_end = today.replace(day=last_day_current_month)
        
        # Last month calculation
        if current_month == 1:
            last_month_year = current_year - 1
            last_month_num = 12
        else:
            last_month_year = current_year
            last_month_num = current_month - 1
        
        last_month_start = today.replace(year=last_month_year, month=last_month_num, day=1)
        last_day_last_month = monthrange(last_month_year, last_month_num)[1]
        last_month_end = today.replace(year=last_month_year, month=last_month_num, day=last_day_last_month)
        
        # Last 30 days
        last_30_days = today - timedelta(days=30)
        
        # Time period statistics
        time_periods = {}
        
        # Current Year
        current_year_expenses = Expense.objects.filter(date__range=[current_year_start, current_year_end])
        time_periods['current_year'] = {
            'count': current_year_expenses.count(),
            'amount': float(current_year_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Current Year ({current_year})',
            'start_date': current_year_start.isoformat(),
            'end_date': current_year_end.isoformat()
        }
        
        # Last Year
        last_year_expenses = Expense.objects.filter(date__range=[last_year_start, last_year_end])
        time_periods['last_year'] = {
            'count': last_year_expenses.count(),
            'amount': float(last_year_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Last Year ({last_year})',
            'start_date': last_year_start.isoformat(),
            'end_date': last_year_end.isoformat()
        }
        
        # Current Month
        current_month_expenses = Expense.objects.filter(date__range=[current_month_start, current_month_end])
        time_periods['current_month'] = {
            'count': current_month_expenses.count(),
            'amount': float(current_month_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Current Month ({today.strftime("%B %Y")})',
            'start_date': current_month_start.isoformat(),
            'end_date': current_month_end.isoformat()
        }
        
        # Last Month
        last_month_expenses = Expense.objects.filter(date__range=[last_month_start, last_month_end])
        month_name = last_month_start.strftime("%B %Y")
        time_periods['last_month'] = {
            'count': last_month_expenses.count(),
            'amount': float(last_month_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Last Month ({month_name})',
            'start_date': last_month_start.isoformat(),
            'end_date': last_month_end.isoformat()
        }
        
        # Last 30 Days
        last_30_days_expenses = Expense.objects.filter(date__gte=last_30_days)
        time_periods['last_30_days'] = {
            'count': last_30_days_expenses.count(),
            'amount': float(last_30_days_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': 'Last 30 Days',
            'start_date': last_30_days.isoformat(),
            'end_date': today.isoformat()
        }
        
        # All Time (Whole Year Data)
        all_expenses = Expense.objects.all()
        time_periods['all_time'] = {
            'count': all_expenses.count(),
            'amount': float(all_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': 'All Time',
            'start_date': None,
            'end_date': None
        }
        
        # Category-wise statistics for current year
        category_stats = []
        for choice in Expense.CATEGORY_CHOICES:
            category_expenses = current_year_expenses.filter(category=choice[0])
            count = category_expenses.count()
            amount = category_expenses.aggregate(total=Sum('amount'))['total'] or 0
            
            category_stats.append({
                'category': choice[0],
                'category_display': choice[1],
                'count': count,
                'amount': float(amount),
                'percentage': round((float(amount) / time_periods['current_year']['amount'] * 100) if time_periods['current_year']['amount'] > 0 else 0, 2)
            })
        
        # Payment mode statistics for current year
        payment_mode_stats = []
        for choice in Expense.PAYMENT_MODE_CHOICES:
            mode_expenses = current_year_expenses.filter(mode_of_payment=choice[0])
            count = mode_expenses.count()
            amount = mode_expenses.aggregate(total=Sum('amount'))['total'] or 0
            
            payment_mode_stats.append({
                'mode_of_payment': choice[0],
                'mode_display': choice[1],
                'count': count,
                'amount': float(amount),
                'percentage': round((float(amount) / time_periods['current_year']['amount'] * 100) if time_periods['current_year']['amount'] > 0 else 0, 2)
            })
        
        # Top spenders for current year
        top_spenders = current_year_expenses.values('spent_by').annotate(
            total_count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('-total_amount')[:10]
        
        top_spenders_list = []
        for spender in top_spenders:
            top_spenders_list.append({
                'spent_by': spender['spent_by'],
                'count': spender['total_count'],
                'amount': float(spender['total_amount']),
                'percentage': round((float(spender['total_amount']) / time_periods['current_year']['amount'] * 100) if time_periods['current_year']['amount'] > 0 else 0, 2)
            })
        
        return Response({
            'status': 'success',
            'message': 'Dashboard statistics retrieved successfully',
            'data': {
                'time_periods': time_periods,
                'current_year_breakdown': {
                    'category_stats': category_stats,
                    'payment_mode_stats': payment_mode_stats,
                    'top_spenders': top_spenders_list
                },
                'generated_at': timezone.now().isoformat()
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving dashboard statistics: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_monthly_trend_data(request):
    """
    Get monthly expense trends for the current and last year
    """
    try:
        today = timezone.now().date()
        current_year = today.year
        last_year = current_year - 1
        
        monthly_data = []
        
        # Get data for both years
        for year in [last_year, current_year]:
            for month in range(1, 13):
                # Skip future months in current year
                if year == current_year and month > today.month:
                    continue
                    
                month_start = datetime(year, month, 1).date()
                last_day = monthrange(year, month)[1]
                month_end = datetime(year, month, last_day).date()
                
                month_expenses = Expense.objects.filter(
                    date__range=[month_start, month_end]
                )
                
                count = month_expenses.count()
                amount = month_expenses.aggregate(total=Sum('amount'))['total'] or 0
                
                monthly_data.append({
                    'year': year,
                    'month': month,
                    'month_name': month_start.strftime('%B'),
                    'month_year': month_start.strftime('%b %Y'),
                    'count': count,
                    'amount': float(amount),
                    'start_date': month_start.isoformat(),
                    'end_date': month_end.isoformat()
                })
        
        return Response({
            'status': 'success',
            'message': 'Monthly trend data retrieved successfully',
            'data': {
                'monthly_trends': monthly_data,
                'generated_at': timezone.now().isoformat()
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving monthly trend data: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_expense_comparison_stats(request):
    """
    Get comparative statistics between different periods
    """
    try:
        today = timezone.now().date()
        current_year = today.year
        current_month = today.month
        
        # Calculate date ranges
        current_year_start = today.replace(month=1, day=1)
        last_year = current_year - 1
        last_year_start = today.replace(year=last_year, month=1, day=1)
        last_year_end = today.replace(year=last_year, month=12, day=31)
        
        current_month_start = today.replace(day=1)
        if current_month == 1:
            last_month_year = current_year - 1
            last_month_num = 12
        else:
            last_month_year = current_year
            last_month_num = current_month - 1
        last_month_start = today.replace(year=last_month_year, month=last_month_num, day=1)
        last_day_last_month = monthrange(last_month_year, last_month_num)[1]
        last_month_end = today.replace(year=last_month_year, month=last_month_num, day=last_day_last_month)
        
        # Get statistics
        current_year_stats = Expense.objects.filter(date__gte=current_year_start).aggregate(
            count=Count('id'), total=Sum('amount')
        )
        last_year_stats = Expense.objects.filter(date__range=[last_year_start, last_year_end]).aggregate(
            count=Count('id'), total=Sum('amount')
        )
        current_month_stats = Expense.objects.filter(date__gte=current_month_start).aggregate(
            count=Count('id'), total=Sum('amount')
        )
        last_month_stats = Expense.objects.filter(date__range=[last_month_start, last_month_end]).aggregate(
            count=Count('id'), total=Sum('amount')
        )
        
        # Calculate percentage changes
        def calculate_percentage_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 2)
        
        current_year_amount = float(current_year_stats['total'] or 0)
        last_year_amount = float(last_year_stats['total'] or 0)
        current_month_amount = float(current_month_stats['total'] or 0)
        last_month_amount = float(last_month_stats['total'] or 0)
        
        yearly_change = calculate_percentage_change(current_year_amount, last_year_amount)
        monthly_change = calculate_percentage_change(current_month_amount, last_month_amount)
        
        return Response({
            'status': 'success',
            'message': 'Comparison statistics retrieved successfully',
            'data': {
                'yearly_comparison': {
                    'current_year': {
                        'amount': current_year_amount,
                        'count': current_year_stats['count'] or 0
                    },
                    'last_year': {
                        'amount': last_year_amount,
                        'count': last_year_stats['count'] or 0
                    },
                    'percentage_change': yearly_change,
                    'trend': 'up' if yearly_change > 0 else 'down' if yearly_change < 0 else 'stable'
                },
                'monthly_comparison': {
                    'current_month': {
                        'amount': current_month_amount,
                        'count': current_month_stats['count'] or 0
                    },
                    'last_month': {
                        'amount': last_month_amount,
                        'count': last_month_stats['count'] or 0
                    },
                    'percentage_change': monthly_change,
                    'trend': 'up' if monthly_change > 0 else 'down' if monthly_change < 0 else 'stable'
                },
                'generated_at': timezone.now().isoformat()
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving comparison statistics: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_expense_summary_by_period(request, period_type):
    """
    Get expense summary for a specific period type
    
    Parameters:
    - period_type: 'current_year', 'last_year', 'current_month', 'last_month', 'all_time'
    """
    try:
        today = timezone.now().date()
        current_year = today.year
        current_month = today.month
        
        # Determine date range based on period_type
        if period_type == 'current_year':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
            period_name = f'Current Year ({current_year})'
        elif period_type == 'last_year':
            last_year = current_year - 1
            start_date = today.replace(year=last_year, month=1, day=1)
            end_date = today.replace(year=last_year, month=12, day=31)
            period_name = f'Last Year ({last_year})'
        elif period_type == 'current_month':
            start_date = today.replace(day=1)
            last_day = monthrange(current_year, current_month)[1]
            end_date = today.replace(day=last_day)
            period_name = f'Current Month ({today.strftime("%B %Y")})'
        elif period_type == 'last_month':
            if current_month == 1:
                last_month_year = current_year - 1
                last_month_num = 12
            else:
                last_month_year = current_year
                last_month_num = current_month - 1
            start_date = today.replace(year=last_month_year, month=last_month_num, day=1)
            last_day = monthrange(last_month_year, last_month_num)[1]
            end_date = today.replace(year=last_month_year, month=last_month_num, day=last_day)
            period_name = f'Last Month ({start_date.strftime("%B %Y")})'
        elif period_type == 'all_time':
            start_date = None
            end_date = None
            period_name = 'All Time'
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid period_type. Use: current_year, last_year, current_month, last_month, all_time'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter expenses based on period
        if period_type == 'all_time':
            expenses = Expense.objects.all()
        else:
            expenses = Expense.objects.filter(date__range=[start_date, end_date])
        
        # Calculate statistics
        total_count = expenses.count()
        total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0
        
        # Category breakdown
        category_breakdown = []
        for choice in Expense.CATEGORY_CHOICES:
            cat_expenses = expenses.filter(category=choice[0])
            count = cat_expenses.count()
            amount = cat_expenses.aggregate(total=Sum('amount'))['total'] or 0
            
            if count > 0:
                category_breakdown.append({
                    'category': choice[0],
                    'category_display': choice[1],
                    'count': count,
                    'amount': float(amount),
                    'percentage': round((float(amount) / float(total_amount) * 100) if total_amount > 0 else 0, 2)
                })
        
        # Payment mode breakdown
        payment_breakdown = []
        for choice in Expense.PAYMENT_MODE_CHOICES:
            mode_expenses = expenses.filter(mode_of_payment=choice[0])
            count = mode_expenses.count()
            amount = mode_expenses.aggregate(total=Sum('amount'))['total'] or 0
            
            if count > 0:
                payment_breakdown.append({
                    'mode': choice[0],
                    'mode_display': choice[1],
                    'count': count,
                    'amount': float(amount),
                    'percentage': round((float(amount) / float(total_amount) * 100) if total_amount > 0 else 0, 2)
                })
        
        # Top expenses
        top_expenses = expenses.order_by('-amount')[:5]
        top_expenses_list = []
        for expense in top_expenses:
            top_expenses_list.append({
                'id': expense.id,
                'expense_name': expense.expense_name,
                'amount': float(expense.amount),
                'date': expense.date.isoformat(),
                'category': expense.category,
                'spent_by': expense.spent_by
            })
        
        return Response({
            'status': 'success',
            'message': f'Summary for {period_name} retrieved successfully',
            'data': {
                'period_info': {
                    'type': period_type,
                    'name': period_name,
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None
                },
                'summary': {
                    'total_count': total_count,
                    'total_amount': float(total_amount)
                },
                'category_breakdown': category_breakdown,
                'payment_breakdown': payment_breakdown,
                'top_expenses': top_expenses_list,
                'generated_at': timezone.now().isoformat()
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving expense summary for {period_type}: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)