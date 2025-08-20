from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from ...models import Yield, YieldFarmSegment, YieldVariant, Crop, FarmSegment, CropVariant
from ...serializers import YieldSerializer

@api_view(['POST'])
def save_yield_data(request):
    """
    Save yield data to the database with farm segments and variants
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
        
        # Validate the yield data
        serializer = YieldSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            yield_record = serializer.save()
        
        # Return success response with created data
        response_serializer = YieldSerializer(yield_record)
        return Response({
            'status': 'success',
            'message': 'Yield data saved successfully',
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
def get_all_yields(request):
    """
    Get all yield records from the database
    """
    try:
        # Get query parameters for filtering
        crop_id = request.GET.get('crop_id')
        farm_segment_id = request.GET.get('farm_segment_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Start with all yields
        yields = Yield.objects.select_related('crop').prefetch_related(
            'yield_variants__crop_variant',
            'yield_farm_segments__farm_segment'
        )
        
        # Apply filters
        if crop_id:
            yields = yields.filter(crop_id=crop_id)
        
        if farm_segment_id:
            yields = yields.filter(yield_farm_segments__farm_segment_id=farm_segment_id)
        
        if start_date:
            yields = yields.filter(harvest_date__gte=start_date)
        
        if end_date:
            yields = yields.filter(harvest_date__lte=end_date)
        
        # Order by most recent first
        yields = yields.order_by('-created_at')
        
        serializer = YieldSerializer(yields, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Yields retrieved successfully',
            'data': serializer.data,
            'count': yields.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_yield_by_id(request, yield_id):
    """
    Get a specific yield record by ID
    """
    try:
        yield_record = Yield.objects.select_related('crop').prefetch_related(
            'yield_variants__crop_variant',
            'yield_farm_segments__farm_segment'
        ).get(id=yield_id)
        
        serializer = YieldSerializer(yield_record)
        
        return Response({
            'status': 'success',
            'message': 'Yield retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_yield_data(request, yield_id):
    """
    Update yield data
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        
        # Validate the updated data
        serializer = YieldSerializer(yield_record, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            yield_record = serializer.save()
        
        # Return updated data
        response_serializer = YieldSerializer(yield_record)
        return Response({
            'status': 'success',
            'message': 'Yield updated successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_yield(request, yield_id):
    """
    Delete a yield record
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        
        # Use transaction to ensure related data is also deleted
        with transaction.atomic():
            yield_record.delete()
        
        return Response({
            'status': 'success',
            'message': 'Yield deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_yield_summary(request):
    """
    Get yield summary statistics
    """
    try:
        from django.db.models import Sum, Count, Avg
        from django.db.models.functions import TruncMonth
        
        # Get query parameters
        crop_id = request.GET.get('crop_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        # Base queryset
        yields = Yield.objects.all()
        
        # Apply filters
        if crop_id:
            yields = yields.filter(crop_id=crop_id)
        if start_date:
            yields = yields.filter(harvest_date__gte=start_date)
        if end_date:
            yields = yields.filter(harvest_date__lte=end_date)
        
        # Get summary statistics
        total_yields = yields.count()
        
        # Get monthly summary
        monthly_summary = yields.annotate(
            month=TruncMonth('harvest_date')
        ).values('month').annotate(
            yield_count=Count('id')
        ).order_by('month')
        
        # Get crop-wise summary
        crop_summary = yields.values(
            'crop__crop_name'
        ).annotate(
            yield_count=Count('id')
        ).order_by('-yield_count')
        
        # Get variant quantity summary
        variant_summary = YieldVariant.objects.filter(
            yield_record__in=yields
        ).values(
            'crop_variant__crop_variant',
            'crop_variant__crop__crop_name'
        ).annotate(
            total_quantity=Sum('quantity'),
            avg_quantity=Avg('quantity')
        ).order_by('-total_quantity')
        
        return Response({
            'status': 'success',
            'message': 'Yield summary retrieved successfully',
            'data': {
                'total_yields': total_yields,
                'monthly_summary': list(monthly_summary),
                'crop_summary': list(crop_summary),
                'variant_summary': list(variant_summary)
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)