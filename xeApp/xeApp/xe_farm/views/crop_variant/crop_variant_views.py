from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from ...models import Crop, CropVariant
from ...serializers import CropVariantSerializer

@api_view(['POST'])
def save_crop_variant(request):
    """
    Save crop variant data to the database
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
        
        # Validate the crop variant data
        serializer = CropVariantSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Check if crop variant already exists for this crop
        crop_variant_name = validated_data.get('crop_variant')
        crop_id = validated_data.get('crop').id
        
        existing_variant = CropVariant.objects.filter(
            crop_id=crop_id,
            crop_variant__iexact=crop_variant_name
        ).first()
        
        if existing_variant:
            return Response({
                'status': 'error',
                'message': 'Crop variant already exists for this crop'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create crop variant record
        crop_variant = CropVariant.objects.create(**validated_data)
        
        # Return success response with crop name included
        response_serializer = CropVariantSerializer(crop_variant)
        return Response({
            'status': 'success',
            'message': 'Crop Variant Added Successfully',
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
def get_all_crop_variants(request):
    """
    Get all crop variants from the database
    """
    try:
        crop_variants = CropVariant.objects.select_related('crop').all().order_by('-created_at')
        serializer = CropVariantSerializer(crop_variants, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Crop variants retrieved successfully',
            'data': serializer.data,
            'count': crop_variants.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_crop_variants_by_crop(request, crop_id):
    """
    Get all variants for a specific crop
    """
    try:
        # Check if crop exists
        if not Crop.objects.filter(id=crop_id).exists():
            return Response({
                'status': 'error',
                'message': 'Crop not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        crop_variants = CropVariant.objects.select_related('crop').filter(
            crop_id=crop_id
        ).order_by('-created_at')
        
        serializer = CropVariantSerializer(crop_variants, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Crop variants retrieved successfully',
            'data': serializer.data,
            'count': crop_variants.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_crop_variant_by_id(request, variant_id):
    """
    Get a specific crop variant by ID
    """
    try:
        crop_variant = CropVariant.objects.select_related('crop').get(id=variant_id)
        serializer = CropVariantSerializer(crop_variant)
        
        return Response({
            'status': 'success',
            'message': 'Crop variant retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except CropVariant.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Crop variant not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_crop_variant(request, variant_id):
    """
    Update crop variant data
    """
    try:
        crop_variant = CropVariant.objects.get(id=variant_id)
        
        # Validate the updated data
        serializer = CropVariantSerializer(crop_variant, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if crop variant name already exists for this crop (excluding current variant)
        crop_variant_name = serializer.validated_data.get('crop_variant')
        crop_id = serializer.validated_data.get('crop', crop_variant.crop).id
        
        if crop_variant_name:
            existing_variant = CropVariant.objects.filter(
                crop_id=crop_id,
                crop_variant__iexact=crop_variant_name
            ).exclude(id=variant_id).first()
            
            if existing_variant:
                return Response({
                    'status': 'error',
                    'message': 'Crop variant already exists for this crop'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the updated crop variant
        serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Crop variant updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except CropVariant.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Crop variant not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_crop_variant(request, variant_id):
    """
    Delete a crop variant
    """
    try:
        crop_variant = CropVariant.objects.get(id=variant_id)
        crop_variant.delete()
        
        return Response({
            'status': 'success',
            'message': 'Crop variant deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except CropVariant.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Crop variant not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)