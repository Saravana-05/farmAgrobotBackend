from itertools import count
import logging
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json
from ...models import Yield, BillImage, YieldFarmSegment, YieldVariant, Crop, FarmSegment, CropVariant
from ...serializers import (
    YieldSerializer, BillImageSerializer, BillImageUploadSerializer,
    YieldSummarySerializer
)

logger = logging.getLogger(__name__)


# Add this enhanced debugging to your save_yield_data function
@api_view(['POST'])
def save_yield_data(request):
    try:
        # ENHANCED DEBUGGING
        logger.info("=== DEBUGGING FILE UPLOAD ===")
        logger.info(f"request.FILES keys: {list(request.FILES.keys())}")
        logger.info(f"request.FILES count: {len(request.FILES)}")
        
        for key, file in request.FILES.items():
            logger.info(f"File key: '{key}', filename: '{file.name}', size: {file.size}")
            
        logger.info(f"request.POST keys: {list(request.POST.keys()) if hasattr(request, 'POST') else 'No POST'}")
        logger.info(f"request.data keys: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'No data keys'}")
        logger.info("=== END DEBUG INFO ===")

        if not request.data and not request.FILES:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Handle multipart form data vs JSON data
        if request.content_type and 'multipart/form-data' in request.content_type:
            yield_data = {}
            for key, value in request.POST.items():
                yield_data[key] = value
        else:
            yield_data = request.data.copy()

        # Parse JSON strings
        for field in ['variants', 'farm_segments']:
            if field in yield_data:
                if isinstance(yield_data[field], str):
                    try:
                        yield_data[field] = json.loads(yield_data[field])
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse {field}: {e}")
                        yield_data[field] = []
                elif not isinstance(yield_data[field], list):
                    yield_data[field] = []

        # Validate required fields
        required_fields = ['crop', 'harvest_date']
        missing_fields = [field for field in required_fields if field not in yield_data or not yield_data[field]]
        
        if missing_fields:
            return Response({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'missing_fields': missing_fields
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate variants
        if 'variants' in yield_data and yield_data['variants']:
            for i, variant in enumerate(yield_data['variants']):
                if not isinstance(variant, dict):
                    return Response({
                        'status': 'error',
                        'message': f'Variant {i+1}: Must be an object with crop_variant_id, unit, and quantity'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                required_variant_fields = ['crop_variant_id', 'unit', 'quantity']
                missing_variant_fields = [field for field in required_variant_fields 
                                        if field not in variant or variant[field] is None or variant[field] == '']
                
                if missing_variant_fields:
                    return Response({
                        'status': 'error',
                        'message': f'Variant {i+1}: Missing fields {", ".join(missing_variant_fields)}'
                    }, status=status.HTTP_400_BAD_REQUEST)

        # IMPROVED FILE HANDLING
        uploaded_files = []
        if request.FILES:
            logger.info("Processing uploaded files...")
            for key, file in request.FILES.items():
                logger.info(f"Processing file key: '{key}'")
                
                # More flexible keyword matching
                if any(keyword in key.lower() for keyword in ['bill', 'image', 'file', 'upload']):
                    uploaded_files.append(file)
                    logger.info(f"Added file: {file.name} (key: {key})")
                else:
                    logger.warning(f"Skipped file with key '{key}' - doesn't match keywords")
        
        logger.info(f"Total files to process: {len(uploaded_files)}")

        # Validate with serializer
        serializer = YieldSerializer(data=yield_data, context={'request': request})
        if not serializer.is_valid():
            logger.error(f"Yield validation errors: {serializer.errors}")
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Save data with SEPARATE transaction for images to avoid rollback
        yield_record = serializer.save()
        logger.info(f"Yield record created with ID: {yield_record.id}")

        # Upload images OUTSIDE the main transaction to prevent rollback
        uploaded_images = []
        failed_uploads = []
        
        for i, file in enumerate(uploaded_files):
            try:
                logger.info(f"Uploading image {i+1}/{len(uploaded_files)}: {file.name}")
                
                bill_image = BillImage.objects.create(
                    yield_record=yield_record,
                    image=file,
                    original_filename=file.name
                )
                uploaded_images.append(bill_image)
                logger.info(f"Successfully uploaded: {bill_image.image.url}")
                
            except Exception as upload_error:
                error_msg = f"Failed to upload {file.name}: {str(upload_error)}"
                logger.error(error_msg)
                failed_uploads.append(error_msg)
                continue

        # Prepare response message
        success_count = len(uploaded_images)
        failed_count = len(failed_uploads)
        
        message = f'Yield created successfully with {success_count} images'
        if failed_count > 0:
            message += f' ({failed_count} failed uploads)'

        response_data = {
            'status': 'success',
            'message': message,
            'data': YieldSerializer(yield_record, context={'request': request}).data,
            'upload_summary': {
                'total_attempted': len(uploaded_files),
                'successful': success_count,
                'failed': failed_count,
                'failed_uploads': failed_uploads if failed_uploads else None
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return Response({
            'status': 'error', 
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
        return Response({
            'status': 'error', 
            'message': 'Database integrity error occurred'
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error', 
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_yields(request):
    try:
        crop_id = request.GET.get('crop_id')
        farm_segment_id = request.GET.get('farm_segment_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        has_bills = request.GET.get('has_bills')

        yields = Yield.objects.select_related('crop').prefetch_related(
            'yield_variants__crop_variant',
            'yield_farm_segments__farm_segment',
            'bill_images'
        )

        if crop_id:
            yields = yields.filter(crop_id=crop_id)

        if farm_segment_id:
            yields = yields.filter(yield_farm_segments__farm_segment_id=farm_segment_id)

        if start_date:
            yields = yields.filter(harvest_date__gte=start_date)

        if end_date:
            yields = yields.filter(harvest_date__lte=end_date)

        if has_bills is not None:
            yields = yields.annotate(bill_count=count('bill_images'))
            if has_bills.lower() == 'true':
                yields = yields.filter(bill_count__gt=0)
            elif has_bills.lower() == 'false':
                yields = yields.filter(bill_count=0)

        yields = yields.order_by('-created_at').distinct()

        page_size = request.GET.get('page_size')
        page = request.GET.get('page')

        if page_size and page:
            try:
                page_size = int(page_size)
                page = int(page)
                start = (page - 1) * page_size
                end = start + page_size
                yields = yields[start:end]
            except (ValueError, TypeError):
                pass

        serializer = YieldSerializer(yields, many=True, context={'request': request})

        return Response({
            'status': 'success',
            'message': 'Yields retrieved successfully',
            'data': serializer.data,
            'count': len(serializer.data)
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Server error: {e}")
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
            'yield_farm_segments__farm_segment',
            'bill_images'
        ).get(id=yield_id)
        
        serializer = YieldSerializer(yield_record, context={'request': request})
        
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
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_yield_data(request, yield_id):
    """
    Update yield data WITH support for multiple image uploads
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        
        # ENHANCED DEBUGGING for updates
        logger.info("=== DEBUGGING UPDATE WITH FILES ===")
        logger.info(f"request.FILES keys: {list(request.FILES.keys())}")
        logger.info(f"request.FILES count: {len(request.FILES)}")
        
        for key, file in request.FILES.items():
            logger.info(f"Update File key: '{key}', filename: '{file.name}', size: {file.size}")
            
        logger.info(f"request.data keys: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'No data keys'}")
        logger.info("=== END UPDATE DEBUG INFO ===")

        # Handle multipart form data vs JSON data (same as create)
        if request.content_type and 'multipart/form-data' in request.content_type:
            yield_data = {}
            for key, value in request.POST.items():
                yield_data[key] = value
        else:
            yield_data = request.data.copy()

        # Parse JSON strings for variants and farm_segments
        for field in ['variants', 'farm_segments']:
            if field in yield_data:
                if isinstance(yield_data[field], str):
                    try:
                        yield_data[field] = json.loads(yield_data[field])
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse {field}: {e}")
                        yield_data[field] = []
                elif not isinstance(yield_data[field], list):
                    yield_data[field] = []

        # Handle file uploads during update
        uploaded_files = []
        replace_images = request.data.get('replace_images', 'false').lower() == 'true'
        
        if request.FILES:
            logger.info("Processing uploaded files during update...")
            for key, file in request.FILES.items():
                logger.info(f"Processing update file key: '{key}'")
                
                # More flexible keyword matching
                if any(keyword in key.lower() for keyword in ['bill', 'image', 'file', 'upload']):
                    uploaded_files.append(file)
                    logger.info(f"Added update file: {file.name} (key: {key})")
                else:
                    logger.warning(f"Skipped update file with key '{key}' - doesn't match keywords")
        
        logger.info(f"Total update files to process: {len(uploaded_files)}")

        # Validate the updated data (exclude file handling from serializer)
        serializer = YieldSerializer(yield_record, data=yield_data, partial=True, 
                                   context={'request': request})
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the record in transaction
        with transaction.atomic():
            yield_record = serializer.save()
            
            # Handle image updates if files are provided
            if uploaded_files:
                current_image_count = yield_record.bill_images.count()
                
                if replace_images:
                    # Replace all existing images
                    logger.info("Replacing all existing images...")
                    yield_record.bill_images.all().delete()
                    max_new_images = 10
                else:
                    # Add to existing images
                    max_new_images = 10 - current_image_count
                    if max_new_images <= 0:
                        return Response({
                            'status': 'error',
                            'message': f'Cannot add more images. Current count: {current_image_count}, maximum allowed: 10'
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                # Limit files to upload
                files_to_upload = uploaded_files[:max_new_images]
                if len(uploaded_files) > max_new_images:
                    logger.warning(f"Limiting upload to {max_new_images} files out of {len(uploaded_files)} provided")
                
                # Upload new images
                uploaded_images = []
                failed_uploads = []
                
                for i, file in enumerate(files_to_upload):
                    try:
                        logger.info(f"Uploading update image {i+1}/{len(files_to_upload)}: {file.name}")
                        
                        # Validate image
                        upload_serializer = BillImageUploadSerializer(data={
                            'image': file,
                            'original_filename': file.name
                        })
                        
                        if upload_serializer.is_valid():
                            bill_image = BillImage.objects.create(
                                yield_record=yield_record,
                                image=file,
                                original_filename=file.name
                            )
                            uploaded_images.append(bill_image)
                            logger.info(f"Successfully uploaded update image: {bill_image.image.url}")
                        else:
                            error_msg = f"Invalid image {file.name}: {upload_serializer.errors}"
                            logger.error(error_msg)
                            failed_uploads.append(error_msg)
                            
                    except Exception as upload_error:
                        error_msg = f"Failed to upload {file.name}: {str(upload_error)}"
                        logger.error(error_msg)
                        failed_uploads.append(error_msg)
                        continue
        
        # Prepare response message
        message = 'Yield updated successfully'
        if uploaded_files:
            success_count = len(uploaded_images) if 'uploaded_images' in locals() else 0
            failed_count = len(failed_uploads) if 'failed_uploads' in locals() else 0
            
            if replace_images:
                message += f' with {success_count} replacement images'
            else:
                message += f' with {success_count} additional images'
                
            if failed_count > 0:
                message += f' ({failed_count} failed uploads)'
        
        # Return updated data with upload summary
        response_serializer = YieldSerializer(yield_record, context={'request': request})
        response_data = {
            'status': 'success',
            'message': message,
            'data': response_serializer.data
        }
        
        # Add upload summary if files were processed
        if uploaded_files:
            response_data['upload_summary'] = {
                'total_attempted': len(uploaded_files),
                'successful': len(uploaded_images) if 'uploaded_images' in locals() else 0,
                'failed': len(failed_uploads) if 'failed_uploads' in locals() else 0,
                'failed_uploads': failed_uploads if 'failed_uploads' in locals() and failed_uploads else None,
                'replace_mode': replace_images
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Server error in update: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])  
def update_yield_with_image_options(request, yield_id):
    """
    Enhanced update endpoint with explicit image handling options
    Supports: update_mode = 'add' | 'replace' | 'keep'
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        
        # Get image handling mode from request
        update_mode = request.data.get('image_update_mode', 'add').lower()
        valid_modes = ['add', 'replace', 'keep']
        
        if update_mode not in valid_modes:
            return Response({
                'status': 'error',
                'message': f'Invalid image_update_mode. Must be one of: {", ".join(valid_modes)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Update mode: {update_mode}")
        
        # Handle form data
        if request.content_type and 'multipart/form-data' in request.content_type:
            yield_data = {}
            for key, value in request.POST.items():
                if key != 'image_update_mode':  # Exclude mode from yield data
                    yield_data[key] = value
        else:
            yield_data = request.data.copy()
            yield_data.pop('image_update_mode', None)  # Remove mode from yield data

        # Parse JSON strings
        for field in ['variants', 'farm_segments']:
            if field in yield_data:
                if isinstance(yield_data[field], str):
                    try:
                        yield_data[field] = json.loads(yield_data[field])
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse {field}: {e}")
                        yield_data[field] = []

        # Collect uploaded files
        uploaded_files = []
        if request.FILES and update_mode != 'keep':
            for key, file in request.FILES.items():
                if any(keyword in key.lower() for keyword in ['bill', 'image', 'file', 'upload']):
                    uploaded_files.append(file)
                    logger.info(f"Found file for {update_mode}: {file.name}")

        # Validate yield data
        serializer = YieldSerializer(yield_record, data=yield_data, partial=True, 
                                   context={'request': request})
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Perform update with transaction
        with transaction.atomic():
            # Update yield record
            yield_record = serializer.save()
            
            uploaded_images = []
            failed_uploads = []
            
            # Handle images based on mode
            if update_mode == 'replace' and uploaded_files:
                # Replace all images
                logger.info(f"Replacing all images with {len(uploaded_files)} new files")
                yield_record.bill_images.all().delete()
                
                files_to_upload = uploaded_files[:10]  # Limit to 10
                for file in files_to_upload:
                    try:
                        bill_image = BillImage.objects.create(
                            yield_record=yield_record,
                            image=file,
                            original_filename=file.name
                        )
                        uploaded_images.append(bill_image)
                    except Exception as e:
                        failed_uploads.append(f"Failed to upload {file.name}: {str(e)}")
                        
            elif update_mode == 'add' and uploaded_files:
                # Add to existing images
                current_count = yield_record.bill_images.count()
                max_additional = 10 - current_count
                
                if max_additional <= 0:
                    return Response({
                        'status': 'error',
                        'message': f'Cannot add images. Already at maximum (10). Current count: {current_count}'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                files_to_upload = uploaded_files[:max_additional]
                logger.info(f"Adding {len(files_to_upload)} images to existing {current_count}")
                
                for file in files_to_upload:
                    try:
                        bill_image = BillImage.objects.create(
                            yield_record=yield_record,
                            image=file,
                            original_filename=file.name
                        )
                        uploaded_images.append(bill_image)
                    except Exception as e:
                        failed_uploads.append(f"Failed to upload {file.name}: {str(e)}")
            
            # Mode 'keep' doesn't change images

        # Prepare response
        success_count = len(uploaded_images)
        message = f'Yield updated successfully'
        
        if update_mode == 'replace' and uploaded_files:
            message += f' with {success_count} replacement images'
        elif update_mode == 'add' and uploaded_files:
            message += f' with {success_count} additional images'
        elif update_mode == 'keep':
            message += ' (images unchanged)'
            
        if failed_uploads:
            message += f' ({len(failed_uploads)} failed uploads)'

        response_serializer = YieldSerializer(yield_record, context={'request': request})
        response_data = {
            'status': 'success',
            'message': message,
            'data': response_serializer.data,
            'image_update_mode': update_mode
        }
        
        if uploaded_files:
            response_data['upload_summary'] = {
                'total_attempted': len(uploaded_files),
                'successful': success_count,
                'failed': len(failed_uploads),
                'failed_uploads': failed_uploads if failed_uploads else None
            }

        return Response(response_data, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Server error in enhanced update: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_bill_image(request, yield_id):
    """
    Add bill images to an existing yield record
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        
        # Check current image count
        current_count = yield_record.bill_images.count()
        if current_count >= 10:
            return Response({
                'status': 'error',
                'message': 'Maximum 10 bill images allowed per yield'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle multiple file uploads
        uploaded_files = []
        for key, file in request.FILES.items():
            if any(keyword in key.lower() for keyword in ['bill', 'image']):
                uploaded_files.append(file)
        
        if not uploaded_files:
            return Response({
                'status': 'error',
                'message': 'No image files provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if adding these files would exceed limit
        if current_count + len(uploaded_files) > 10:
            return Response({
                'status': 'error',
                'message': f'Cannot add {len(uploaded_files)} images. '
                          f'Would exceed maximum limit (current: {current_count}, max: 10)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Upload images
        uploaded_images = []
        with transaction.atomic():
            for file in uploaded_files:
                try:
                    # Validate image
                    upload_serializer = BillImageUploadSerializer(data={
                        'image': file,
                        'original_filename': file.name
                    })
                    
                    if upload_serializer.is_valid():
                        bill_image = BillImage.objects.create(
                            yield_record=yield_record,
                            image=file,
                            original_filename=file.name
                        )
                        uploaded_images.append(bill_image)
                        logger.info(f"Added bill image: {bill_image.image.url}")
                    else:
                        logger.warning(f"Invalid image file {file.name}: {upload_serializer.errors}")
                        
                except Exception as upload_error:
                    logger.error(f"Failed to upload {file.name}: {upload_error}")
                    continue
        
        if not uploaded_images:
            return Response({
                'status': 'error',
                'message': 'Failed to upload any images'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Return updated yield data
        response_serializer = YieldSerializer(yield_record, context={'request': request})
        return Response({
            'status': 'success',
            'message': f'Successfully added {len(uploaded_images)} bill images',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def remove_bill_image(request, yield_id, image_id):
    """
    Remove a specific bill image from a yield record
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        bill_image = yield_record.bill_images.get(id=image_id)
        
        # Delete the image (this will also delete the file)
        bill_image.delete()
        
        # Return updated yield data
        response_serializer = YieldSerializer(yield_record, context={'request': request})
        return Response({
            'status': 'success',
            'message': 'Bill image removed successfully',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except BillImage.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Bill image not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_yield(request, yield_id):
    """
    Delete a yield record and all associated bill images
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        
        # Use transaction for atomic deletion
        with transaction.atomic():
            # Delete all bill images (files will be deleted automatically via model's delete method)
            yield_record.bill_images.all().delete()
            
            # Delete the yield record (related objects will cascade)
            yield_record.delete()
        
        return Response({
            'status': 'success',
            'message': 'Yield and all associated data deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_yield_summary(request):
    """
    Get yield summary statistics with bill image information
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
        total_bills = BillImage.objects.filter(yield_record__in=yields).count()
        
        # Get monthly summary
        monthly_summary = yields.annotate(
            month=TruncMonth('harvest_date')
        ).values('month').annotate(
            yield_count=Count('id'),
            bill_count=Count('bill_images')
        ).order_by('month')
        
        # Get crop-wise summary
        crop_summary = yields.values(
            'crop__crop_name'
        ).annotate(
            yield_count=Count('id'),
            bill_count=Count('bill_images')
        ).order_by('-yield_count')
        
        # Get variant quantity summary
        variant_summary = YieldVariant.objects.filter(
            yield_record__in=yields
        ).values(
            'crop_variant__crop_variant',
            'crop_variant__crop__crop_name'
        ).annotate(
            total_quantity=Sum('quantity'),
            avg_quantity=Avg('quantity'),
            yield_count=Count('yield_record', distinct=True)
        ).order_by('-total_quantity')
        
        return Response({
            'status': 'success',
            'message': 'Yield summary retrieved successfully',
            'data': {
                'total_yields': total_yields,
                'total_bills': total_bills,
                'monthly_summary': list(monthly_summary),
                'crop_summary': list(crop_summary),
                'variant_summary': list(variant_summary)
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_bill_images(request, yield_id):
    """
    Get all bill images for a specific yield
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        bill_images = yield_record.bill_images.all().order_by('uploaded_at')
        
        serializer = BillImageSerializer(bill_images, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'message': 'Bill images retrieved successfully',
            'data': serializer.data,
            'count': len(serializer.data)
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def replace_bill_images(request, yield_id):
    """
    Replace all bill images for a yield with new ones
    """
    try:
        yield_record = Yield.objects.get(id=yield_id)
        
        # Handle file uploads
        uploaded_files = []
        for key, file in request.FILES.items():
            if any(keyword in key.lower() for keyword in ['bill', 'image']):
                uploaded_files.append(file)
        
        if not uploaded_files:
            return Response({
                'status': 'error',
                'message': 'No image files provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(uploaded_files) > 10:
            return Response({
                'status': 'error',
                'message': 'Maximum 10 images allowed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Replace images in transaction
        with transaction.atomic():
            # Delete existing images
            yield_record.bill_images.all().delete()
            
            # Upload new images
            uploaded_images = []
            for file in uploaded_files:
                try:
                    upload_serializer = BillImageUploadSerializer(data={
                        'image': file,
                        'original_filename': file.name
                    })
                    
                    if upload_serializer.is_valid():
                        bill_image = BillImage.objects.create(
                            yield_record=yield_record,
                            image=file,
                            original_filename=file.name
                        )
                        uploaded_images.append(bill_image)
                    else:
                        logger.warning(f"Invalid image file {file.name}: {upload_serializer.errors}")
                        
                except Exception as upload_error:
                    logger.error(f"Failed to upload {file.name}: {upload_error}")
                    continue
        
        if not uploaded_images:
            return Response({
                'status': 'error',
                'message': 'Failed to upload any images'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Return updated yield data
        response_serializer = YieldSerializer(yield_record, context={'request': request})
        return Response({
            'status': 'success',
            'message': f'Successfully replaced with {len(uploaded_images)} bill images',
            'data': response_serializer.data
        }, status=status.HTTP_200_OK)
        
    except Yield.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Yield record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Additional utility view for bulk operations
@api_view(['POST'])
def bulk_delete_yields(request):
    """
    Delete multiple yields in bulk
    """
    try:
        yield_ids = request.data.get('yield_ids', [])
        
        if not yield_ids or not isinstance(yield_ids, list):
            return Response({
                'status': 'error',
                'message': 'yield_ids must be a non-empty list'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction for atomic bulk deletion
        with transaction.atomic():
            # Get yields to delete
            yields_to_delete = Yield.objects.filter(id__in=yield_ids)
            actual_count = yields_to_delete.count()
            
            if actual_count == 0:
                return Response({
                    'status': 'error',
                    'message': 'No yields found with the provided IDs'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Delete all related bill images first (files will be deleted automatically)
            BillImage.objects.filter(yield_record__in=yields_to_delete).delete()
            
            # Delete the yields (other related objects will cascade)
            yields_to_delete.delete()
        
        return Response({
            'status': 'success',
            'message': f'Successfully deleted {actual_count} yields and all associated data',
            'deleted_count': actual_count
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Server error in bulk delete: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_crop_dashboard(request):
    """
    Get crop dashboard data with quantities and units for different time periods
    Supports filtering by crop_id, farm_segment_id, and custom date ranges
    """
    try:
        from django.db.models import Sum, Count, Q
        from django.utils import timezone
        from datetime import datetime, timedelta
        import calendar
        
        # Get query parameters
        crop_id = request.GET.get('crop_id')
        farm_segment_id = request.GET.get('farm_segment_id')
        
        # Get current date and calculate time ranges
        now = timezone.now()
        today = now.date()
        
        # Current week (Monday to Sunday)
        current_week_start = today - timedelta(days=today.weekday())
        current_week_end = current_week_start + timedelta(days=6)
        
        # Current month
        current_month_start = today.replace(day=1)
        current_month_end = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        
        # Last month
        last_month_date = (current_month_start - timedelta(days=1))
        last_month_start = last_month_date.replace(day=1)
        last_month_end = last_month_date.replace(day=calendar.monthrange(last_month_date.year, last_month_date.month)[1])
        
        # Current year
        current_year_start = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)
        
        logger.info(f"Dashboard date ranges - Current week: {current_week_start} to {current_week_end}, "
                   f"Current month: {current_month_start} to {current_month_end}, "
                   f"Last month: {last_month_start} to {last_month_end}, "
                   f"Current year: {current_year_start} to {current_year_end}")
        
        # Base queryset for yields
        base_yields = Yield.objects.select_related('crop').prefetch_related(
            'yield_variants__crop_variant'
        )
        
        # Apply filters
        if crop_id:
            base_yields = base_yields.filter(crop_id=crop_id)
        
        if farm_segment_id:
            base_yields = base_yields.filter(yield_farm_segments__farm_segment_id=farm_segment_id)
        
        def get_crop_data_for_period(yields_queryset, period_name):
            """Helper function to get crop data for a specific period"""
            # Get yield variants with crop and variant information
            variants_data = YieldVariant.objects.filter(
                yield_record__in=yields_queryset
            ).select_related(
                'crop_variant__crop', 'yield_record'
            ).values(
                'crop_variant__crop__id',
                'crop_variant__crop__crop_name',
                'crop_variant__crop_variant',
                'unit'
            ).annotate(
                total_quantity=Sum('quantity'),
                yield_count=Count('yield_record', distinct=True)
            ).order_by('crop_variant__crop__crop_name', 'crop_variant__crop_variant')
            
            # Group data by crop
            crops_summary = {}
            total_yields = yields_queryset.count()
            
            for variant in variants_data:
                crop_id = variant['crop_variant__crop__id']
                crop_name = variant['crop_variant__crop__crop_name']
                
                if crop_id not in crops_summary:
                    crops_summary[crop_id] = {
                        'crop_id': crop_id,
                        'crop_name': crop_name,
                        'variants': [],
                        'total_yield_records': 0,
                        'unique_units': set()
                    }
                
                # Add variant data
                crops_summary[crop_id]['variants'].append({
                    'variant_name': variant['crop_variant__crop_variant'],
                    'unit': variant['unit'],
                    'total_quantity': float(variant['total_quantity'] or 0),
                    'yield_count': variant['yield_count']
                })
                
                crops_summary[crop_id]['total_yield_records'] += variant['yield_count']
                crops_summary[crop_id]['unique_units'].add(variant['unit'])
            
            # Convert sets to lists and calculate summaries
            for crop_data in crops_summary.values():
                crop_data['unique_units'] = list(crop_data['unique_units'])
                
                # Calculate total quantity per unit
                unit_totals = {}
                for variant in crop_data['variants']:
                    unit = variant['unit']
                    if unit not in unit_totals:
                        unit_totals[unit] = 0
                    unit_totals[unit] += variant['total_quantity']
                
                crop_data['unit_wise_totals'] = [
                    {'unit': unit, 'total_quantity': quantity}
                    for unit, quantity in unit_totals.items()
                ]
            
            return {
                'period': period_name,
                'total_yield_records': total_yields,
                'crops': list(crops_summary.values())
            }
        
        # Get data for each time period
        dashboard_data = {}
        
        # Current week data
        current_week_yields = base_yields.filter(
            harvest_date__gte=current_week_start,
            harvest_date__lte=current_week_end
        )
        dashboard_data['current_week'] = get_crop_data_for_period(current_week_yields, 'Current Week')
        
        # Current month data
        current_month_yields = base_yields.filter(
            harvest_date__gte=current_month_start,
            harvest_date__lte=current_month_end
        )
        dashboard_data['current_month'] = get_crop_data_for_period(current_month_yields, 'Current Month')
        
        # Last month data
        last_month_yields = base_yields.filter(
            harvest_date__gte=last_month_start,
            harvest_date__lte=last_month_end
        )
        dashboard_data['last_month'] = get_crop_data_for_period(last_month_yields, 'Last Month')
        
        # Current year data
        current_year_yields = base_yields.filter(
            harvest_date__gte=current_year_start,
            harvest_date__lte=current_year_end
        )
        dashboard_data['current_year'] = get_crop_data_for_period(current_year_yields, 'Current Year')
        
        # Get overall statistics
        overall_stats = {
            'total_crops': Crop.objects.count(),
            'total_yield_records': base_yields.count(),
            'date_range_info': {
                'current_week': f"{current_week_start} to {current_week_end}",
                'current_month': f"{current_month_start} to {current_month_end}",
                'last_month': f"{last_month_start} to {last_month_end}",
                'current_year': f"{current_year_start} to {current_year_end}"
            }
        }
        
        # Add filters info if applied
        filters_applied = {}
        if crop_id:
            try:
                crop = Crop.objects.get(id=crop_id)
                filters_applied['crop'] = {'id': crop_id, 'name': crop.crop_name}
            except Crop.DoesNotExist:
                pass
                
        if farm_segment_id:
            try:
                segment = FarmSegment.objects.get(id=farm_segment_id)
                filters_applied['farm_segment'] = {'id': farm_segment_id, 'name': segment.segment_name}
            except FarmSegment.DoesNotExist:
                pass
        
        if filters_applied:
            overall_stats['filters_applied'] = filters_applied
        
        return Response({
            'status': 'success',
            'message': 'Crop dashboard data retrieved successfully',
            'data': {
                'overall_stats': overall_stats,
                'periods': dashboard_data
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Server error in crop dashboard: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_crop_comparison_dashboard(request):
    """
    Get crop comparison dashboard showing quantity trends across time periods
    """
    try:
        from django.db.models import Sum, Count, Q
        from django.utils import timezone
        from datetime import datetime, timedelta
        import calendar
        
        # Get query parameters
        compare_crops = request.GET.get('compare_crops')  # comma-separated crop IDs
        farm_segment_id = request.GET.get('farm_segment_id')
        
        # Parse crop IDs for comparison
        crop_ids = []
        if compare_crops:
            try:
                crop_ids = [int(x.strip()) for x in compare_crops.split(',')]
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid crop IDs format. Use comma-separated integers.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get time ranges (same as dashboard)
        now = timezone.now()
        today = now.date()
        
        current_week_start = today - timedelta(days=today.weekday())
        current_week_end = current_week_start + timedelta(days=6)
        
        current_month_start = today.replace(day=1)
        current_month_end = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        
        last_month_date = (current_month_start - timedelta(days=1))
        last_month_start = last_month_date.replace(day=1)
        last_month_end = last_month_date.replace(day=calendar.monthrange(last_month_date.year, last_month_date.month)[1])
        
        current_year_start = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)
        
        # Base queryset
        base_yields = Yield.objects.select_related('crop').prefetch_related(
            'yield_variants__crop_variant'
        )
        
        # Apply filters
        if crop_ids:
            base_yields = base_yields.filter(crop_id__in=crop_ids)
        
        if farm_segment_id:
            base_yields = base_yields.filter(yield_farm_segments__farm_segment_id=farm_segment_id)
        
        def get_comparison_data(yields_queryset, period_name):
            """Get comparison data for a specific period"""
            comparison_data = YieldVariant.objects.filter(
                yield_record__in=yields_queryset
            ).select_related(
                'crop_variant__crop'
            ).values(
                'crop_variant__crop__id',
                'crop_variant__crop__crop_name'
            ).annotate(
                total_quantity=Sum('quantity'),
                yield_count=Count('yield_record', distinct=True),
                variant_count=Count('id')
            ).order_by('crop_variant__crop__crop_name')
            
            # Also get unit-wise breakdown
            unit_breakdown = YieldVariant.objects.filter(
                yield_record__in=yields_queryset
            ).select_related(
                'crop_variant__crop'
            ).values(
                'crop_variant__crop__id',
                'crop_variant__crop__crop_name',
                'unit'
            ).annotate(
                quantity_in_unit=Sum('quantity'),
                variant_count=Count('id')
            ).order_by('crop_variant__crop__crop_name', 'unit')
            
            # Combine the data
            crops_data = {}
            for item in comparison_data:
                crop_id = item['crop_variant__crop__id']
                crops_data[crop_id] = {
                    'crop_id': crop_id,
                    'crop_name': item['crop_variant__crop__crop_name'],
                    'total_quantity': float(item['total_quantity'] or 0),
                    'yield_count': item['yield_count'],
                    'variant_count': item['variant_count'],
                    'units': []
                }
            
            # Add unit breakdown
            for item in unit_breakdown:
                crop_id = item['crop_variant__crop__id']
                if crop_id in crops_data:
                    crops_data[crop_id]['units'].append({
                        'unit': item['unit'],
                        'quantity': float(item['quantity_in_unit'] or 0),
                        'variant_count': item['variant_count']
                    })
            
            return {
                'period': period_name,
                'crops': list(crops_data.values())
            }
        
        # Get comparison data for all periods
        comparison_data = {}
        
        # Current week
        current_week_yields = base_yields.filter(
            harvest_date__gte=current_week_start,
            harvest_date__lte=current_week_end
        )
        comparison_data['current_week'] = get_comparison_data(current_week_yields, 'Current Week')
        
        # Current month
        current_month_yields = base_yields.filter(
            harvest_date__gte=current_month_start,
            harvest_date__lte=current_month_end
        )
        comparison_data['current_month'] = get_comparison_data(current_month_yields, 'Current Month')
        
        # Last month
        last_month_yields = base_yields.filter(
            harvest_date__gte=last_month_start,
            harvest_date__lte=last_month_end
        )
        comparison_data['last_month'] = get_comparison_data(last_month_yields, 'Last Month')
        
        # Current year
        current_year_yields = base_yields.filter(
            harvest_date__gte=current_year_start,
            harvest_date__lte=current_year_end
        )
        comparison_data['current_year'] = get_comparison_data(current_year_yields, 'Current Year')
        
        # Get crop metadata if specific crops are being compared
        crop_metadata = []
        if crop_ids:
            crops = Crop.objects.filter(id__in=crop_ids).values('id', 'crop_name')
            crop_metadata = list(crops)
        
        return Response({
            'status': 'success',
            'message': 'Crop comparison dashboard data retrieved successfully',
            'data': {
                'crop_metadata': crop_metadata,
                'comparison_periods': comparison_data,
                'filters_applied': {
                    'compare_crops': crop_ids if crop_ids else None,
                    'farm_segment_id': farm_segment_id
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Server error in crop comparison dashboard: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_crop_performance_metrics(request):
    """
    Get detailed crop performance metrics including growth trends and efficiency
    """
    try:
        from django.db.models import Sum, Count, Avg, Min, Max
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        crop_id = request.GET.get('crop_id')
        months_back = int(request.GET.get('months_back', 6))  # Default 6 months
        
        if not crop_id:
            return Response({
                'status': 'error',
                'message': 'crop_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate crop exists
        try:
            crop = Crop.objects.get(id=crop_id)
        except Crop.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Crop not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate date range
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30 * months_back)
        
        # Get yields for this crop
        yields = Yield.objects.filter(
            crop_id=crop_id,
            harvest_date__gte=start_date,
            harvest_date__lte=end_date
        ).prefetch_related('yield_variants__crop_variant')
        
        # Monthly aggregation
        from django.db.models.functions import TruncMonth
        monthly_performance = yields.annotate(
            month=TruncMonth('harvest_date')
        ).values('month').annotate(
            yield_count=Count('id'),
            total_variants=Count('yield_variants')
        ).order_by('month')
        
        # Get variant-wise performance
        variant_performance = YieldVariant.objects.filter(
            yield_record__crop_id=crop_id,
            yield_record__harvest_date__gte=start_date,
            yield_record__harvest_date__lte=end_date
        ).select_related('crop_variant').values(
            'crop_variant__crop_variant',
            'unit'
        ).annotate(
            total_quantity=Sum('quantity'),
            avg_quantity=Avg('quantity'),
            min_quantity=Min('quantity'),
            max_quantity=Max('quantity'),
            yield_count=Count('yield_record', distinct=True)
        ).order_by('-total_quantity')
        
        # Calculate growth trends
        recent_yields = yields.filter(
            harvest_date__gte=end_date - timedelta(days=30)
        ).count()
        
        previous_yields = yields.filter(
            harvest_date__gte=end_date - timedelta(days=60),
            harvest_date__lt=end_date - timedelta(days=30)
        ).count()
        
        growth_trend = {
            'recent_month': recent_yields,
            'previous_month': previous_yields,
            'growth_percentage': ((recent_yields - previous_yields) / previous_yields * 100) if previous_yields > 0 else 0
        }
        
        # Get top performing variants
        top_variants = list(variant_performance[:5])  # Top 5 variants
        
        # Overall statistics
        overall_stats = {
            'crop_name': crop.crop_name,
            'total_yields': yields.count(),
            'date_range': f"{start_date} to {end_date}",
            'unique_variants': YieldVariant.objects.filter(
                yield_record__crop_id=crop_id,
                yield_record__harvest_date__gte=start_date
            ).values('crop_variant').distinct().count(),
            'total_quantity_all_units': YieldVariant.objects.filter(
                yield_record__crop_id=crop_id,
                yield_record__harvest_date__gte=start_date
            ).aggregate(total=Sum('quantity'))['total'] or 0
        }
        
        return Response({
            'status': 'success',
            'message': 'Crop performance metrics retrieved successfully',
            'data': {
                'crop_info': {
                    'id': crop.id,
                    'name': crop.crop_name
                },
                'overall_stats': overall_stats,
                'monthly_performance': list(monthly_performance),
                'variant_performance': list(variant_performance),
                'top_performing_variants': top_variants,
                'growth_trend': growth_trend,
                'analysis_period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'months_analyzed': months_back
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Server error in crop performance metrics: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)