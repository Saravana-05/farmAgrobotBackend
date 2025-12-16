from datetime import date, datetime
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import UserProfile,User, Page, Role, Jobs , JobAssignment
from .models import  AttendanceRecord, BillImage, BulkWagePayment, Employee,  Merchant, FarmSegment, Crop, CropVariant, PaymentHistory, SaleImage, Wage, WeeklyWagePayment,  Yield, YieldVariant, YieldFarmSegment, Sale, SaleVariant, Job, JobEmployee,JobFarmSegment, Expense, get_wage_for_date, ScrapedEvent



# Employee Serializer
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'tamil_name', 'joining_date', 
            'emp_type', 'gender','image_url',  
            'contact', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    
    
    def validate_contact(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Contact must contain only digits")
        if len(value) < 10:
            raise serializers.ValidationError("Contact must be at least 10 digits")
        return value

# Merchant Serializer   
class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id','name', 'address', 'payment_terms', 'contact', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']

    def validate_contact(self, value):
        """
        Validate contact number format (10 digits)
        """
        import re
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Please enter a valid 10-digit mobile number")
        return value

    def validate_name(self, value):
        """
        Validate merchant name is not empty
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Merchant name cannot be empty")
        return value.strip()

    def validate_address(self, value):
        """
        Validate address is not empty
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Address cannot be empty")
        return value.strip()

# Farm Segment Serializer
class FarmSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmSegment
        fields = ['id','farm_name', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']
    
    def validate_farm_name(self, value):
        """
        Validate farm name is not empty and has reasonable length
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Farm name cannot be empty")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Farm name must be at least 2 characters long")
        
        return value.strip()

# Crop Serializer
class CropSerializer(serializers.ModelSerializer):
    crop_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Crop
        fields = ['id', 'crop_name', 'crop_image', 'crop_image_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'crop_image_url']
    
    def get_crop_image_url(self, obj):
        """
        Return full URL for crop image if it exists
        """
        if obj.crop_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.crop_image.url)
            else:
                # Fallback if request context is not available
                return f"{settings.MEDIA_URL}{obj.crop_image.name}"
        return None
    
    def validate_crop_name(self, value):
        """
        Validate crop name is not empty and has reasonable length
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Crop name cannot be empty")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Crop name must be at least 2 characters long")
        
        return value.strip()
    
    def validate_crop_image(self, value):
        """
        Validate crop image if provided
        """
        if value:
            # Check file size (limit to 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file size should not exceed 5MB")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, GIF, and WebP images are allowed")
        
        return value
    
    def update(self, instance, validated_data):
        """
        Update crop instance, handling image replacement
        """
        # If a new image is provided, delete the old one
        if 'crop_image' in validated_data and validated_data['crop_image'] and instance.crop_image:
            try:
                instance.crop_image.delete(save=False)
            except Exception as e:
                print(f"Error deleting old image: {e}")
        
        return super().update(instance, validated_data)

# Crop Variant Serializer
class CropVariantSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source='crop.crop_name', read_only=True)
    crop_id = serializers.IntegerField(source='crop.id', read_only=True)
    crop = serializers.PrimaryKeyRelatedField(queryset=Crop.objects.all())

    class Meta:
        model = CropVariant
        fields = ['id', 'crop', 'crop_id', 'crop_name', 'crop_variant', 'unit', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_unit(self, value):
        valid_units = ['Pieces', 'Bunch', 'Pack']
        if value not in valid_units:
            raise serializers.ValidationError(f"Unit must be one of: {', '.join(valid_units)}")
        return value

class BillImageSerializer(serializers.ModelSerializer):
    """Serializer for bill images"""
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = BillImage
        fields = ['id', 'url', 'original_filename', 'file_size', 'uploaded_at','yield_record_id']
        read_only_fields = ['id', 'uploaded_at', 'file_size']
    
    def get_url(self, obj):
        """Get the absolute URL for the image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class YieldVariantSerializer(serializers.ModelSerializer):
    crop_variant_name = serializers.CharField(source='crop_variant.crop_variant', read_only=True)
    crop_variant_id = serializers.IntegerField(source='crop_variant.id', read_only=True)
    
    class Meta:
        model = YieldVariant
        fields = ['id', 'crop_variant_id', 'crop_variant_name', 'quantity', 'unit', 'created_at']
        read_only_fields = ['id', 'created_at']


class YieldFarmSegmentSerializer(serializers.ModelSerializer):
    farm_segment_name = serializers.CharField(source='farm_segment.farm_name', read_only=True)
    farm_segment_id = serializers.IntegerField(source='farm_segment.id', read_only=True)
    
    class Meta:
        model = YieldFarmSegment
        fields = ['id', 'farm_segment_id', 'farm_segment_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class YieldSerializer(serializers.ModelSerializer):
    """Main yield serializer with improved image handling"""
    crop_name = serializers.CharField(source='crop.crop_name', read_only=True)
    yield_variants = YieldVariantSerializer(many=True, read_only=True)
    yield_farm_segments = YieldFarmSegmentSerializer(many=True, read_only=True)
    bill_images = BillImageSerializer(many=True, read_only=True)
    
    # Backward compatibility
    bill_urls = serializers.SerializerMethodField()
    bill_count = serializers.SerializerMethodField()
    
    # Write-only fields for creation/update
    farm_segments = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
        required=True,
        help_text="List of farm segment IDs"
    )
    variants = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True,
        help_text="List of variant objects with crop_variant_id, quantity, unit"
    )
    
    class Meta:
        model = Yield
        fields = [
            'id', 'crop', 'crop_name', 'harvest_date', 
            'bill_images', 'bill_urls', 'bill_count',
            'created_at', 'updated_at', 
            'yield_variants', 'yield_farm_segments',
            'farm_segments', 'variants'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_bill_urls(self, obj):
        """Get list of bill URLs for backward compatibility"""
        request = self.context.get('request')
        urls = []
        for img in obj.bill_images.all():
            if img.image:
                if request:
                    urls.append(request.build_absolute_uri(img.image.url))
                else:
                    urls.append(img.image.url)
        return urls
    
    def get_bill_count(self, obj):
        """Get the number of bill images"""
        return obj.bill_images.count()
    
    def validate_farm_segments(self, value):
        """Validate that all farm segment IDs exist"""
        if not value:
            raise serializers.ValidationError("At least one farm segment must be selected.")
        
        existing_segments = FarmSegment.objects.filter(id__in=value)
        if len(existing_segments) != len(set(value)):
            raise serializers.ValidationError("One or more farm segments do not exist.")
        
        return list(set(value))  # Remove duplicates
    
    def validate_variants(self, value):
        """Validate variant data structure and existence"""
        if not value:
            raise serializers.ValidationError("At least one variant must be specified.")
        
        variant_ids = []
        for i, variant in enumerate(value):
            # Check required fields
            if not all(key in variant for key in ['crop_variant_id', 'unit', 'quantity']):
                raise serializers.ValidationError(
                    f"Variant {i+1}: Must have crop_variant_id, unit, and quantity."
                )
            
            # Validate types
            try:
                crop_variant_id = int(variant['crop_variant_id'])
                quantity = float(variant['quantity'])
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    f"Variant {i+1}: Invalid data types for crop_variant_id or quantity."
                )
            
            # Check for duplicates
            if crop_variant_id in variant_ids:
                raise serializers.ValidationError(
                    f"Variant {i+1}: Duplicate crop variant ID {crop_variant_id}."
                )
            variant_ids.append(crop_variant_id)
            
            # Validate variant exists
            if not CropVariant.objects.filter(id=crop_variant_id).exists():
                raise serializers.ValidationError(
                    f"Variant {i+1}: Crop variant with ID {crop_variant_id} does not exist."
                )
            
            # Validate quantity is positive
            if quantity <= 0:
                raise serializers.ValidationError(
                    f"Variant {i+1}: Quantity must be greater than 0."
                )
            
            # Normalize the data
            variant['crop_variant_id'] = crop_variant_id
            variant['quantity'] = quantity
            variant['unit'] = str(variant['unit']).strip()
        
        return value
    
    def create(self, validated_data):
        """Create yield with related objects"""
        farm_segments_data = validated_data.pop('farm_segments')
        variants_data = validated_data.pop('variants')
        
        # Create the yield record
        yield_record = Yield.objects.create(**validated_data)
        
        # Create farm segment relationships
        farm_segments_to_create = [
            YieldFarmSegment(yield_record=yield_record, farm_segment_id=segment_id)
            for segment_id in farm_segments_data
        ]
        YieldFarmSegment.objects.bulk_create(farm_segments_to_create)
        
        # Create variant records
        variants_to_create = [
            YieldVariant(
                yield_record=yield_record,
                crop_variant_id=variant_data['crop_variant_id'],
                quantity=variant_data['quantity'],
                unit=variant_data['unit']
            )
            for variant_data in variants_data
        ]
        YieldVariant.objects.bulk_create(variants_to_create)
        
        return yield_record
    
    def update(self, instance, validated_data):
        """Update yield with related objects"""
        farm_segments_data = validated_data.pop('farm_segments', None)
        variants_data = validated_data.pop('variants', None)
        
        # Update main yield fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update farm segments if provided
        if farm_segments_data is not None:
            # Clear existing relationships
            instance.yield_farm_segments.all().delete()
            # Create new relationships
            farm_segments_to_create = [
                YieldFarmSegment(yield_record=instance, farm_segment_id=segment_id)
                for segment_id in farm_segments_data
            ]
            YieldFarmSegment.objects.bulk_create(farm_segments_to_create)
        
        # Update variants if provided
        if variants_data is not None:
            # Clear existing variants
            instance.yield_variants.all().delete()
            # Create new variants
            variants_to_create = [
                YieldVariant(
                    yield_record=instance,
                    crop_variant_id=variant_data['crop_variant_id'],
                    quantity=variant_data['quantity'],
                    unit=variant_data['unit']
                )
                for variant_data in variants_data
            ]
            YieldVariant.objects.bulk_create(variants_to_create)
        
        return instance


class BillImageUploadSerializer(serializers.ModelSerializer):
    """Serializer specifically for uploading bill images"""
    
    class Meta:
        model = BillImage
        fields = ['image', 'original_filename']
        
    def validate_image(self, value):
        """Validate image file"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large. Maximum size is 10MB.")
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if hasattr(value, 'content_type') and value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Invalid image format. Allowed formats: JPEG, PNG, WebP."
            )
        
        return value


class YieldSummarySerializer(serializers.Serializer):
    """Serializer for yield summary data"""
    total_yields = serializers.IntegerField()
    total_bills = serializers.IntegerField()
    monthly_summary = serializers.ListField(child=serializers.DictField())
    crop_summary = serializers.ListField(child=serializers.DictField())
    variant_summary = serializers.ListField(child=serializers.DictField())
    
# Sale Image Serializer - NEW
class SaleImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SaleImage
        fields = [
            'id', 'image', 'image_url', 'image_name', 'description', 
            'is_primary', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


# Payment History Serializer - NEW
class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = [
            'id', 'payment_amount', 'payment_date', 'payment_method',
            'payment_reference', 'notes', 'created_by'
        ]
        read_only_fields = ['id', 'payment_date']


# Sale Variant Serializer - UNCHANGED
class SaleVariantSerializer(serializers.ModelSerializer):
    crop_variant_name = serializers.CharField(source='crop_variant.crop_variant', read_only=True)
    crop_name = serializers.CharField(source='crop_variant.crop.crop_name', read_only=True)
    
    class Meta:
        model = SaleVariant
        fields = [
            'id', 'crop_variant', 'crop_variant_name', 'crop_name',
            'quantity', 'amount_per_unit', 'total_amount', 'unit', 'created_at'
        ]
        read_only_fields = ['id', 'total_amount', 'created_at']


# Sale Serializer - UPDATED
class SaleSerializer(serializers.ModelSerializer):
    # Read-only fields for display
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    merchant_contact = serializers.CharField(source='merchant.contact', read_only=True)
    crop_name = serializers.CharField(source='yield_record.crop.crop_name', read_only=True)
    sale_variants = SaleVariantSerializer(many=True, read_only=True)
    sale_images = SaleImageSerializer(many=True, read_only=True)
    payment_history = PaymentHistorySerializer(many=True, read_only=True)
    
    # Write-only fields for creation/update
    variants = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True,
        help_text="List of variant data with variantId, quantity, amount, unit"
    )
    
    # Image upload field
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text="List of images to upload"
    )
    
    # Image metadata
    image_metadata = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
        help_text="List of image metadata with name, description, is_primary"
    )
    
    class Meta:
        model = Sale
        fields = [
            'id', 'merchant', 'merchant_name', 'merchant_contact',
            'yield_record', 'crop_name', 'payment_mode', 'harvest_date',
            'bill_url', 'total_amount', 'commission', 'lorry_rent',
            'cooly_charges', 'total_deductions', 'total_calculated_amount',
            'final_amount', 'paid_amount', 'pending_amount', 'payment_status',
            'status', 'created_at', 'updated_at', 'sale_variants', 
            'sale_images', 'payment_history', 'variants', 'images', 'image_metadata'
        ]
        read_only_fields = [
            'id', 'total_deductions', 'final_amount', 'pending_amount', 
            'payment_status', 'created_at', 'updated_at'
        ]
    
    def validate_merchant(self, value):
        """Validate merchant exists and is active"""
        if not Merchant.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Merchant does not exist")
        return value
    
    
    
    def validate_yield_record(self, value):
        """Validate yield record exists and is not already sold"""
        if not Yield.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Yield record does not exist")
        
        # Check if this yield is already sold (only for creation, not updates)
        if not self.instance:  # Creation
            existing_sale = Sale.objects.filter(yield_record=value).exclude(status='cancelled').first()
            if existing_sale:
                raise serializers.ValidationError("This yield record has already been sold")
        
        return value
    
    def validate_paid_amount(self, value):
        """Validate paid amount is not negative"""
        if value < 0:
            raise serializers.ValidationError("Paid amount cannot be negative")
        return value
    
    def validate_variants(self, value):
        """Validate variant data structure and availability"""
        if not value:
            raise serializers.ValidationError("At least one variant must be specified.")
        
        for variant in value:
            # Check required fields
            required_fields = ['crop_variant_id', 'quantity', 'amount', 'unit']
            if not all(key in variant for key in required_fields):
                raise serializers.ValidationError(
                    f"Each variant must have: {', '.join(required_fields)}"
                )
            
            # Validate variant exists
            try:
                crop_variant = CropVariant.objects.get(id=variant['crop_variant_id'])
            except CropVariant.DoesNotExist:
                raise serializers.ValidationError(
                    f"Crop variant with ID {variant['crop_variant_id']} does not exist."
                )
            
            # Validate quantity and amount are positive
            if variant['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0.")
            
            if variant['amount'] <= 0:
                raise serializers.ValidationError("Amount per unit must be greater than 0.")
        
        return value
    
    def validate_image_metadata(self, value):
        """Validate image metadata if provided"""
        if value:
            for metadata in value:
                if 'name' not in metadata:
                    metadata['name'] = ''
                if 'description' not in metadata:
                    metadata['description'] = ''
                if 'is_primary' not in metadata:
                    metadata['is_primary'] = False
        return value
    
    
    
    def validate(self, data):
        """Cross-field validation"""
        # Validate that harvest_date is not in the future
        from django.utils import timezone
        if data.get('harvest_date') and data['harvest_date'] > timezone.now():
            raise serializers.ValidationError("Harvest date cannot be in the future.")
        
        # Validate financial calculations if variants are provided
        if 'variants' in data:
            calculated_total = sum(
                Decimal(str(variant['quantity'])) * Decimal(str(variant['amount']))
                for variant in data['variants']
            )
            
            # Allow small floating-point differences
            if abs(calculated_total - data.get('total_calculated_amount', 0)) > Decimal('0.01'):
                raise serializers.ValidationError(
                    f"Total calculated amount ({data.get('total_calculated_amount')}) "
                    f"does not match sum of variants ({calculated_total})"
                )
        
        # Validate paid amount doesn't exceed final amount
        if 'paid_amount' in data and 'total_calculated_amount' in data:
            commission = data.get('commission', 0)
            lorry_rent = data.get('lorry_rent', 0)
            cooly_charges = data.get('cooly_charges', 0)
            total_deductions = commission + lorry_rent + cooly_charges
            final_amount = data['total_calculated_amount'] - total_deductions
            
            if data['paid_amount'] > final_amount:
                raise serializers.ValidationError("Paid amount cannot exceed final amount")
        
        # Validate images and metadata count match
        images = data.get('images', [])
        image_metadata = data.get('image_metadata', [])
        
        if images and image_metadata and len(images) != len(image_metadata):
            raise serializers.ValidationError("Number of images and metadata must match")
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        images_data = validated_data.pop('images', [])
        image_metadata = validated_data.pop('image_metadata', [])
        
        # Create the sale record
        sale = Sale.objects.create(**validated_data)
        
        # Create variant records
        for variant_data in variants_data:
            SaleVariant.objects.create(
                sale=sale,
                crop_variant_id=variant_data['crop_variant_id'],
                quantity=Decimal(str(variant_data['quantity'])),
                amount_per_unit=Decimal(str(variant_data['amount'])),
                unit=variant_data['unit']
            )
        
        # Create image records - FIXED: Handle multiple images properly
        print(f"Creating {len(images_data)} images for sale {sale.id}")
        for i, image in enumerate(images_data):
            metadata = image_metadata[i] if i < len(image_metadata) else {}
            
            # Set first image as primary if no is_primary is specified
            is_primary = metadata.get('is_primary', i == 0)
            
            sale_image = SaleImage.objects.create(
                sale=sale,
                image=image,
                image_name=metadata.get('name', f'Image {i+1}'),
                description=metadata.get('description', ''),
                is_primary=is_primary
            )
            print(f"Created SaleImage {sale_image.id}: {sale_image.image_name}")
        
        return sale
    
    @transaction.atomic
    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', None)
        images_data = validated_data.pop('images', [])
        image_metadata = validated_data.pop('image_metadata', [])
        
        # Track old paid amount for payment history
        old_paid_amount = instance.paid_amount
        
        # Update main sale fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update variants if provided
        if variants_data is not None:
            # Clear existing variants
            instance.sale_variants.all().delete()
            
            # Create new variants
            for variant_data in variants_data:
                SaleVariant.objects.create(
                    sale=instance,
                    crop_variant_id=variant_data['crop_variant_id'],
                    quantity=Decimal(str(variant_data['quantity'])),
                    amount_per_unit=Decimal(str(variant_data['amount'])),
                    unit=variant_data['unit']
                )
        
        # Add new images if provided - FIXED: Handle multiple images properly
        if images_data:
            print(f"Adding {len(images_data)} new images to sale {instance.id}")
            
            # Check if we should make any of the new images primary
            has_existing_primary = instance.sale_images.filter(is_primary=True).exists()
            
            for i, image in enumerate(images_data):
                metadata = image_metadata[i] if i < len(image_metadata) else {}
                
                # If no existing primary image, make first new image primary
                is_primary = metadata.get('is_primary', not has_existing_primary and i == 0)
                
                sale_image = SaleImage.objects.create(
                    sale=instance,
                    image=image,
                    image_name=metadata.get('name', f'Updated Image {i+1}'),
                    description=metadata.get('description', ''),
                    is_primary=is_primary
                )
                print(f"Added new SaleImage {sale_image.id}: {sale_image.image_name}")
        
        # Create payment history record if paid amount changed
        new_paid_amount = instance.paid_amount
        if new_paid_amount != old_paid_amount and new_paid_amount > old_paid_amount:
            payment_amount = new_paid_amount - old_paid_amount
            PaymentHistory.objects.create(
                sale=instance,
                payment_amount=payment_amount,
                payment_method=instance.payment_mode,
                notes=f"Payment updated via sale update"
            )
        
        return instance


# Sale summary serializer - UPDATED
class SaleSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for sale summaries/lists"""
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    crop_name = serializers.CharField(source='yield_record.crop.crop_name', read_only=True)
    variant_count = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Sale
        fields = [
            'id', 'merchant_name', 'crop_name', 'payment_mode',
            'harvest_date', 'final_amount', 'paid_amount', 'pending_amount',
            'payment_status', 'status', 'variant_count', 'image_count', 
            'primary_image', 'created_at'
        ]
    
    def get_variant_count(self, obj):
        return obj.sale_variants.count()
    
    def get_image_count(self, obj):
        return obj.sale_images.count()
    
    def get_primary_image(self, obj):
        primary_image = obj.sale_images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None


# Payment Update Serializer - NEW
class PaymentUpdateSerializer(serializers.Serializer):
    payment_amount = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_method = serializers.ChoiceField(choices=Sale.PAYMENT_MODE_CHOICES)
    payment_reference = serializers.CharField(max_length=100, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    created_by = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    def validate_payment_amount(self, value):
        """Validate payment amount doesn't exceed pending amount"""
        if hasattr(self, 'instance') and self.instance:
            if value > self.instance.pending_amount:
                raise serializers.ValidationError(
                    f"Payment amount (₹{value}) cannot exceed pending amount (₹{self.instance.pending_amount})"
                )
        return value

# Job Farm Segment serializers
class JobFarmSegmentSerializer(serializers.ModelSerializer):
    farm_segment_name = serializers.CharField(source='farm_segment.farm_name', read_only=True)
    farm_segment_id = serializers.CharField(source='farm_segment.id', read_only=True)
    
    class Meta:
        model = JobFarmSegment
        fields = ['id', 'farm_segment_id', 'farm_segment_name', 'created_at']
        read_only_fields = ['id', 'created_at']

# Job Employee serializer
class JobEmployeeSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_tamil_name = serializers.CharField(source='employee.tamil_name', read_only=True)
    employee_id = serializers.CharField(source='employee.id', read_only=True)
    
    class Meta:
        model = JobEmployee
        fields = ['id', 'employee_id', 'employee_name', 'employee_tamil_name', 'created_at']
        read_only_fields = ['id', 'created_at']

# Job serializer
class JobSerializer(serializers.ModelSerializer):
    # Read-only fields for display
    job_farm_segments = JobFarmSegmentSerializer(many=True, read_only=True)
    job_employees = JobEmployeeSerializer(many=True, read_only=True)
    
    # Write-only fields for creation/update
    farm_segment_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=True,
        help_text="List of farm segment IDs"
    )
    employee_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=True,
        help_text="List of employee IDs"
    )
    
    class Meta:
        model = Job
        fields = [
            'id', 'job_name', 'job_date', 'job_status', 'no_of_employees',
            'created_at', 'updated_at', 'job_farm_segments', 'job_employees',
            'farm_segment_ids', 'employee_ids'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_job_name(self, value):
        """Validate job name is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Job name cannot be empty")
        return value.strip()
    
    def validate_farm_segment_ids(self, value):
        """Validate that all farm segment IDs exist"""
        if not value:
            raise serializers.ValidationError("At least one farm segment must be selected.")
        
        existing_segments = FarmSegment.objects.filter(id__in=value)
        if len(existing_segments) != len(value):
            missing_ids = set(value) - set(str(seg.id) for seg in existing_segments)
            raise serializers.ValidationError(f"Farm segments with IDs {list(missing_ids)} do not exist.")
        
        return value
    
    def validate_employee_ids(self, value):
        """Validate that all employee IDs exist and are active"""
        if not value:
            raise serializers.ValidationError("At least one employee must be selected.")
        
        existing_employees = Employee.objects.filter(id__in=value, status=True)
        if len(existing_employees) != len(value):
            existing_ids = set(str(emp.id) for emp in existing_employees)
            missing_ids = set(value) - existing_ids
            raise serializers.ValidationError(f"Employees with IDs {list(missing_ids)} do not exist or are inactive.")
        
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        # Validate that job_date is not in the past
        from django.utils import timezone
        from datetime import date
        
        if data.get('job_date') and data['job_date'] < date.today():
            raise serializers.ValidationError("Job date cannot be in the past.")
        
        # Validate that no_of_employees matches the number of employee_ids
        employee_ids = data.get('employee_ids', [])
        no_of_employees = data.get('no_of_employees', 0)
        
        if len(employee_ids) != no_of_employees:
            raise serializers.ValidationError(
                f"Number of employees ({no_of_employees}) does not match "
                f"the number of employee IDs provided ({len(employee_ids)})"
            )
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        farm_segment_ids = validated_data.pop('farm_segment_ids')
        employee_ids = validated_data.pop('employee_ids')
        
        # Create the job record
        job = Job.objects.create(**validated_data)
        
        # Create farm segment relationships
        for segment_id in farm_segment_ids:
            JobFarmSegment.objects.create(
                job=job,
                farm_segment_id=segment_id
            )
        
        # Create employee relationships
        for employee_id in employee_ids:
            JobEmployee.objects.create(
                job=job,
                employee_id=employee_id
            )
        
        return job
    
    @transaction.atomic
    def update(self, instance, validated_data):
        # Extract nested data
        farm_segment_ids = validated_data.pop('farm_segment_ids', None)
        employee_ids = validated_data.pop('employee_ids', None)
        
        # Update main job fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update farm segments if provided
        if farm_segment_ids is not None:
            # Clear existing relationships
            instance.job_farm_segments.all().delete()
            # Create new relationships
            for segment_id in farm_segment_ids:
                JobFarmSegment.objects.create(
                    job=instance,
                    farm_segment_id=segment_id
                )
        
        # Update employees if provided
        if employee_ids is not None:
            # Clear existing relationships
            instance.job_employees.all().delete()
            # Create new relationships
            for employee_id in employee_ids:
                JobEmployee.objects.create(
                    job=instance,
                    employee_id=employee_id
                )
        
        return instance

# Job summary serializer
class JobSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for job summaries/lists"""
    farm_segment_count = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()
    farm_segment_names = serializers.SerializerMethodField()
    employee_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'job_name', 'job_date', 'job_status', 'no_of_employees',
            'farm_segment_count', 'employee_count', 'farm_segment_names',
            'employee_names', 'created_at'
        ]
    
    def get_farm_segment_count(self, obj):
        return obj.job_farm_segments.count()
    
    def get_employee_count(self, obj):
        return obj.job_employees.count()
    
    def get_farm_segment_names(self, obj):
        return [jfs.farm_segment.farm_name for jfs in obj.job_farm_segments.all()]
    
    def get_employee_names(self, obj):
        return [
            {
                'name': je.employee.name,
                'tamil_name': je.employee.tamil_name
            }
            for je in obj.job_employees.all()
        ]

# Job status update serializer
class JobStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating only job status"""
    
    class Meta:
        model = Job
        fields = ['job_status']
    
    def validate_job_status(self, value):
        """Validate job status choice"""
        valid_statuses = [choice[0] for choice in Job.JOB_STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Valid choices are: {valid_statuses}")
        return value

# Expense Serializer   
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'id', 'expense_name', 'date', 'category', 'description', 
            'amount', 'spent_by', 'mode_of_payment', 'expense_image_url', 
             'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        if value > Decimal('999999999.99'):
            raise serializers.ValidationError("Amount is too large")
        return value
    
    def validate_expense_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Expense name cannot be empty")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Expense name must be at least 2 characters")
        return value.strip()
    
    def validate_spent_by(self, value):
        # Make spent_by optional - only validate if provided
        if value is not None and value.strip():
            return value.strip()
        # Return empty string or None if not provided (depending on your model field requirements)
        return value  # or return "" if your model requires a string
    
# Wages Serializer
class WageSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_contact = serializers.CharField(source='employee.contact', read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Wage
        fields = [
            'id', 'employee', 'employee_name', 'employee_contact',
            'effective_from', 'effective_to', 'amount', 'remarks',
            'is_current', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_current']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Wage amount must be greater than 0")
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Wage amount is too large")
        return value
    
    def validate_effective_from(self, value):
        if not value:
            raise serializers.ValidationError("Effective from date is required")
        return value
    
    def validate(self, data):
        effective_from = data.get('effective_from')
        effective_to = data.get('effective_to')
        
        # Validate date range
        if effective_from and effective_to and effective_to < effective_from:
            raise serializers.ValidationError("Effective to date must be after effective from date")
        
        # Check for overlapping wage periods for the same employee
        employee = data.get('employee')
        if employee:
            # Get existing wages for this employee
            existing_wages = Wage.objects.filter(employee=employee)
            
            # If this is an update, exclude the current instance
            if self.instance:
                existing_wages = existing_wages.exclude(id=self.instance.id)
            
            # Check for overlaps
            for wage in existing_wages:
                if self._check_date_overlap(effective_from, effective_to, wage.effective_from, wage.effective_to):
                    raise serializers.ValidationError(
                        f"This wage period overlaps with existing wage from {wage.effective_from} to {wage.effective_to or 'present'}"
                    )
        
        return data
    
    def _check_date_overlap(self, start1, end1, start2, end2):
        """Check if two date ranges overlap"""
        # If either range has no end date, treat it as ongoing
        if end1 is None:
            end1 = date.max
        if end2 is None:
            end2 = date.max
        
        # Check for overlap
        return start1 <= end2 and start2 <= end1
    
class AttendanceEmployeeSerializer(serializers.Serializer):
    """Serializer for individual employee attendance within a date"""
    employee_id = serializers.CharField()
    employee_name = serializers.CharField()
    status = serializers.IntegerField()
    wage_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def validate_status(self, value):
        """Validate attendance status values"""
        valid_statuses = [0, 1, 2, 3]  # Absent, Present, Half Day, Late
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Must be one of: {valid_statuses} "
                "(0=Absent, 1=Present, 2=Half Day, 3=Late)"
            )
        return value

    def validate_employee_id(self, value):
        """Validate that employee ID exists and is active"""
        try:
            employee = Employee.objects.get(id=value, status=True)
            return value
        except Employee.DoesNotExist:
            raise serializers.ValidationError(
                f"Employee with ID {value} does not exist or is inactive"
            )

    def validate(self, data):
        """Cross-field validation for employee data"""
        employee_id = data.get('employee_id')
        employee_name = data.get('employee_name')
        
        if employee_id and employee_name:
            try:
                employee = Employee.objects.get(id=employee_id, status=True)
                if employee.name != employee_name:
                    raise serializers.ValidationError({
                        'employee_name': f"Employee name mismatch. Expected: '{employee.name}', Got: '{employee_name}'"
                    })
                
                # Check if employee has a current wage
                current_wage = Wage.get_current_wage(employee)
                if not current_wage:
                    raise serializers.ValidationError({
                        'employee_id': f"Employee '{employee.name}' does not have a current wage rate"
                    })
                    
            except Employee.DoesNotExist:
                raise serializers.ValidationError({
                    'employee_id': f"Employee with ID {employee_id} does not exist or is inactive"
                })
        
        return data


class AttendanceCreateUpdateSerializer(serializers.Serializer):
    """Enhanced serializer with historical wage validation"""
    date = serializers.DateField()
    attendance_records = AttendanceEmployeeSerializer(many=True)

    def validate_attendance_records(self, value):
        """Validate attendance records with historical wage checks"""
        if not value:
            raise serializers.ValidationError("At least one employee attendance record is required.")
        
        attendance_date = self.initial_data.get('date')
        if attendance_date:
            try:
                target_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
            except ValueError:
                raise serializers.ValidationError("Invalid date format.")
        else:
            raise serializers.ValidationError("Date is required for wage validation.")
        
        # Check for duplicate employee IDs
        employee_ids = [record['employee_id'] for record in value]
        if len(employee_ids) != len(set(employee_ids)):
            duplicates = [emp_id for emp_id in set(employee_ids) if employee_ids.count(emp_id) > 1]
            raise serializers.ValidationError(
                f"Duplicate employee IDs found: {duplicates}"
            )
        
        # Validate each employee has a wage rate for the target date
        employees_without_wages = []
        for record in value:
            employee_id = record['employee_id']
            try:
                employee = Employee.objects.get(id=employee_id, status=True)
                historical_wage = get_wage_for_date(employee, target_date)
                
                if not historical_wage:
                    employees_without_wages.append(f"{employee.name} (ID: {employee_id})")
                    
            except Employee.DoesNotExist:
                raise serializers.ValidationError(
                    f"Employee with ID {employee_id} does not exist or is inactive"
                )
        
        if employees_without_wages:
            raise serializers.ValidationError(
                f"The following employees don't have wage rates for {target_date}: {', '.join(employees_without_wages)}"
            )
        
        return value

    def create(self, validated_data):
        """Create attendance record with historical wage amounts"""
        attendance_date = validated_data['date']
        attendance_records = validated_data['attendance_records']
        
        with transaction.atomic():
            attendance_data = []
            for record_data in attendance_records:
                employee_id = record_data['employee_id']
                employee = Employee.objects.get(id=employee_id, status=True)
                
                # FIXED: Get historical wage for the attendance date
                historical_wage = get_wage_for_date(employee, attendance_date)
                wage_amount = historical_wage.amount if historical_wage else Decimal('0')
                
                attendance_data.append({
                    'employee_id': employee_id,
                    'employee_name': employee.name,
                    'status': record_data['status'],
                    'wage_amount': float(wage_amount),
                    'wage_effective_from': historical_wage.effective_from.isoformat() if historical_wage else None,
                    'wage_effective_to': historical_wage.effective_to.isoformat() if historical_wage and historical_wage.effective_to else None
                })
            
            attendance_record, created = AttendanceRecord.objects.update_or_create(
                date=attendance_date,
                defaults={
                    'attendance_data': attendance_data
                }
            )
            
            return attendance_record

    def update(self, instance, validated_data):
        """Update attendance record with historical wage amounts"""
        attendance_date = instance.date
        attendance_records = validated_data['attendance_records']
        
        attendance_data = []
        for record_data in attendance_records:
            employee_id = record_data['employee_id']
            employee = Employee.objects.get(id=employee_id, status=True)
            
            # FIXED: Get historical wage for the attendance date
            historical_wage = get_wage_for_date(employee, attendance_date)
            wage_amount = historical_wage.amount if historical_wage else Decimal('0')
            
            attendance_data.append({
                'employee_id': employee_id,
                'employee_name': employee.name,
                'status': record_data['status'],
                'wage_amount': float(wage_amount),
                'wage_effective_from': historical_wage.effective_from.isoformat() if historical_wage else None,
                'wage_effective_to': historical_wage.effective_to.isoformat() if historical_wage and historical_wage.effective_to else None
            })
        
        instance.attendance_data = attendance_data
        instance.save()
        return instance



class AttendanceRecordSerializer(serializers.ModelSerializer):
    """Serializer for displaying attendance records"""
    total_employees = serializers.ReadOnlyField()
    total_present = serializers.ReadOnlyField()
    total_absent = serializers.ReadOnlyField()
    total_half_day = serializers.ReadOnlyField()
    daily_wages_total = serializers.SerializerMethodField()
    attendance_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = AttendanceRecord
        fields = [
            'id', 'date', 'attendance_data', 'total_employees',
            'total_present', 'total_absent', 'total_half_day',
            'daily_wages_total', 'attendance_summary', 'created_at', 'last_updated'
        ]
    
    def get_daily_wages_total(self, obj):
        """Calculate total wages for the day"""
        return float(obj.calculate_daily_wages_total())
    
    def get_attendance_summary(self, obj):
        """Get formatted attendance summary"""
        return {
            'date': obj.date.isoformat(),
            'total_employees': obj.total_employees,
            'present': obj.total_present,
            'absent': obj.total_absent,
            'half_day': obj.total_half_day,
            'daily_wages': self.get_daily_wages_total(obj)
        }


class WeeklyWagePaymentSerializer(serializers.ModelSerializer):
    """Serializer for weekly wage payments"""
    employee_name = serializers.CharField(read_only=True)
    employee_details = serializers.SerializerMethodField()
    
    class Meta:
        model = WeeklyWagePayment
        fields = '__all__'
    
    def get_employee_details(self, obj):
        """Get additional employee details"""
        return {
            'id': str(obj.employee.id),
            'name': obj.employee.name,
            'is_active': obj.employee.status
        }


class PayWageSerializer(serializers.Serializer):
    """Enhanced serializer for processing wage payments"""
    employee_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_mode = serializers.ChoiceField(
        choices=WeeklyWagePayment.PAYMENT_MODE_CHOICES, 
        default='Cash'
    )
    payment_reference = serializers.CharField(required=False, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_blank=True)
    is_partial = serializers.BooleanField(default=False)

    def validate_employee_id(self, value):
        """Validate that employee exists and is active"""
        try:
            employee = Employee.objects.get(id=value, status=True)
            return value
        except Employee.DoesNotExist:
            raise serializers.ValidationError(
                f"Employee with ID {value} does not exist or is inactive"
            )

    def validate_amount(self, value):
        """Validate payment amount"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate(self, data):
        """Cross-field validation for payment data"""
        employee_id = data.get('employee_id')
        amount = data.get('amount')
        
        # Additional validation can be added here
        # For example, checking if amount doesn't exceed remaining balance
        
        return data


class WeeklyAttendanceSerializer(serializers.Serializer):
    """Enhanced serializer for weekly attendance summary"""
    employee_id = serializers.CharField()
    employee_name = serializers.CharField()
    daily_wage = serializers.DecimalField(max_digits=10, decimal_places=2)
    attendance = serializers.DictField()  # {date: status}
    present_days = serializers.IntegerField()
    half_days = serializers.IntegerField()
    absent_days = serializers.IntegerField(default=0)
    late_days = serializers.IntegerField(default=0)
    total_wages = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_status = serializers.CharField()
    partial_payment = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    week_summary = serializers.SerializerMethodField()

    def get_week_summary(self, obj):
        """Get formatted week summary"""
        total_work_days = obj.get('present_days', 0) + obj.get('half_days', 0)
        return {
            'total_work_days': total_work_days,
            'attendance_percentage': round(
                (total_work_days / 7) * 100, 2
            ) if total_work_days > 0 else 0,
            'wages_per_day': float(obj.get('total_wages', 0)) / max(total_work_days, 1)
        }


class EmployeeAttendanceValidationSerializer(serializers.Serializer):
    """Serializer for validating employee existence before attendance marking"""
    employee_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False
    )
    
    def validate_employee_ids(self, value):
        """Validate that all employee IDs exist and are active"""
        if not value:
            raise serializers.ValidationError("Employee IDs list cannot be empty")
        
        # Check for duplicates
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate employee IDs found")
        
        # Check if all employees exist and are active
        existing_employees = Employee.objects.filter(
            id__in=value, 
            status=True
        ).values_list('id', flat=True)
        
        existing_ids = set(str(emp_id) for emp_id in existing_employees)
        missing_ids = set(value) - existing_ids
        
        if missing_ids:
            raise serializers.ValidationError(
                f"The following employee IDs do not exist or are inactive: {list(missing_ids)}"
            )
        
        return value

class BulkWagePaymentSerializer(serializers.ModelSerializer):
    """Serializer for bulk wage payments"""
    paid_by_username = serializers.CharField(source='paid_by.username', read_only=True)
    employee_count = serializers.IntegerField(source='total_employees', read_only=True)
    
    class Meta:
        model = BulkWagePayment
        fields = [
            'id', 'week_start_date', 'week_end_date', 'payment_date',
            'employee_payments', 'total_employees', 'employee_count',
            'total_amount', 'payment_mode', 'payment_reference', 'remarks',
            'expense_category', 'paid_by', 'paid_by_username', 'created_at'
        ]


class BulkPaymentCreateSerializer(serializers.Serializer):
    """Serializer for creating bulk wage payments"""
    week_start = serializers.DateField()
    payment_mode = serializers.ChoiceField(
        choices=BulkWagePayment.PAYMENT_MODE_CHOICES, 
        default='Cash'
    )
    payment_reference = serializers.CharField(required=False, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_blank=True)
    
    def validate_week_start(self, value):
        """Validate week start date"""
        if value > date.today():
            raise serializers.ValidationError("Cannot create bulk payment for future weeks.")
        
        # Check if bulk payment already exists for this week
        if BulkWagePayment.objects.filter(week_start_date=value).exists():
            raise serializers.ValidationError("Bulk payment already exists for this week.")
        
        return value



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedEvent
        fields = '__all__'
#jobs
class JobsSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(default=timezone.localdate)
    end_date = serializers.DateField(required = False) 
    class Meta:
        model = Jobs
        fields = '__all__'  
        
    def validate(self,data):
        start_date = data.get("start_date", getattr(self.instance,'start_date', None))
        end_date = data.get("end_date", getattr(self.instance,'end_date', None))
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("end_date cannot be before start_date")        
        return data
   
#Register
class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','username','email','password','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data['password'],
        )
        role, created = Role.objects.get_or_create(name = role.strip().capitalize())
        UserProfile.objects.create(user = user , role = role)
        return user
    def update(self, instance, validated_data):
        role = validated_data.pop('role')
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        if role:
            role, created = Role.objects.get_or_create(name  = role.strip().capitalize())
            profile = UserProfile.objects.get(user = instance)
            profile.role = role
            profile.save()
        return instance
    
# Assigning page access based on their role    
class AssignPageSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    page = serializers.ListField(
        child = serializers.CharField(max_length = 100 )
    )

 
