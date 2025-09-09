from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from ...models import Crop
from ...serializers import CropSerializer

@api_view(['POST'])
def save_crop_data(request):
    """
    Save crop data to the database
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
        print(f"Request files: {request.FILES}")
        
        # Validate the crop data (including image if provided)
        serializer = CropSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Check if crop name already exists (optional - remove if duplicates are allowed)
        crop_name = validated_data.get('crop_name')
        if crop_name:
            existing_crop = Crop.objects.filter(
                crop_name__iexact=crop_name
            ).first()
            
            if existing_crop:
                return Response({
                    'status': 'error',
                    'message': 'Crop with this name already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create crop record
        crop = Crop.objects.create(**validated_data)
        
        # Return success response
        response_serializer = CropSerializer(crop)
        return Response({
            'status': 'success',
            'message': 'Crop Added Successfully',
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
def get_all_crops(request):
    """
    Get all crops from the database
    """
    try:
        crops = Crop.objects.all().order_by('-created_at')
        serializer = CropSerializer(crops, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'message': 'Crops retrieved successfully',
            'data': serializer.data,
            'count': crops.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_crop_by_id(request, crop_id):
    """
    Get a specific crop by ID
    """
    try:
        crop = Crop.objects.get(id=crop_id)
        serializer = CropSerializer(crop, context={'request': request})
        
        return Response({
            'status': 'success',
            'message': 'Crop retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Crop.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Crop not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_crop_data(request, crop_id):
    """
    Update crop data
    """
    try:
        crop = Crop.objects.get(id=crop_id)
        
        # Debug logging
        print(f"Update request data: {request.data}")
        print(f"Update request files: {request.FILES}")
        
        # Validate the updated data (including image if provided)
        serializer = CropSerializer(crop, data=request.data, partial=True, context={'request': request})
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if crop name already exists (excluding current crop)
        crop_name = serializer.validated_data.get('crop_name')
        if crop_name:
            existing_crop = Crop.objects.filter(
                crop_name__iexact=crop_name
            ).exclude(id=crop_id).first()
            
            if existing_crop:
                return Response({
                    'status': 'error',
                    'message': 'Crop with this name already exists'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the updated crop
        serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Crop updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Crop.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Crop not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_crop(request, crop_id):
    """
    Delete a crop
    """
    try:
        crop = Crop.objects.get(id=crop_id)
        
        # Delete the crop image file if it exists
        if crop.crop_image:
            try:
                crop.crop_image.delete(save=False)
                print(f"Deleted image file: {crop.crop_image.name}")
            except Exception as img_error:
                print(f"Error deleting image file: {img_error}")
        
        crop.delete()
        
        return Response({
            'status': 'success',
            'message': 'Crop deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Crop.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Crop not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)