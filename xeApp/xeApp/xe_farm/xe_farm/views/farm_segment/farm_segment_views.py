from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.db.models import Q
from ...models import FarmSegment
from ...serializers import FarmSegmentSerializer

@api_view(['POST'])
def save_farm_segment_data(request):
    """
    Save farm segment data to the database
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
        
        # Validate the farm segment data
        serializer = FarmSegmentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Check if farm name already exists (optional - remove if duplicates are allowed)
        farm_name = validated_data.get('farm_name')
        if farm_name:
            existing_farm = FarmSegment.objects.filter(
                farm_name__iexact=farm_name
            ).first()
            
            if existing_farm:
                return Response({
                    'status': 'error',
                    'message': 'Farm segment with this name already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create farm segment record
        farm_segment = FarmSegment.objects.create(**validated_data)
        
        # Return success response
        response_serializer = FarmSegmentSerializer(farm_segment)
        return Response({
            'status': 'success',
            'message': 'Farm Segment Added Successfully',
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
def get_all_farm_segments(request):
    """
    Get all farm segments from the database
    """
    try:
        farm_segments = FarmSegment.objects.all().order_by('-created_at')
        serializer = FarmSegmentSerializer(farm_segments, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Farm segments retrieved successfully',
            'data': serializer.data,
            'count': farm_segments.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_farm_segments(request):
    """
    Search farm segments by query string
    Supports searching by: farm_name
    Usage: /api/farm-segments/search/?q=searchterm
    """
    try:
        # Get search query from request parameters
        search_query = request.GET.get('q', '').strip()
        
        if not search_query:
            return Response({
                'status': 'error',
                'message': 'Search query parameter "q" is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Search only farm_name field (adjust based on your actual model fields)
        farm_segments = FarmSegment.objects.filter(
            Q(farm_name__icontains=search_query)
        ).order_by('-created_at')
        
        serializer = FarmSegmentSerializer(farm_segments, many=True)
        
        return Response({
            'status': 'success',
            'message': f'Found {farm_segments.count()} farm segment(s)',
            'data': serializer.data,
            'count': farm_segments.count(),
            'query': search_query
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_farm_segment_by_id(request, farm_id):
    """
    Get a specific farm segment by ID
    """
    try:
        farm_segment = FarmSegment.objects.get(id=farm_id)
        serializer = FarmSegmentSerializer(farm_segment)
        
        return Response({
            'status': 'success',
            'message': 'Farm segment retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except FarmSegment.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Farm segment not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_farm_segment_data(request, farm_id):
    """
    Update farm segment data
    """
    try:
        farm_segment = FarmSegment.objects.get(id=farm_id)
        
        # Validate the updated data
        serializer = FarmSegmentSerializer(farm_segment, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if farm name already exists (excluding current farm segment)
        farm_name = serializer.validated_data.get('farm_name')
        if farm_name:
            existing_farm = FarmSegment.objects.filter(
                farm_name__iexact=farm_name
            ).exclude(id=farm_id).first()
            
            if existing_farm:
                return Response({
                    'status': 'error',
                    'message': 'Farm segment with this name already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the updated farm segment
        serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Farm segment updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except FarmSegment.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Farm segment not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_farm_segment(request, farm_id):
    """
    Delete a farm segment
    """
    try:
        farm_segment = FarmSegment.objects.get(id=farm_id)
        farm_segment.delete()
        
        return Response({
            'status': 'success',
            'message': 'Farm segment deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except FarmSegment.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Farm segment not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)