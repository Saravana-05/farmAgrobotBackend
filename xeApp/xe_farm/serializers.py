from datetime import date
from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Employee, Merchant, FarmSegment, Crop, CropVariant, Wage, Yield, YieldVariant, YieldFarmSegment, Sale, SaleVariant, Job, JobEmployee,JobFarmSegment, Expense

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
    class Meta:
        model = Crop
        fields = ['id','crop_name', 'created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']
    
    def validate_crop_name(self, value):
        """
        Validate crop name is not empty and has reasonable length
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Crop name cannot be empty")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Crop name must be at least 2 characters long")
        
        return value.strip()

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

# Yield Variant Serializer    
class YieldVariantSerializer(serializers.ModelSerializer):
    crop_variant_name = serializers.CharField(source='crop_variant.crop_variant', read_only=True)
    crop_variant_id = serializers.IntegerField(source='crop_variant.id', read_only=True)
    
    class Meta:
        model = YieldVariant
        fields = ['id', 'crop_variant_id', 'crop_variant_name', 'quantity', 'unit', 'created_at']
        read_only_fields = ['id', 'created_at']

# Yield Farm Segment Serializer
class YieldFarmSegmentSerializer(serializers.ModelSerializer):
    farm_segment_name = serializers.CharField(source='farm_segment.farm_name', read_only=True)
    farm_segment_id = serializers.IntegerField(source='farm_segment.id', read_only=True)
    
    class Meta:
        model = YieldFarmSegment
        fields = ['id', 'farm_segment_id', 'farm_segment_name', 'created_at']
        read_only_fields = ['id', 'created_at']

# Yield Serializer
class YieldSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source='crop.crop_name', read_only=True)
    yield_variants = YieldVariantSerializer(many=True, read_only=True)
    yield_farm_segments = YieldFarmSegmentSerializer(many=True, read_only=True)
    
    # For write operations
    farm_segments = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
        required=True
    )
    variants = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Yield
        fields = [
            'id', 'crop', 'crop_name', 'harvest_date', 'bill_url', 
            'created_at', 'updated_at', 'yield_variants', 'yield_farm_segments',
            'farm_segments', 'variants'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_farm_segments(self, value):
        """Validate that all farm segment IDs exist"""
        if not value:
            raise serializers.ValidationError("At least one farm segment must be selected.")
        
        existing_segments = FarmSegment.objects.filter(id__in=value)
        if len(existing_segments) != len(value):
            raise serializers.ValidationError("One or more farm segments do not exist.")
        
        return value
    
    def validate_variants(self, value):
        """Validate variant data structure and existence"""
        if not value:
            raise serializers.ValidationError("At least one variant must be specified.")
        
        for variant in value:
            if not all(key in variant for key in ['variantId', 'unit', 'quantity']):
                raise serializers.ValidationError("Each variant must have variantId, unit, and quantity.")
            
            # Validate variant exists
            try:
                CropVariant.objects.get(id=variant['variantId'])
            except CropVariant.DoesNotExist:
                raise serializers.ValidationError(f"Crop variant with ID {variant['variantId']} does not exist.")
            
            # Validate quantity is positive
            if variant['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0.")
        
        return value
    
    def create(self, validated_data):
        farm_segments_data = validated_data.pop('farm_segments')
        variants_data = validated_data.pop('variants')
        
        # Create the yield record
        yield_record = Yield.objects.create(**validated_data)
        
        # Create farm segment relationships
        for segment_id in farm_segments_data:
            YieldFarmSegment.objects.create(
                yield_record=yield_record,
                farm_segment_id=segment_id
            )
        
        # Create variant records
        for variant_data in variants_data:
            YieldVariant.objects.create(
                yield_record=yield_record,
                crop_variant_id=variant_data['variantId'],
                quantity=variant_data['quantity'],
                unit=variant_data['unit']
            )
        
        return yield_record
    
    def update(self, instance, validated_data):
        # Extract nested data
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
            for segment_id in farm_segments_data:
                YieldFarmSegment.objects.create(
                    yield_record=instance,
                    farm_segment_id=segment_id
                )
        
        # Update variants if provided
        if variants_data is not None:
            # Clear existing variants
            instance.yield_variants.all().delete()
            # Create new variants
            for variant_data in variants_data:
                YieldVariant.objects.create(
                    yield_record=instance,
                    crop_variant_id=variant_data['variantId'],
                    quantity=variant_data['quantity'],
                    unit=variant_data['unit']
                )
        
        return instance

# Sale Serializer
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

# Sale Serializer
class SaleSerializer(serializers.ModelSerializer):
    # Read-only fields for display
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    merchant_contact = serializers.CharField(source='merchant.contact', read_only=True)
    crop_name = serializers.CharField(source='yield_record.crop.crop_name', read_only=True)
    sale_variants = SaleVariantSerializer(many=True, read_only=True)
    
    # Write-only fields for creation/update
    variants = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True,
        help_text="List of variant data with variantId, quantity, amount, unit"
    )
    
    class Meta:
        model = Sale
        fields = [
            'id', 'merchant', 'merchant_name', 'merchant_contact',
            'yield_record', 'crop_name', 'payment_mode', 'harvest_date',
            'bill_url', 'total_amount', 'commission', 'lorry_rent',
            'cooly_charges', 'total_deductions', 'total_calculated_amount',
            'final_amount', 'status', 'created_at', 'updated_at',
            'sale_variants', 'variants'
        ]
        read_only_fields = [
            'id', 'total_deductions', 'final_amount', 'created_at', 'updated_at'
        ]
    
    def validate_merchant(self, value):
        """Validate merchant exists and is active"""
        if not Merchant.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Merchant does not exist")
        return value
    
    def validate_yield_record(self, value):
        """Validate yield record exists"""
        if not Yield.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Yield record does not exist")
        return value
    
    def validate_variants(self, value):
        """Validate variant data structure and availability"""
        if not value:
            raise serializers.ValidationError("At least one variant must be specified.")
        
        for variant in value:
            # Check required fields
            required_fields = ['variantId', 'quantity', 'amount', 'unit']
            if not all(key in variant for key in required_fields):
                raise serializers.ValidationError(
                    f"Each variant must have: {', '.join(required_fields)}"
                )
            
            # Validate variant exists
            try:
                crop_variant = CropVariant.objects.get(id=variant['variantId'])
            except CropVariant.DoesNotExist:
                raise serializers.ValidationError(
                    f"Crop variant with ID {variant['variantId']} does not exist."
                )
            
            # Validate quantity and amount are positive
            if variant['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0.")
            
            if variant['amount'] <= 0:
                raise serializers.ValidationError("Amount per unit must be greater than 0.")
        
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
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        
        # Create the sale record
        sale = Sale.objects.create(**validated_data)
        
        # Create variant records
        for variant_data in variants_data:
            SaleVariant.objects.create(
                sale=sale,
                crop_variant_id=variant_data['variantId'],
                quantity=Decimal(str(variant_data['quantity'])),
                amount_per_unit=Decimal(str(variant_data['amount'])),
                unit=variant_data['unit']
            )
        
        return sale
    
    @transaction.atomic
    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', None)
        
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
                    crop_variant_id=variant_data['variantId'],
                    quantity=Decimal(str(variant_data['quantity'])),
                    amount_per_unit=Decimal(str(variant_data['amount'])),
                    unit=variant_data['unit']
                )
        
        return instance

# Sale summary serializer
class SaleSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for sale summaries/lists"""
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    crop_name = serializers.CharField(source='yield_record.crop.crop_name', read_only=True)
    variant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Sale
        fields = [
            'id', 'merchant_name', 'crop_name', 'payment_mode',
            'harvest_date', 'final_amount', 'status', 'variant_count',
            'created_at'
        ]
    
    def get_variant_count(self, obj):
        return obj.sale_variants.count()

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
        if not value.strip():
            raise serializers.ValidationError("Expense name cannot be empty")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Expense name must be at least 2 characters")
        return value.strip()
    
    def validate_spent_by(self, value):
        if not value.strip():
            raise serializers.ValidationError("Spent by field cannot be empty")
        return value.strip()

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