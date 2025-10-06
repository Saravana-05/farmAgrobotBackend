from calendar import monthrange
from datetime import datetime, timedelta, timezone
import io
import json
from turtle import pd
from venv import logger
from django.db.models import Q, Sum, Count, Avg
from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from ...models import Sale, SaleVariant, SaleImage, PaymentHistory, Merchant, Yield, CropVariant
from ...serializers import (
    SaleSerializer, SaleSummarySerializer, PaymentUpdateSerializer, 
    SaleImageSerializer, PaymentHistorySerializer
)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def save_sale_data(request):
    """
    Save sale data to the database with sale variants and images
    """
    try:
        # Check if request has any data
        if not request.data:
            return Response({
                'status': 'error',
                'message': 'No data received in request'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle multipart form data vs JSON data
        if request.content_type and 'multipart/form-data' in request.content_type:
            sale_data = {}
            for key, value in request.POST.items():
                sale_data[key] = value
        else:
            sale_data = request.data.copy()

        # Parse JSON strings
        for field in ['variants', 'image_metadata']:
            if field in sale_data:
                if isinstance(sale_data[field], str):
                    try:
                        sale_data[field] = json.loads(sale_data[field])
                        print(f"Successfully parsed {field}: {sale_data[field]}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse {field}: {e}")
                        sale_data[field] = []
                elif not isinstance(sale_data[field], list):
                    sale_data[field] = []

        # FIXED: Handle multiple file uploads properly
        uploaded_files = []
        if request.FILES:
            print(f"Processing {len(request.FILES)} file entries...")
            
            # Method 1: Try to get files with specific field name first
            if 'images' in request.FILES:
                # Single field with multiple files
                files = request.FILES.getlist('images')
                uploaded_files.extend(files)
                print(f"Found {len(files)} files in 'images' field")
            
            # Method 2: Check for files with image-related keywords
            for key, file in request.FILES.items():
                if key != 'images':  # Don't double-process
                    print(f"Processing file key: '{key}'")
                    
                    # Check for image-related keywords
                    if any(keyword in key.lower() for keyword in ['image', 'file', 'upload', 'bill', 'photo']):
                        uploaded_files.append(file)
                        print(f"Added file: {file.name} (key: {key})")
                    else:
                        print(f"Skipped file with key '{key}' - doesn't match keywords")
            
            # Method 3: If no files found yet, check for numbered fields (image_0, image_1, etc.)
            if not uploaded_files:
                file_keys = sorted([k for k in request.FILES.keys() if k.startswith(('image_', 'file_', 'upload_'))])
                for key in file_keys:
                    uploaded_files.append(request.FILES[key])
                    print(f"Added numbered file: {request.FILES[key].name} (key: {key})")
        
        print(f"Total files to process: {len(uploaded_files)}")

        # Add files to sale_data for serializer processing
        if uploaded_files:
            sale_data['images'] = uploaded_files
            print(f"Added {len(uploaded_files)} images to sale_data")

        # Debug logging
        print(f"Sale data keys: {list(sale_data.keys())}")
        print(f"Variants type: {type(sale_data.get('variants'))}")
        print(f"Variants value: {sale_data.get('variants')}")
        
        # Validate the sale data
        serializer = SaleSerializer(data=sale_data, context={'request': request})
        
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            sale_record = serializer.save()
            print(f"Sale {sale_record.id} created with {sale_record.sale_images.count()} images")
        
        # Return success response with created data
        response_serializer = SaleSerializer(sale_record, context={'request': request})
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
        import traceback
        traceback.print_exc()
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
        payment_status_filter = request.GET.get('payment_status')  # NEW
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
            'sale_variants__crop_variant__crop',
            'sale_images',
            'payment_history'
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
        
        if payment_status_filter:  # NEW
            sales = sales.filter(payment_status=payment_status_filter)
        
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
        
        serializer = SaleSerializer(sales, many=True, context={'request': request})
        
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
            'sale_variants__crop_variant__crop',
            'sale_images',
            'payment_history'
        ).get(id=sale_id)
        
        serializer = SaleSerializer(sale_record, context={'request': request})
        
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
@parser_classes([MultiPartParser, FormParser])
def update_sale_data(request, sale_id):
    """
    Update sale data with proper multiple image handling
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        
        # Handle multipart form data vs JSON data
        if request.content_type and 'multipart/form-data' in request.content_type:
            sale_data = {}
            for key, value in request.POST.items():
                sale_data[key] = value
        else:
            sale_data = request.data.copy()

        # Parse JSON strings
        for field in ['variants', 'image_metadata']:
            if field in sale_data:
                if isinstance(sale_data[field], str):
                    try:
                        sale_data[field] = json.loads(sale_data[field])
                        print(f"Successfully parsed {field}: {sale_data[field]}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse {field}: {e}")
                        sale_data[field] = []
                elif not isinstance(sale_data[field], list):
                    sale_data[field] = []

        # FIXED: Handle multiple file uploads for updates
        uploaded_files = []
        if request.FILES:
            print(f"Processing {len(request.FILES)} update file entries...")
            
            # Same logic as create view
            if 'images' in request.FILES:
                files = request.FILES.getlist('images')
                uploaded_files.extend(files)
                print(f"Found {len(files)} update files in 'images' field")
            
            for key, file in request.FILES.items():
                if key != 'images':
                    print(f"Processing update file key: '{key}'")
                    
                    if any(keyword in key.lower() for keyword in ['image', 'file', 'upload', 'bill', 'photo']):
                        uploaded_files.append(file)
                        print(f"Added update file: {file.name} (key: {key})")
                    else:
                        print(f"Skipped update file with key '{key}' - doesn't match keywords")
            
            if not uploaded_files:
                file_keys = sorted([k for k in request.FILES.keys() if k.startswith(('image_', 'file_', 'upload_'))])
                for key in file_keys:
                    uploaded_files.append(request.FILES[key])
                    print(f"Added numbered update file: {request.FILES[key].name} (key: {key})")
        
        print(f"Total update files to process: {len(uploaded_files)}")

        # Add files to sale_data for serializer processing
        if uploaded_files:
            sale_data['images'] = uploaded_files
            print(f"Added {len(uploaded_files)} update images to sale_data")
        
        # Validate the updated data
        serializer = SaleSerializer(
            sale_record, 
            data=sale_data, 
            partial=True, 
            context={'request': request}
        )
        
        if not serializer.is_valid():
            print(f"Update validation errors: {serializer.errors}")
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            sale_record = serializer.save()
            print(f"Sale {sale_record.id} updated, now has {sale_record.sale_images.count()} images")
        
        # Return updated data
        response_serializer = SaleSerializer(sale_record, context={'request': request})
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
        import traceback
        traceback.print_exc()
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

# NEW: Payment Management Views

@api_view(['POST'])
def add_payment(request, sale_id):
    """
    Add a payment to a sale record
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        
        # Set the instance for validation
        serializer = PaymentUpdateSerializer(data=request.data)
        serializer.instance = sale_record  # For validation purposes
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        payment_amount = serializer.validated_data['payment_amount']
        payment_method = serializer.validated_data['payment_method']
        payment_reference = serializer.validated_data.get('payment_reference', '')
        notes = serializer.validated_data.get('notes', '')
        created_by = serializer.validated_data.get('created_by', '')
        
        with transaction.atomic():
            # Create payment history record
            PaymentHistory.objects.create(
                sale=sale_record,
                payment_amount=payment_amount,
                payment_method=payment_method,
                payment_reference=payment_reference,
                notes=notes,
                created_by=created_by
            )
            
            # Update sale payment information
            sale_record.paid_amount += payment_amount
            sale_record.save()  # This will auto-update payment_status and pending_amount
        
        # Return updated sale data
        response_serializer = SaleSerializer(sale_record, context={'request': request})
        return Response({
            'status': 'success',
            'message': 'Payment added successfully',
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

@api_view(['GET'])
def get_payment_history(request, sale_id):
    """
    Get payment history for a specific sale
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        payment_history = PaymentHistory.objects.filter(sale=sale_record).order_by('-payment_date')
        
        serializer = PaymentHistorySerializer(payment_history, many=True)
        
        return Response({
            'status': 'success',
            'message': 'Payment history retrieved successfully',
            'data': {
                'sale_id': sale_id,
                'final_amount': sale_record.final_amount,
                'paid_amount': sale_record.paid_amount,
                'pending_amount': sale_record.pending_amount,
                'payment_status': sale_record.payment_status,
                'payment_history': serializer.data
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

# NEW: Image Management Views
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_sale_images(request, sale_id):
    """
    Add images to an existing sale
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        
        images = request.FILES.getlist('images')
        if not images:
            return Response({
                'status': 'error',
                'message': 'No images provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get metadata if provided
        image_names = request.data.getlist('image_names', [])
        image_descriptions = request.data.getlist('image_descriptions', [])
        is_primary_flags = request.data.getlist('is_primary', [])
        
        created_images = []
        
        with transaction.atomic():
            for i, image in enumerate(images):
                name = image_names[i] if i < len(image_names) else ''
                description = image_descriptions[i] if i < len(image_descriptions) else ''
                is_primary = str(is_primary_flags[i]).lower() == 'true' if i < len(is_primary_flags) else False
                
                sale_image = SaleImage.objects.create(
                    sale=sale_record,
                    image=image,
                    image_name=name,
                    description=description,
                    is_primary=is_primary
                )
                created_images.append(sale_image)
        
        serializer = SaleImageSerializer(created_images, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'message': f'{len(created_images)} images added successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
        
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
@parser_classes([MultiPartParser, FormParser])
def update_sale_image(request, sale_id, image_id):
    """
    Update a specific sale image
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        sale_image = SaleImage.objects.get(id=image_id, sale=sale_record)
        
        serializer = SaleImageSerializer(
            sale_image, 
            data=request.data, 
            partial=True, 
            context={'request': request}
        )
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        updated_image = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Image updated successfully',
            'data': SaleImageSerializer(updated_image, context={'request': request}).data
        }, status=status.HTTP_200_OK)
        
    except Sale.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Sale record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except SaleImage.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Image not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_sale_image(request, sale_id, image_id):
    """
    Delete a specific sale image
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        sale_image = SaleImage.objects.get(id=image_id, sale=sale_record)
        
        # Delete the image file and record
        sale_image.delete()
        
        return Response({
            'status': 'success',
            'message': 'Image deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Sale.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Sale record not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except SaleImage.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Image not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_sale_images(request, sale_id):
    """
    Get all images for a specific sale
    """
    try:
        sale_record = Sale.objects.get(id=sale_id)
        images = SaleImage.objects.filter(sale=sale_record).order_by('-is_primary', '-uploaded_at')
        
        serializer = SaleImageSerializer(images, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'message': 'Images retrieved successfully',
            'data': serializer.data,
            'count': images.count()
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
            'sale_variants__crop_variant',
            'sale_images',
            'payment_history'
        ).order_by('-created_at')
        
        serializer = SaleSerializer(sales, many=True, context={'request': request})
        
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
def get_available_yields(request):
    """
    Get yields that are not yet sold (for dropdown population)
    """
    try:
        # Get yields that don't have any non-cancelled sales
        sold_yield_ids = Sale.objects.exclude(status='cancelled').values_list('yield_record_id', flat=True)
        available_yields = Yield.objects.exclude(id__in=sold_yield_ids).select_related('crop').prefetch_related(
            'yield_variants__crop_variant',
            'yield_farm_segments__farm_segment'
        ).order_by('-harvest_date')
        
        # Simple serialization for dropdown
        yields_data = []
        for yield_record in available_yields:
            # Calculate total quantity from yield variants
            total_quantity = sum(variant.quantity for variant in yield_record.yield_variants.all())
            
            # Get farm segment names if any
            farm_segments = [seg.farm_segment.farm_name for seg in yield_record.yield_farm_segments.all()]
            farm_location = ", ".join(farm_segments) if farm_segments else "No location specified"
            
            # Get yield variants info for display
            variants_info = []
            for variant in yield_record.yield_variants.all():
                variants_info.append(f"{variant.crop_variant.crop_variant}: {variant.quantity} {variant.unit}")
            variants_display = "; ".join(variants_info) if variants_info else "No variants"
            
            # Build display text
            display_text = f"{yield_record.crop.crop_name} - {yield_record.harvest_date.strftime('%Y-%m-%d')}"
            if total_quantity > 0:
                display_text += f" ({total_quantity} total)"
            if farm_segments:
                display_text += f" - {farm_segments[0]}"  # Show first farm segment only in dropdown
            
            yield_data = {
                'id': yield_record.id,
                'crop_name': yield_record.crop.crop_name,
                'harvest_date': yield_record.harvest_date,
                'total_quantity': float(total_quantity),
                'farm_location': farm_location,
                'variants_info': variants_display,
                'bill_count': yield_record.bill_count,
                'has_bills': yield_record.has_bills,
                'created_at': yield_record.created_at,
                'display_text': display_text
            }
            
            yields_data.append(yield_data)
        
        return Response({
            'status': 'success',
            'message': 'Available yields retrieved successfully',
            'data': yields_data,
            'count': len(yields_data)
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
    Get sale summary statistics with payment tracking
    """
    try:
        from django.db.models import Sum, Count, Avg, Max, Min, Q
        from django.db.models.functions import TruncMonth, TruncDate
        
        # Get query parameters
        merchant_id = request.GET.get('merchant_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        status_filter = request.GET.get('status')
        payment_status_filter = request.GET.get('payment_status')
        
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
        if payment_status_filter:
            sales = sales.filter(payment_status=payment_status_filter)
        
        # Get summary statistics
        summary_stats = sales.aggregate(
            total_sales=Count('id'),
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount'),
            avg_sale_amount=Avg('final_amount'),
            max_sale_amount=Max('final_amount'),
            min_sale_amount=Min('final_amount'),
            total_commission=Sum('commission'),
            total_lorry_rent=Sum('lorry_rent'),
            total_cooly_charges=Sum('cooly_charges'),
            total_deductions=Sum('total_deductions')
        )
        
        # Add collection rate calculation
        if summary_stats['total_revenue'] and summary_stats['total_revenue'] > 0:
            summary_stats['collection_rate'] = (
                summary_stats['total_paid'] / summary_stats['total_revenue'] * 100
            )
        else:
            summary_stats['collection_rate'] = 0
        
        # Payment status breakdown
        payment_status_summary = sales.values('payment_status').annotate(
            count=Count('id'),
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount')
        ).order_by('-count')
        
        # Monthly summary with payment tracking
        monthly_summary = sales.annotate(
            month=TruncMonth('harvest_date')
        ).values('month').annotate(
            sales_count=Count('id'),
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount'),
            avg_revenue=Avg('final_amount'),
            collection_rate=Sum('paid_amount') * 100.0 / Sum('final_amount')
        ).order_by('month')
        
        # Merchant-wise summary with payment details
        merchant_summary = sales.values(
            'merchant__name',
            'merchant__id'
        ).annotate(
            sales_count=Count('id'),
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount'),
            avg_revenue=Avg('final_amount'),
            collection_rate=Sum('paid_amount') * 100.0 / Sum('final_amount')
        ).order_by('-total_revenue')
        
        # Payment method distribution
        payment_mode_summary = sales.values('payment_mode').annotate(
            count=Count('id'),
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            percentage=Count('id') * 100.0 / sales.count() if sales.count() > 0 else 0
        ).order_by('-count')
        
        return Response({
            'status': 'success',
            'message': 'Sale summary retrieved successfully',
            'data': {
                'summary_stats': summary_stats,
                'payment_status_summary': list(payment_status_summary),
                'monthly_summary': list(monthly_summary),
                'merchant_summary': list(merchant_summary),
                'payment_mode_summary': list(payment_mode_summary)
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
    Get advanced analytics for sales data with payment insights
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
        
        # Revenue and collection trends
        revenue_trend = sales.extra(
            select={'day': 'DATE(harvest_date)'}
        ).values('day').annotate(
            revenue=Sum('final_amount'),
            paid=Sum('paid_amount'),
            pending=Sum('pending_amount'),
            sales_count=Count('id'),
            collection_rate=Sum('paid_amount') * 100.0 / Sum('final_amount')
        ).order_by('day')
        
        # Top performing merchants with payment insights
        top_merchants = sales.values(
            'merchant__name',
            'merchant__id'
        ).annotate(
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount'),
            sales_count=Count('id'),
            avg_sale_value=Avg('final_amount'),
            collection_rate=Sum('paid_amount') * 100.0 / Sum('final_amount')
        ).order_by('-total_revenue')[:10]
        
        # Payment behavior analysis
        payment_analysis = sales.aggregate(
            prompt_payments=Count('id', filter=Q(payment_status='paid')),
            partial_payments=Count('id', filter=Q(payment_status='partial')),
            pending_payments=Count('id', filter=Q(payment_status='pending')),
            total_collectible=Sum('final_amount'),
            total_collected=Sum('paid_amount'),
            total_outstanding=Sum('pending_amount')
        )
        
        # Add percentage calculations
        total_sales = payment_analysis['prompt_payments'] + payment_analysis['partial_payments'] + payment_analysis['pending_payments']
        if total_sales > 0:
            payment_analysis['prompt_payment_rate'] = payment_analysis['prompt_payments'] / total_sales * 100
            payment_analysis['partial_payment_rate'] = payment_analysis['partial_payments'] / total_sales * 100
            payment_analysis['pending_payment_rate'] = payment_analysis['pending_payments'] / total_sales * 100
        
        # Outstanding amounts by merchant
        outstanding_by_merchant = sales.filter(
            payment_status__in=['pending', 'partial']
        ).values(
            'merchant__name',
            'merchant__id'
        ).annotate(
            outstanding_amount=Sum('pending_amount'),
            outstanding_count=Count('id')
        ).order_by('-outstanding_amount')[:10]
        
        return Response({
            'status': 'success',
            'message': 'Sales analytics retrieved successfully',
            'data': {
                'period': f'Last {days} days',
                'revenue_trend': list(revenue_trend),
                'top_merchants': list(top_merchants),
                'payment_analysis': payment_analysis,
                'outstanding_by_merchant': list(outstanding_by_merchant)
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def advanced_sales_search(request):
    """
    Advanced search with multiple criteria including date ranges, merchant, yield, etc.
    """
    try:
        # Get all filter parameters
        merchant_id = request.GET.get('merchant_id')
        merchant_name = request.GET.get('merchant_name')
        yield_id = request.GET.get('yield_id')
        crop_name = request.GET.get('crop_name')
        payment_mode = request.GET.get('payment_mode')
        status_filter = request.GET.get('status')
        payment_status_filter = request.GET.get('payment_status')
        
        # Date filters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        date_range = request.GET.get('date_range')  # predefined ranges like 'today', 'week', 'month'
        
        # Amount filters
        min_amount = request.GET.get('min_amount')
        max_amount = request.GET.get('max_amount')
        
        # Sorting
        sort_by = request.GET.get('sort_by', '-created_at')
        
        # Pagination
        page_size = int(request.GET.get('page_size', 50))
        page = int(request.GET.get('page', 1))
        
        # Start with base queryset
        sales = Sale.objects.select_related(
            'merchant', 
            'yield_record',
            'yield_record__crop'
        ).prefetch_related(
            'sale_variants__crop_variant',
            'sale_variants__crop_variant__crop',
            'sale_images',
            'payment_history'
        )
        
        # Apply filters
        if merchant_id:
            sales = sales.filter(merchant_id=merchant_id)
        
        if merchant_name:
            sales = sales.filter(merchant__name__icontains=merchant_name)
        
        if yield_id:
            sales = sales.filter(yield_record_id=yield_id)
        
        if crop_name:
            sales = sales.filter(yield_record__crop__crop_name__icontains=crop_name)
        
        if payment_mode:
            sales = sales.filter(payment_mode=payment_mode)
        
        if status_filter:
            sales = sales.filter(status=status_filter)
        
        if payment_status_filter:
            sales = sales.filter(payment_status=payment_status_filter)
        
        # Date range filtering
        if date_range:
            today = timezone.now().date()
            if date_range == 'today':
                sales = sales.filter(harvest_date__date=today)
            elif date_range == 'yesterday':
                yesterday = today - timedelta(days=1)
                sales = sales.filter(harvest_date__date=yesterday)
            elif date_range == 'week':
                week_ago = today - timedelta(days=7)
                sales = sales.filter(harvest_date__date__gte=week_ago)
            elif date_range == 'month':
                month_ago = today - timedelta(days=30)
                sales = sales.filter(harvest_date__date__gte=month_ago)
            elif date_range == 'quarter':
                quarter_ago = today - timedelta(days=90)
                sales = sales.filter(harvest_date__date__gte=quarter_ago)
        
        if start_date:
            sales = sales.filter(harvest_date__date__gte=start_date)
        
        if end_date:
            sales = sales.filter(harvest_date__date__lte=end_date)
        
        if min_amount:
            sales = sales.filter(final_amount__gte=min_amount)
        
        if max_amount:
            sales = sales.filter(final_amount__lte=max_amount)
        
        # Get total count before pagination
        total_count = sales.count()
        
        # Apply sorting
        sales = sales.order_by(sort_by)
        
        # Apply pagination
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        sales = sales[start_index:end_index]
        
        # Serialize data
        serializer = SaleSerializer(sales, many=True, context={'request': request})
        
        # Calculate summary statistics for filtered results
        summary_stats = Sale.objects.filter(
            id__in=[sale.id for sale in Sale.objects.filter(
                **{k: v for k, v in {
                    'merchant_id': merchant_id,
                    'yield_record_id': yield_id,
                    'payment_mode': payment_mode,
                    'status': status_filter,
                    'payment_status': payment_status_filter
                }.items() if v}
            )]
        ).aggregate(
            total_sales=Count('id'),
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount'),
            avg_sale_amount=Avg('final_amount')
        )
        
        return Response({
            'status': 'success',
            'message': 'Search results retrieved successfully',
            'data': {
                'sales': serializer.data,
                'pagination': {
                    'current_page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size,
                    'has_next': end_index < total_count,
                    'has_previous': page > 1
                },
                'summary': summary_stats,
                'filters_applied': {
                    'merchant_id': merchant_id,
                    'merchant_name': merchant_name,
                    'yield_id': yield_id,
                    'crop_name': crop_name,
                    'payment_mode': payment_mode,
                    'status': status_filter,
                    'payment_status': payment_status_filter,
                    'start_date': start_date,
                    'end_date': end_date,
                    'date_range': date_range,
                    'min_amount': min_amount,
                    'max_amount': max_amount
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error in advanced search: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def search_suggestions(request):
    """
    Provide search suggestions for autocomplete functionality
    """
    try:
        search_type = request.GET.get('type')  # 'merchant', 'crop', 'yield'
        query = request.GET.get('query', '')
        
        suggestions = []
        
        if search_type == 'merchant' and query:
            merchants = Merchant.objects.filter(
                name__icontains=query
            )[:10]
            suggestions = [{'id': m.id, 'name': m.name} for m in merchants]
            
        elif search_type == 'crop' and query:
            from ...models import Crop
            crops = Crop.objects.filter(
                crop_name__icontains=query
            )[:10]
            suggestions = [{'id': c.id, 'name': c.crop_name} for c in crops]
            
        elif search_type == 'yield' and query:
            yields = Yield.objects.select_related('crop').filter(
                Q(crop__crop_name__icontains=query) |
                Q(location__icontains=query)
            )[:10]
            suggestions = [{
                'id': y.id,
                'name': f"{y.crop.crop_name} - {y.harvest_date.strftime('%Y-%m-%d')} - {y.location or 'N/A'}"
            } for y in yields]
        
        return Response({
            'status': 'success',
            'data': suggestions
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# EXCEL REPORT GENERATION

@api_view(['GET'])
def generate_excel_report(request):
    """
    Generate Excel report based on search filters
    """
    try:
        # Get the same filters as advanced search
        filters = _get_search_filters(request)
        sales_queryset = _apply_search_filters(filters)
        
        # Create Excel file
        output = io.BytesIO()
        
        # Create pandas DataFrame
        sales_data = []
        for sale in sales_queryset:
            # Basic sale data
            row = {
                'Sale ID': sale.id,
                'Merchant Name': sale.merchant.name,
                'Crop Name': sale.yield_record.crop.crop_name,
                'Harvest Date': sale.harvest_date.strftime('%Y-%m-%d %H:%M:%S'),
                'Payment Mode': sale.payment_mode,
                'Status': sale.status,
                'Payment Status': sale.payment_status,
                'Total Amount': float(sale.total_amount),
                'Commission': float(sale.commission),
                'Lorry Rent': float(sale.lorry_rent),
                'Cooly Charges': float(sale.cooly_charges),
                'Total Deductions': float(sale.total_deductions),
                'Final Amount': float(sale.final_amount),
                'Paid Amount': float(sale.paid_amount),
                'Pending Amount': float(sale.pending_amount),
                'Created At': sale.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            # Add sale variants data
            variants_data = []
            for variant in sale.sale_variants.all():
                variants_data.append(f"{variant.crop_variant.crop_variant}: {variant.quantity} {variant.unit} @ ₹{variant.amount_per_unit}")
            row['Sale Variants'] = '; '.join(variants_data)
            
            sales_data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(sales_data)
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Main sales data
            df.to_excel(writer, sheet_name='Sales Data', index=False)
            
            # Summary sheet
            summary_data = sales_queryset.aggregate(
                total_sales=Count('id'),
                total_revenue=Sum('final_amount'),
                total_paid=Sum('paid_amount'),
                total_pending=Sum('pending_amount'),
                avg_sale_amount=Avg('final_amount'),
                total_commission=Sum('commission'),
                total_deductions=Sum('total_deductions')
            )
            
            summary_df = pd.DataFrame([summary_data])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Merchant wise summary
            merchant_summary = sales_queryset.values(
                'merchant__name'
            ).annotate(
                total_sales=Count('id'),
                total_revenue=Sum('final_amount'),
                total_paid=Sum('paid_amount'),
                total_pending=Sum('pending_amount'),
                avg_revenue=Avg('final_amount')
            ).order_by('-total_revenue')
            
            merchant_df = pd.DataFrame(list(merchant_summary))
            merchant_df.to_excel(writer, sheet_name='Merchant Summary', index=False)
        
        output.seek(0)
        
        # Create response
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # Generate filename with current date
        filename = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        print(f"Excel generation error: {e}")
        return Response({
            'status': 'error',
            'message': f'Error generating Excel report: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PDF BILL GENERATION

@api_view(['GET'])
def generate_pdf_bill(request, sale_id):
    """
    Generate PDF bill for a specific sale
    """
    try:
        sale = Sale.objects.select_related(
            'merchant',
            'yield_record__crop'
        ).prefetch_related(
            'sale_variants__crop_variant',
            'payment_history'
        ).get(id=sale_id)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        filename = f"sale_bill_{sale.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkgreen
        )
        
        # Title
        title = Paragraph("SALE INVOICE", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Sale Information
        sale_info = [
            ['Sale ID:', str(sale.id)],
            ['Date:', sale.harvest_date.strftime('%Y-%m-%d %H:%M:%S')],
            ['Status:', sale.status.upper()],
            ['Payment Status:', sale.payment_status.upper()],
        ]
        
        sale_table = Table(sale_info, colWidths=[2*inch, 3*inch])
        sale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ]))
        
        elements.append(Paragraph("Sale Information", header_style))
        elements.append(sale_table)
        elements.append(Spacer(1, 20))
        
        # Merchant Information
        merchant_info = [
            ['Merchant Name:', sale.merchant.name],
            ['Payment Mode:', sale.payment_mode],
        ]
        
        merchant_table = Table(merchant_info, colWidths=[2*inch, 3*inch])
        merchant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ]))
        
        elements.append(Paragraph("Merchant Information", header_style))
        elements.append(merchant_table)
        elements.append(Spacer(1, 20))
        
        # Sale Variants
        elements.append(Paragraph("Items Sold", header_style))
        
        variant_data = [['Crop Variant', 'Quantity', 'Unit', 'Rate (₹)', 'Amount (₹)']]
        
        for variant in sale.sale_variants.all():
            variant_data.append([
                variant.crop_variant.crop_variant,
                str(variant.quantity),
                variant.unit,
                f"₹{variant.amount_per_unit:,.2f}",
                f"₹{variant.total_amount:,.2f}"
            ])
        
        variant_table = Table(variant_data, colWidths=[2*inch, 1*inch, 0.8*inch, 1.2*inch, 1.2*inch])
        variant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(variant_table)
        elements.append(Spacer(1, 20))
        
        # Financial Summary
        financial_data = [
            ['Total Amount', f"₹{sale.total_amount:,.2f}"],
            ['Commission', f"₹{sale.commission:,.2f}"],
            ['Lorry Rent', f"₹{sale.lorry_rent:,.2f}"],
            ['Cooly Charges', f"₹{sale.cooly_charges:,.2f}"],
            ['Total Deductions', f"₹{sale.total_deductions:,.2f}"],
            ['Final Amount', f"₹{sale.final_amount:,.2f}"],
            ['Paid Amount', f"₹{sale.paid_amount:,.2f}"],
            ['Pending Amount', f"₹{sale.pending_amount:,.2f}"],
        ]
        
        financial_table = Table(financial_data, colWidths=[3*inch, 2*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (0, -3), (-1, -1), colors.lightcoral),  # Highlight final amounts
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(Paragraph("Financial Summary", header_style))
        elements.append(financial_table)
        
        # Payment History if available
        if sale.payment_history.exists():
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("Payment History", header_style))
            
            payment_data = [['Date', 'Amount', 'Method', 'Reference']]
            for payment in sale.payment_history.all():
                payment_data.append([
                    payment.payment_date.strftime('%Y-%m-%d'),
                    f"₹{payment.payment_amount:,.2f}",
                    payment.payment_method,
                    payment.payment_reference or 'N/A'
                ])
            
            payment_table = Table(payment_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            payment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(payment_table)
        
        # Footer
        elements.append(Spacer(1, 30))
        footer_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        footer = Paragraph(footer_text, styles['Normal'])
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        return response
        
    except Sale.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Sale not found'
        }, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(f"PDF generation error: {e}")
        return Response({
            'status': 'error',
            'message': f'Error generating PDF: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def generate_bulk_pdf_report(request):
    """
    Generate bulk PDF report for multiple sales
    """
    try:
        # Get search filters
        filters = _get_search_filters(request)
        sales_queryset = _apply_search_filters(filters)
        
        response = HttpResponse(content_type='application/pdf')
        filename = f"bulk_sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1,
            textColor=colors.darkblue
        )
        
        title = Paragraph("BULK SALES REPORT", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Summary
        summary = sales_queryset.aggregate(
            total_sales=Count('id'),
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount')
        )
        
        summary_data = [
            ['Total Sales', str(summary['total_sales'] or 0)],
            ['Total Revenue', f"₹{summary['total_revenue'] or 0:,.2f}"],
            ['Total Paid', f"₹{summary['total_paid'] or 0:,.2f}"],
            ['Total Pending', f"₹{summary['total_pending'] or 0:,.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(Paragraph("Summary", styles['Heading2']))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Sales table
        sales_data = [['ID', 'Merchant', 'Date', 'Final Amount', 'Paid', 'Status']]
        
        for sale in sales_queryset[:50]:  # Limit to 50 for PDF readability
            sales_data.append([
                str(sale.id),
                sale.merchant.name[:20],  # Truncate long names
                sale.harvest_date.strftime('%Y-%m-%d'),
                f"₹{sale.final_amount:,.0f}",
                f"₹{sale.paid_amount:,.0f}",
                sale.payment_status
            ])
        
        sales_table = Table(sales_data, colWidths=[0.8*inch, 1.8*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1*inch])
        sales_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        
        elements.append(Paragraph("Sales Details", styles['Heading2']))
        elements.append(sales_table)
        
        if sales_queryset.count() > 50:
            elements.append(Spacer(1, 10))
            note = Paragraph(f"Note: Showing first 50 sales out of {sales_queryset.count()} total sales.", styles['Normal'])
            elements.append(note)
        
        doc.build(elements)
        return response
        
    except Exception as e:
        print(f"Bulk PDF generation error: {e}")
        return Response({
            'status': 'error',
            'message': f'Error generating bulk PDF: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# UTILITY FUNCTIONS

def _get_search_filters(request):
    """Extract search filters from request parameters"""
    return {
        'merchant_id': request.GET.get('merchant_id'),
        'merchant_name': request.GET.get('merchant_name'),
        'yield_id': request.GET.get('yield_id'),
        'crop_name': request.GET.get('crop_name'),
        'payment_mode': request.GET.get('payment_mode'),
        'status': request.GET.get('status'),
        'payment_status': request.GET.get('payment_status'),
        'start_date': request.GET.get('start_date'),
        'end_date': request.GET.get('end_date'),
        'date_range': request.GET.get('date_range'),
        'min_amount': request.GET.get('min_amount'),
        'max_amount': request.GET.get('max_amount'),
    }

def _apply_search_filters(filters):
    """Apply filters to Sale queryset"""
    sales = Sale.objects.select_related(
        'merchant',
        'yield_record__crop'
    ).prefetch_related(
        'sale_variants__crop_variant',
        'payment_history'
    )
    
    # Apply all the same filters as in advanced_sales_search
    if filters['merchant_id']:
        sales = sales.filter(merchant_id=filters['merchant_id'])
    
    if filters['merchant_name']:
        sales = sales.filter(merchant__name__icontains=filters['merchant_name'])
    
    if filters['yield_id']:
        sales = sales.filter(yield_record_id=filters['yield_id'])
    
    if filters['crop_name']:
        sales = sales.filter(yield_record__crop__crop_name__icontains=filters['crop_name'])
    
    if filters['payment_mode']:
        sales = sales.filter(payment_mode=filters['payment_mode'])
    
    if filters['status']:
        sales = sales.filter(status=filters['status'])
    
    if filters['payment_status']:
        sales = sales.filter(payment_status=filters['payment_status'])
    
    # Date filtering logic
    if filters['date_range']:
        today = timezone.now().date()
        if filters['date_range'] == 'today':
            sales = sales.filter(harvest_date__date=today)
        elif filters['date_range'] == 'yesterday':
            yesterday = today - timedelta(days=1)
            sales = sales.filter(harvest_date__date=yesterday)
        elif filters['date_range'] == 'week':
            week_ago = today - timedelta(days=7)
            sales = sales.filter(harvest_date__date__gte=week_ago)
        elif filters['date_range'] == 'month':
            month_ago = today - timedelta(days=30)
            sales = sales.filter(harvest_date__date__gte=month_ago)
        elif filters['date_range'] == 'quarter':
            quarter_ago = today - timedelta(days=90)
            sales = sales.filter(harvest_date__date__gte=quarter_ago)
    
    if filters['start_date']:
        sales = sales.filter(harvest_date__date__gte=filters['start_date'])
    
    if filters['end_date']:
        sales = sales.filter(harvest_date__date__lte=filters['end_date'])
    
    if filters['min_amount']:
        sales = sales.filter(final_amount__gte=filters['min_amount'])
    
    if filters['max_amount']:
        sales = sales.filter(final_amount__lte=filters['max_amount'])
    
    return sales.order_by('-created_at')


@api_view(['GET'])
def get_payment_modes(request):
    """
    Get available payment modes from Sale model choices
    """
    try:
        # Get payment modes from the model choices
        payment_modes = [choice[0] for choice in Sale.PAYMENT_MODE_CHOICES]
        
        return Response({
            'status': 'success',
            'message': 'Payment modes retrieved successfully',
            'data': payment_modes
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Server error: {e}")
        return Response({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_yield_variants(request, yield_id):
    """
    Get yield variants for a specific yield record
    """
    try:
        # Get the yield record with related data
        yield_record = Yield.objects.select_related('crop').prefetch_related(
            'yield_variants__crop_variant',
            'yield_variants__crop_variant__crop',
            'yield_farm_segments__farm_segment'
        ).get(id=yield_id)
        
        # Prepare yield variants data
        variants_data = []
        for variant in yield_record.yield_variants.all():
            variant_data = {
                'id': variant.id,
                'crop_variant_id': variant.crop_variant.id,
                'crop_variant_name': variant.crop_variant.crop_variant,
                'quantity': float(variant.quantity),
                'unit': variant.unit,
                'crop_name': variant.crop_variant.crop.crop_name,
                'notes': getattr(variant, 'notes', '') or '',
            }
            variants_data.append(variant_data)
        
        # Get farm segments info
        farm_segments = []
        for farm_segment in yield_record.yield_farm_segments.all():
            farm_segments.append({
                'id': farm_segment.farm_segment.id,
                'farm_name': farm_segment.farm_segment.farm_name,
                'location': getattr(farm_segment.farm_segment, 'location', ''),
            })
        
        # Calculate total quantity
        total_quantity = sum(variant.quantity for variant in yield_record.yield_variants.all())
        
        # Prepare response data
        response_data = {
            'id': yield_record.id,
            'crop_id': yield_record.crop.id,
            'crop_name': yield_record.crop.crop_name,
            'harvest_date': yield_record.harvest_date,
            'total_quantity': float(total_quantity),
            'bill_count': yield_record.bill_count,
            'has_bills': yield_record.has_bills,
            'location': getattr(yield_record, 'location', ''),
            'notes': getattr(yield_record, 'notes', ''),
            'created_at': yield_record.created_at,
            'updated_at': yield_record.updated_at,
            'yield_variants': variants_data,
            'farm_segments': farm_segments,
        }
        
        return Response({
            'status': 'success',
            'message': 'Yield variants retrieved successfully',
            'data': response_data
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
def get_dashboard_revenue(request):
    """
    Get comprehensive revenue data with time period breakdowns for dashboard display
    """
    try:
        from django.db.models import Sum, Count, Avg
        from datetime import datetime, timedelta
        from calendar import monthrange
        from django.utils import timezone
        
        # Get current date info
        today = timezone.now().date()
        current_year = today.year
        current_month = today.month
        
        # Calculate date ranges
        current_year_start = today.replace(month=1, day=1)
        current_year_end = today.replace(month=12, day=31)
        
        last_year = current_year - 1
        last_year_start = today.replace(year=last_year, month=1, day=1)
        last_year_end = today.replace(year=last_year, month=12, day=31)
        
        current_month_start = today.replace(day=1)
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
        
        # Get query parameters for additional filtering
        merchant_id = request.GET.get('merchant_id')
        status_filter = request.GET.get('status')
        
        # Base queryset - exclude cancelled sales
        base_sales = Sale.objects.exclude(status='cancelled')
        
        # Apply merchant filter if provided
        if merchant_id:
            base_sales = base_sales.filter(merchant_id=merchant_id)
            
        if status_filter:
            base_sales = base_sales.filter(status=status_filter)
        
        # Function to calculate metrics for a given queryset
        def calculate_metrics(sales_queryset):
            metrics = sales_queryset.aggregate(
                total_revenue=Sum('final_amount'),
                total_paid=Sum('paid_amount'),
                total_pending=Sum('pending_amount'),
                total_sales_count=Count('id'),
                average_sale_amount=Avg('final_amount'),
                total_commission=Sum('commission'),
                total_deductions=Sum('total_deductions')
            )
            
            # Handle None values
            for key, value in metrics.items():
                if value is None:
                    metrics[key] = 0
            
            # Calculate collection rate
            if metrics['total_revenue'] > 0:
                metrics['collection_rate'] = round(
                    (metrics['total_paid'] / metrics['total_revenue']) * 100, 2
                )
            else:
                metrics['collection_rate'] = 0
            
            return {
                'total_revenue': float(metrics['total_revenue']),
                'total_paid': float(metrics['total_paid']),
                'total_pending': float(metrics['total_pending']),
                'total_sales_count': metrics['total_sales_count'],
                'average_sale_amount': round(float(metrics['average_sale_amount']), 2),
                'collection_rate': metrics['collection_rate'],
                'total_commission': float(metrics['total_commission']),
                'total_deductions': float(metrics['total_deductions'])
            }
        
        # Calculate metrics for different time periods
        time_periods = {}
        
        # Current Year
        current_year_sales = base_sales.filter(harvest_date__date__range=[current_year_start, current_year_end])
        time_periods['current_year'] = {
            **calculate_metrics(current_year_sales),
            'period_name': f'Current Year ({current_year})',
            'start_date': current_year_start.isoformat(),
            'end_date': current_year_end.isoformat()
        }
        
        # Last Year
        last_year_sales = base_sales.filter(harvest_date__date__range=[last_year_start, last_year_end])
        time_periods['last_year'] = {
            **calculate_metrics(last_year_sales),
            'period_name': f'Last Year ({last_year})',
            'start_date': last_year_start.isoformat(),
            'end_date': last_year_end.isoformat()
        }
        
        # Current Month
        current_month_sales = base_sales.filter(harvest_date__date__range=[current_month_start, current_month_end])
        time_periods['current_month'] = {
            **calculate_metrics(current_month_sales),
            'period_name': f'Current Month ({today.strftime("%B %Y")})',
            'start_date': current_month_start.isoformat(),
            'end_date': current_month_end.isoformat()
        }
        
        # Last Month
        last_month_sales = base_sales.filter(harvest_date__date__range=[last_month_start, last_month_end])
        last_month_name = last_month_start.strftime("%B %Y")
        time_periods['last_month'] = {
            **calculate_metrics(last_month_sales),
            'period_name': f'Last Month ({last_month_name})',
            'start_date': last_month_start.isoformat(),
            'end_date': last_month_end.isoformat()
        }
        
        # All Time (for comparison)
        time_periods['all_time'] = {
            **calculate_metrics(base_sales),
            'period_name': 'All Time',
            'start_date': None,
            'end_date': None
        }
        
        # Calculate percentage changes
        def calculate_percentage_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 2)
        
        # Year-over-year comparison
        yearly_revenue_change = calculate_percentage_change(
            time_periods['current_year']['total_revenue'],
            time_periods['last_year']['total_revenue']
        )
        
        # Month-over-month comparison
        monthly_revenue_change = calculate_percentage_change(
            time_periods['current_month']['total_revenue'],
            time_periods['last_month']['total_revenue']
        )
        
        # Payment status breakdown for current year
        current_year_payment_breakdown = current_year_sales.values('payment_mode').annotate(
            count=Count('id'),
            total_amount=Sum('final_amount')
        ).order_by('-total_amount')
        
        # Convert to list for JSON serialization
        payment_breakdown = []
        for item in current_year_payment_breakdown:
            payment_breakdown.append({
                'payment_mode': item['payment_mode'],
                'count': item['count'],
                'total_amount': float(item['total_amount'] or 0)
            })
        
        # Recent activity (last 7 days)
        recent_sales = base_sales.filter(
            harvest_date__gte=timezone.now() - timedelta(days=7)
        )
        
        recent_data = recent_sales.aggregate(
            recent_count=Count('id'),
            recent_revenue=Sum('final_amount')
        )
        
        # Build response
        response_data = {
            'time_periods': time_periods,
            'comparisons': {
                'yearly_comparison': {
                    'percentage_change': yearly_revenue_change,
                    'trend': 'up' if yearly_revenue_change > 0 else 'down' if yearly_revenue_change < 0 else 'stable',
                    'current_year_revenue': time_periods['current_year']['total_revenue'],
                    'last_year_revenue': time_periods['last_year']['total_revenue']
                },
                'monthly_comparison': {
                    'percentage_change': monthly_revenue_change,
                    'trend': 'up' if monthly_revenue_change > 0 else 'down' if monthly_revenue_change < 0 else 'stable',
                    'current_month_revenue': time_periods['current_month']['total_revenue'],
                    'last_month_revenue': time_periods['last_month']['total_revenue']
                }
            },
            'current_year_breakdown': {
                'payment_breakdown': payment_breakdown
            },
            'recent_activity': {
                'last_7_days_sales': recent_data['recent_count'] or 0,
                'last_7_days_revenue': float(recent_data['recent_revenue'] or 0)
            },
            'generated_at': timezone.now().isoformat()
        }
        
        # Add filter info to response
        filter_info = {}
        if merchant_id:
            try:
                merchant = Merchant.objects.get(id=merchant_id)
                filter_info['merchant'] = merchant.name
            except Merchant.DoesNotExist:
                pass
        if status_filter:
            filter_info['status'] = status_filter
        
        if filter_info:
            response_data['applied_filters'] = filter_info
        
        return Response({
            'status': 'success',
            'message': 'Dashboard revenue data retrieved successfully',
            'data': response_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Dashboard revenue error: {e}")
        logger.error(f"Dashboard revenue error: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET']) 
def get_quick_stats(request):
    """
    Get quick statistics with time period comparisons for dashboard cards (optimized for speed)
    """
    try:
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        from calendar import monthrange
        
        # Get current date info
        today = timezone.now().date()
        current_year = today.year
        current_month = today.month
        
        # Calculate date ranges
        current_year_start = today.replace(month=1, day=1)
        current_month_start = today.replace(day=1)
        
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
        
        # Base queryset
        base_sales = Sale.objects.exclude(status='cancelled')
        
        # Get merchant filter if provided
        merchant_id = request.GET.get('merchant_id')
        if merchant_id:
            base_sales = base_sales.filter(merchant_id=merchant_id)
        
        # Quick stats for different periods
        all_time_stats = base_sales.aggregate(
            total_revenue=Sum('final_amount'),
            total_sales=Count('id'),
            total_pending=Sum('pending_amount')
        )
        
        current_year_stats = base_sales.filter(harvest_date__date__gte=current_year_start).aggregate(
            total_revenue=Sum('final_amount'),
            total_sales=Count('id'),
            total_pending=Sum('pending_amount')
        )
        
        current_month_stats = base_sales.filter(harvest_date__date__gte=current_month_start).aggregate(
            total_revenue=Sum('final_amount'),
            total_sales=Count('id'),
            total_pending=Sum('pending_amount')
        )
        
        last_month_stats = base_sales.filter(
            harvest_date__date__range=[last_month_start, last_month_end]
        ).aggregate(
            total_revenue=Sum('final_amount'),
            total_sales=Count('id'),
            total_pending=Sum('pending_amount')
        )
        
        # Handle None values and format
        def format_stats(stats_dict, period_name):
            for key, value in stats_dict.items():
                if value is None:
                    stats_dict[key] = 0
            
            return {
                'period_name': period_name,
                'total_revenue': f"₹{stats_dict['total_revenue']:,.2f}",
                'total_revenue_raw': float(stats_dict['total_revenue']),
                'total_sales': stats_dict['total_sales'],
                'total_pending': f"₹{stats_dict['total_pending']:,.2f}",
                'total_pending_raw': float(stats_dict['total_pending'])
            }
        
        # Calculate month-over-month change
        current_month_revenue = float(current_month_stats['total_revenue'] or 0)
        last_month_revenue = float(last_month_stats['total_revenue'] or 0)
        
        if last_month_revenue > 0:
            month_change = round(((current_month_revenue - last_month_revenue) / last_month_revenue) * 100, 2)
        else:
            month_change = 100 if current_month_revenue > 0 else 0
        
        formatted_stats = {
            'all_time': format_stats(all_time_stats, 'All Time'),
            'current_year': format_stats(current_year_stats, f'Current Year ({current_year})'),
            'current_month': format_stats(current_month_stats, today.strftime('%B %Y')),
            'last_month': format_stats(last_month_stats, last_month_start.strftime('%B %Y')),
            'month_over_month_change': {
                'percentage': month_change,
                'trend': 'up' if month_change > 0 else 'down' if month_change < 0 else 'stable',
                'current_month_revenue': current_month_revenue,
                'last_month_revenue': last_month_revenue
            }
        }
        
        return Response({
            'status': 'success', 
            'data': formatted_stats,
            'generated_at': timezone.now().isoformat()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Quick stats error: {e}")
        logger.error(f"Quick stats error: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_revenue_by_period(request, period_type):
    """
    Get revenue data for a specific period type
    
    Parameters:
    - period_type: 'current_year', 'last_year', 'current_month', 'last_month', 'all_time'
    """
    try:
        from django.db.models import Sum, Count, Avg
        from django.utils import timezone
        from datetime import datetime, timedelta
        from calendar import monthrange
        
        today = timezone.now().date()
        current_year = today.year
        current_month = today.month
        
        # Determine date range based on period_type
        start_date = None
        end_date = None
        period_name = ''
        
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
        
        # Base queryset
        sales = Sale.objects.exclude(status='cancelled')
        
        # Apply merchant filter if provided
        merchant_id = request.GET.get('merchant_id')
        if merchant_id:
            sales = sales.filter(merchant_id=merchant_id)
        
        # Filter by date range
        if period_type != 'all_time' and start_date and end_date:
            sales = sales.filter(harvest_date__date__range=[start_date, end_date])
        
        # Calculate metrics
        metrics = sales.aggregate(
            total_revenue=Sum('final_amount'),
            total_paid=Sum('paid_amount'),
            total_pending=Sum('pending_amount'),
            total_sales_count=Count('id'),
            average_sale_amount=Avg('final_amount'),
            total_commission=Sum('commission'),
            total_deductions=Sum('total_deductions')
        )
        
        # Handle None values
        for key, value in metrics.items():
            if value is None:
                metrics[key] = 0
        
        # Calculate collection rate
        if metrics['total_revenue'] > 0:
            collection_rate = round((metrics['total_paid'] / metrics['total_revenue']) * 100, 2)
        else:
            collection_rate = 0
        
        # Payment status breakdown
        payment_breakdown = sales.values('payment_status').annotate(
            count=Count('id'),
            amount=Sum('final_amount')
        ).order_by('-amount')
        
        breakdown_dict = {
            'paid': {'count': 0, 'amount': 0},
            'partial': {'count': 0, 'amount': 0},
            'pending': {'count': 0, 'amount': 0}
        }
        
        for item in payment_breakdown:
            payment_status = item['payment_status']
            if payment_status in breakdown_dict:
                breakdown_dict[payment_status] = {
                    'count': item['count'],
                    'amount': float(item['amount'] or 0)
                }
        
        # Top sales for this period
        top_sales = sales.order_by('-final_amount')[:5]
        top_sales_list = []
        for sale in top_sales:
            top_sales_list.append({
                'id': sale.id,
                'final_amount': float(sale.final_amount),
                'harvest_date': sale.harvest_date.isoformat(),
                'merchant_name': sale.merchant.name if sale.merchant else 'N/A',
                'payment_status': sale.payment_status
            })
        
        response_data = {
            'period_info': {
                'type': period_type,
                'name': period_name,
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            },
            'metrics': {
                'total_revenue': float(metrics['total_revenue']),
                'total_paid': float(metrics['total_paid']),
                'total_pending': float(metrics['total_pending']),
                'total_sales_count': metrics['total_sales_count'],
                'average_sale_amount': round(float(metrics['average_sale_amount']), 2),
                'collection_rate': collection_rate,
                'total_commission': float(metrics['total_commission']),
                'total_deductions': float(metrics['total_deductions'])
            },
            'payment_breakdown': breakdown_dict,
            'top_sales': top_sales_list,
            'generated_at': timezone.now().isoformat()
        }
        
        return Response({
            'status': 'success',
            'message': f'Revenue data for {period_name} retrieved successfully',
            'data': response_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Revenue by period error: {e}")
        logger.error(f"Revenue by period error: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# FIXED: Complete expense dashboard function with proper status import
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
        
        # Import your Expense model here
        from ...models import Expense
        
        # Time period statistics
        time_periods = {}
        
        # Current Year
        current_year_expenses = Expense.objects.filter(date__range=[current_year_start, current_year_end])
        time_periods['current_year'] = {
            'count': current_year_expenses.count(),
            'total_amount': float(current_year_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Current Year ({current_year})',
            'start_date': current_year_start.isoformat(),
            'end_date': current_year_end.isoformat()
        }
        
        # Last Year
        last_year_expenses = Expense.objects.filter(date__range=[last_year_start, last_year_end])
        time_periods['last_year'] = {
            'count': last_year_expenses.count(),
            'total_amount': float(last_year_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Last Year ({last_year})',
            'start_date': last_year_start.isoformat(),
            'end_date': last_year_end.isoformat()
        }
        
        # Current Month
        current_month_expenses = Expense.objects.filter(date__range=[current_month_start, current_month_end])
        time_periods['current_month'] = {
            'count': current_month_expenses.count(),
            'total_amount': float(current_month_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Current Month ({today.strftime("%B %Y")})',
            'start_date': current_month_start.isoformat(),
            'end_date': current_month_end.isoformat()
        }
        
        # Last Month
        last_month_expenses = Expense.objects.filter(date__range=[last_month_start, last_month_end])
        month_name = last_month_start.strftime("%B %Y")
        time_periods['last_month'] = {
            'count': last_month_expenses.count(),
            'total_amount': float(last_month_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': f'Last Month ({month_name})',
            'start_date': last_month_start.isoformat(),
            'end_date': last_month_end.isoformat()
        }
        
        # Last 30 Days
        last_30_days_expenses = Expense.objects.filter(date__gte=last_30_days)
        time_periods['last_30_days'] = {
            'count': last_30_days_expenses.count(),
            'total_amount': float(last_30_days_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': 'Last 30 Days',
            'start_date': last_30_days.isoformat(),
            'end_date': today.isoformat()
        }
        
        # All Time (Whole Year Data)
        all_expenses = Expense.objects.all()
        time_periods['all_time'] = {
            'count': all_expenses.count(),
            'total_amount': float(all_expenses.aggregate(total=Sum('amount'))['total'] or 0),
            'period_name': 'All Time',
            'start_date': None,
            'end_date': None
        }
        
        # Category-wise statistics for current year
        category_stats = []
        if hasattr(Expense, 'CATEGORY_CHOICES'):
            for choice in Expense.CATEGORY_CHOICES:
                category_expenses = current_year_expenses.filter(category=choice[0])
                count = category_expenses.count()
                amount = category_expenses.aggregate(total=Sum('amount'))['total'] or 0
                
                category_stats.append({
                    'expense_category': choice[0],
                    'category_display': choice[1],
                    'count': count,
                    'total_amount': float(amount),
                    'percentage': round((float(amount) / time_periods['current_year']['total_amount'] * 100) if time_periods['current_year']['total_amount'] > 0 else 0, 2)
                })
        
        # Payment mode statistics for current year
        payment_mode_stats = []
        if hasattr(Expense, 'PAYMENT_MODE_CHOICES'):
            for choice in Expense.PAYMENT_MODE_CHOICES:
                mode_expenses = current_year_expenses.filter(mode_of_payment=choice[0])
                count = mode_expenses.count()
                amount = mode_expenses.aggregate(total=Sum('amount'))['total'] or 0
                
                payment_mode_stats.append({
                    'mode_of_payment': choice[0],
                    'mode_display': choice[1],
                    'count': count,
                    'total_amount': float(amount),
                    'percentage': round((float(amount) / time_periods['current_year']['total_amount'] * 100) if time_periods['current_year']['total_amount'] > 0 else 0, 2)
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
                'total_amount': float(spender['total_amount']),
                'percentage': round((float(spender['total_amount']) / time_periods['current_year']['total_amount'] * 100) if time_periods['current_year']['total_amount'] > 0 else 0, 2)
            })
        
        # Monthly trend for current year
        monthly_trend = current_year_expenses.extra(
            select={'month': 'EXTRACT(month FROM date)'}
        ).values('month').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('month')
        
        monthly_trend_list = []
        for month_data in monthly_trend:
            month_num = int(month_data['month'])
            month_name = datetime(current_year, month_num, 1).strftime('%B')
            monthly_trend_list.append({
                'month': month_num,
                'month_name': month_name,
                'count': month_data['count'],
                'total_amount': float(month_data['total_amount'] or 0)
            })
        
        # Recent expenses (last 7 days)
        recent_expenses = Expense.objects.filter(
            date__gte=today - timedelta(days=7)
        ).order_by('-date')[:10]
        
        recent_expenses_list = []
        for expense in recent_expenses:
            recent_expenses_list.append({
                'id': expense.id,
                'amount': float(expense.amount),
                'category': getattr(expense, 'category', 'N/A'),
                'spent_by': expense.spent_by,
                'date': expense.date.isoformat(),
                'description': getattr(expense, 'description', '') or ''
            })
        
        # Calculate percentage changes
        def calculate_percentage_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return round(((current - previous) / previous) * 100, 2)
        
        # Year-over-year comparison
        yearly_change = calculate_percentage_change(
            time_periods['current_year']['total_amount'],
            time_periods['last_year']['total_amount']
        )
        
        # Month-over-month comparison
        monthly_change = calculate_percentage_change(
            time_periods['current_month']['total_amount'],
            time_periods['last_month']['total_amount']
        )
        
        # Build response data
        response_data = {
            'time_periods': time_periods,
            'comparisons': {
                'yearly_comparison': {
                    'percentage_change': yearly_change,
                    'trend': 'up' if yearly_change > 0 else 'down' if yearly_change < 0 else 'stable',
                    'current_year_amount': time_periods['current_year']['total_amount'],
                    'last_year_amount': time_periods['last_year']['total_amount']
                },
                'monthly_comparison': {
                    'percentage_change': monthly_change,
                    'trend': 'up' if monthly_change > 0 else 'down' if monthly_change < 0 else 'stable',
                    'current_month_amount': time_periods['current_month']['total_amount'],
                    'last_month_amount': time_periods['last_month']['total_amount']
                }
            },
            'category_breakdown': category_stats,
            'payment_mode_breakdown': payment_mode_stats,
            'top_spenders': top_spenders_list,
            'monthly_trend': monthly_trend_list,
            'recent_expenses': recent_expenses_list,
            'generated_at': timezone.now().isoformat()
        }
        
        return Response({
            'status': 'success',
            'message': 'Expense dashboard statistics retrieved successfully',
            'data': response_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Expense dashboard error: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)