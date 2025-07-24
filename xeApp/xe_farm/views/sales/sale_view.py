from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from ...models import Sale, SaleVariant, Merchant, Yield, CropVariant
from ...serializers import SaleSerializer

@api_view(['POST'])
def save_sale_data(request):
    """
    Save sale data to the database with sale variants
    """
    try:
        # Check if request has any data
        if not request.data:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Debug logging
        print(f"Request data: {request.data}")
        
        # Validate the sale data
        serializer = SaleSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            sale_record = serializer.save()
        
        # Return success response with created data
        response_serializer = SaleSerializer(sale_record)
        return Response({
            'status': 'success',
            'message': 'Sale data saved successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except IntegrityError as e:
        print(f"Database integrity error: {e}")
        return Response({
            'status': 'error',
            'message': 'Database integrity error occurred'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_sales(request):
    """
    Get all sale records from the database with filtering options
    """
    try:
        # Get query parameters for filtering
        merchant_id = request.GET.get('merchant_id')
        yield_id = request.GET.get('yield_id')
        payment_mode = request.GET.get('payment_mode')
        status_filter = request.GET.get('status')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        min_amount = request.GET.get('min_amount')
        max_amount = request.GET.get('max_amount')
        
        # Start with all sales
        sales = Sale.objects.select_related(
            'merchant', 
            'yield_record',
            'yield_record__crop'
        ).prefetch_related(
            'sale_variants__crop_variant',
            'sale_variants__crop_variant__crop'
        )
        
        # Apply filters
        if merchant_id:
            sales = sales.filter(merchant_id=merchant_id)
        
        if yield_id:
            sales = sales.filter(yield_record_id=yield_id)
        
        if payment_mode:
            sales = sales.filter(payment_mode=payment_mode)
        
        if status_filter:
            sales = sales.filter(status=status_filter)
        
        if start_date:
            sales = sales.filter(harvest_date__gte=start_date)
        
        if end_date:
            sales = sales.filter(harvest_date__lte=end_date)
        
        if min_amount:
            sales = sales.filter(final_amount__gte=min_amount)
        
        if max_amount:
            sales = sales.filter(final_amount__lte=max_amount)
        
        # Order by most recent first
        sales = sales.order_by('-created_at')
        
        serializer = SaleSerializer(sales, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Sales retrieved successfully',
            'data': serializer.data,
            'count': sales.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_sale_by_id(request, sale_id):
    """
    Get a specific sale record by ID
    """
    try:
        sale_record = Sale.objects.select_related(
            'merchant', 
            'yield_record',
            'yield_record__crop'
        ).prefetch_related(
            'sale_variants__crop_variant',
            'sale_variants__crop_variant__crop'
        ).get(id=sale_id)
        
        serializer = SaleSerializer(sale_record)
        
        return Response({
            'status': 'success',
            'message': 'Sale retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Sale.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Sale record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_sale_data(request, sale_id):
    """
    Update sale data
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        
        # Validate the updated data
        serializer = SaleSerializer(sale_record, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            sale_record = serializer.save()
        
        # Return updated data
        response_serializer = SaleSerializer(sale_record)
        return Response({
            'status': 'success',
            'message': 'Sale updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Sale.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Sale record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_sale(request, sale_id):
    """
    Delete a sale record
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        
        # Use transaction to ensure related data is also deleted
        with transaction.atomic():
            sale_record.delete()
        
        return Response({
            'status': 'success',
            'message': 'Sale deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Sale.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Sale record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def update_sale_status(request, sale_id):
    """
    Update only the status of a sale record
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        
        # Get the new status from request
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({
                'status': 'error',
                'message': 'Status field is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate status choice
        valid_statuses = [choice[0] for choice in Sale.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({
                'status': 'error',
                'message': f'Invalid status. Valid choices are: {valid_statuses}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status
        sale_record.status = new_status
        sale_record.save()
        
        return Response({
            'status': 'success',
            'message': f'Sale status updated to {new_status}',
            'data': {
                'id': sale_record.id,
                'status': sale_record.status,
                'updated_at': sale_record.updated_at
            }
        }, status=status.HTTP_200_OK)
        
    except Sale.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Sale record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_sales_by_merchant(request, merchant_id):
    """
    Get all sales for a specific merchant
    """
    try:
        # Check if merchant exists
        try:
            merchant = Merchant.objects.get(id=merchant_id)
        except Merchant.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Merchant not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get sales for the merchant
        sales = Sale.objects.filter(merchant_id=merchant_id).select_related(
            'yield_record',
            'yield_record__crop'
        ).prefetch_related(
            'sale_variants__crop_variant'
        ).order_by('-created_at')
        
        serializer = SaleSerializer(sales, many=True)
        
        return Response({
            'status': 'success',
            'message': f'Sales for {merchant.name} retrieved successfully',
            'data': serializer.data,
            'count': sales.count(),
            'merchant': {
                'id': merchant.id,
                'name': merchant.name
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_sale_summary(request):
    """
    Get sale summary statistics
    """
    try:
        from django.db.models import Sum, Count, Avg, Max, Min
        from django.db.models.functions import TruncMonth, TruncDate
        
        # Get query parameters
        merchant_id = request.GET.get('merchant_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        status_filter = request.GET.get('status')
        
        # Base queryset
        sales = Sale.objects.all()
        
        # Apply filters
        if merchant_id:
            sales = sales.filter(merchant_id=merchant_id)
        if start_date:
            sales = sales.filter(harvest_date__gte=start_date)
        if end_date:
            sales = sales.filter(harvest_date__lte=end_date)
        if status_filter:
            sales = sales.filter(status=status_filter)
        
        # Get summary statistics
        summary_stats = sales.aggregate(
            total_sales=Count('id'),
            total_revenue=Sum('final_amount'),
            avg_sale_amount=Avg('final_amount'),
            max_sale_amount=Max('final_amount'),
            min_sale_amount=Min('final_amount'),
            total_commission=Sum('commission'),
            total_lorry_rent=Sum('lorry_rent'),
            total_cooly_charges=Sum('cooly_charges'),
            total_deductions=Sum('total_deductions')
        )
        
        # Get monthly summary
        monthly_summary = sales.annotate(
            month=TruncMonth('harvest_date')
        ).values('month').annotate(
            sales_count=Count('id'),
            total_revenue=Sum('final_amount'),
            avg_revenue=Avg('final_amount')
        ).order_by('month')
        
        # Get daily summary (last 30 days)
        daily_summary = sales.filter(
            harvest_date__gte=request.GET.get('start_date', '2024-01-01')
        ).annotate(
            date=TruncDate('harvest_date')
        ).values('date').annotate(
            sales_count=Count('id'),
            total_revenue=Sum('final_amount')
        ).order_by('date')
        
        # Get merchant-wise summary
        merchant_summary = sales.values(
            'merchant__name',
            'merchant__id'
        ).annotate(
            sales_count=Count('id'),
            total_revenue=Sum('final_amount'),
            avg_revenue=Avg('final_amount')
        ).order_by('-total_revenue')
        
        # Get status-wise summary
        status_summary = sales.values('status').annotate(
            count=Count('id'),
            total_revenue=Sum('final_amount')
        ).order_by('-count')
        
        # Get payment mode summary
        payment_mode_summary = sales.values('payment_mode').annotate(
            count=Count('id'),
            total_revenue=Sum('final_amount'),
            percentage=Count('id') * 100.0 / sales.count() if sales.count() > 0 else 0
        ).order_by('-count')
        
        # Get crop variant summary
        variant_summary = SaleVariant.objects.filter(
            sale__in=sales
        ).values(
            'crop_variant__crop_variant',
            'crop_variant__crop__crop_name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('total_amount'),
            avg_price_per_unit=Avg('amount_per_unit'),
            sales_count=Count('sale', distinct=True)
        ).order_by('-total_amount')
        
        return Response({
            'status': 'success',
            'message': 'Sale summary retrieved successfully',
            'data': {
                'summary_stats': summary_stats,
                'monthly_summary': list(monthly_summary),
                'daily_summary': list(daily_summary),
                'merchant_summary': list(merchant_summary),
                'status_summary': list(status_summary),
                'payment_mode_summary': list(payment_mode_summary),
                'variant_summary': list(variant_summary)
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_sales_analytics(request):
    """
    Get advanced analytics for sales data
    """
    try:
        from django.db.models import Sum, Count, Avg, F, Q
        from django.db.models.functions import Extract
        from datetime import datetime, timedelta
        
        # Get query parameters
        days = int(request.GET.get('days', 30))  # Default to last 30 days
        merchant_id = request.GET.get('merchant_id')
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Base queryset
        sales = Sale.objects.filter(
            harvest_date__gte=start_date,
            harvest_date__lte=end_date
        )
        
        if merchant_id:
            sales = sales.filter(merchant_id=merchant_id)
        
        # Revenue trends
        revenue_trend = sales.extra(
            select={'day': 'DATE(harvest_date)'}
        ).values('day').annotate(
            revenue=Sum('final_amount'),
            sales_count=Count('id')
        ).order_by('day')
        
        # Top performing merchants
        top_merchants = sales.values(
            'merchant__name',
            'merchant__id'
        ).annotate(
            total_revenue=Sum('final_amount'),
            sales_count=Count('id'),
            avg_sale_value=Avg('final_amount')
        ).order_by('-total_revenue')[:10]
        
        # Commission analysis
        commission_analysis = sales.aggregate(
            total_commission=Sum('commission'),
            avg_commission_rate=Avg(F('commission') / F('total_amount') * 100),
            total_lorry_rent=Sum('lorry_rent'),
            total_cooly_charges=Sum('cooly_charges')
        )
        
        # Sales by hour (to identify peak selling times)
        hourly_sales = sales.annotate(
            hour=Extract('harvest_date', 'hour')
        ).values('hour').annotate(
            sales_count=Count('id'),
            total_revenue=Sum('final_amount')
        ).order_by('hour')
        
        # Profitability analysis
        profitability = sales.aggregate(
            gross_revenue=Sum('total_amount'),
            net_revenue=Sum('final_amount'),
            total_deductions=Sum('total_deductions'),
            profit_margin=Avg(F('final_amount') / F('total_amount') * 100)
        )
        
        return Response({
            'status': 'success',
            'message': 'Sales analytics retrieved successfully',
            'data': {
                'period': f'Last {days} days',
                'revenue_trend': list(revenue_trend),
                'top_merchants': list(top_merchants),
                'commission_analysis': commission_analysis,
                'hourly_sales': list(hourly_sales),
                'profitability': profitability
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)