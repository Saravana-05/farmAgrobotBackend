from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Employee(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    EMP_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Contract', 'Contract'),
        ('Others', 'Others'),
    ]
    
    name = models.CharField(max_length=255)
    tamil_name = models.CharField(max_length=255)
    joining_date = models.DateField()
    emp_type = models.CharField(max_length=100, choices=EMP_TYPE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    contact = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'xe_employee'

    def __str__(self):
        return self.name
    
class Merchant(models.Model):

    PAYMENT_TERMS_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Online', 'Online'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    payment_terms = models.CharField(max_length=100, choices=PAYMENT_TERMS_CHOICES)
    contact = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'xe_merchant'

    def __str__(self):
        return self.name

class FarmSegment(models.Model):
    farm_name = models.CharField(max_length=255, verbose_name="Farm Name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'farm_segments'
        ordering = ['-created_at']
        verbose_name = 'Farm Segment'
        verbose_name_plural = 'Farm Segments'
    
    def __str__(self):
        return self.farm_name
    
class Crop(models.Model):
    crop_name = models.CharField(max_length=255, verbose_name="Crop Name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_crops'
        ordering = ['-created_at']
        verbose_name = 'Crop'
        verbose_name_plural = 'Crops'
    
    def __str__(self):
        return self.crop_name
    
class CropVariant(models.Model):
    UNIT_CHOICES = [
        ('Pieces', 'Pieces'),
        ('Bunch', 'Bunch'),
        ('Pack', 'Pack'),
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='variants')
    crop_variant = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'xe_crop_variants'
        unique_together = ['crop', 'crop_variant']  # Prevent duplicate variants for same crop

    def __str__(self):
        return f"{self.crop.crop_name} - {self.crop_variant}"

class Yield(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='yields')
    harvest_date = models.DateTimeField()
    bill_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_yields'
        ordering = ['-created_at']
        verbose_name = 'Yield'
        verbose_name_plural = 'Yields'
    
    def __str__(self):
        return f"{self.crop.crop_name} - {self.harvest_date.strftime('%Y-%m-%d')}"

class YieldFarmSegment(models.Model):
    """Junction table for yield and farm segments (many-to-many relationship)"""
    yield_record = models.ForeignKey(Yield, on_delete=models.CASCADE, related_name='yield_farm_segments')
    farm_segment = models.ForeignKey(FarmSegment, on_delete=models.CASCADE, related_name='yield_farm_segments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_yield_farm_segments'
        unique_together = ['yield_record', 'farm_segment']
    
    def __str__(self):
        return f"{self.yield_record} - {self.farm_segment.farm_name}"

class YieldVariant(models.Model):
    """Individual variant quantities for each yield record"""
    yield_record = models.ForeignKey(Yield, on_delete=models.CASCADE, related_name='yield_variants')
    crop_variant = models.ForeignKey(CropVariant, on_delete=models.CASCADE, related_name='yield_variants')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)  # Store the unit used at time of yield
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_yield_variants'
        unique_together = ['yield_record', 'crop_variant']
    
    def __str__(self):
        return f"{self.yield_record} - {self.crop_variant.crop_variant}: {self.quantity} {self.unit}"

class Sale(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Online', 'Online'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='sales')
    yield_record = models.ForeignKey(Yield, on_delete=models.CASCADE, related_name='sales')
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    harvest_date = models.DateTimeField()
    bill_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Financial fields
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    lorry_rent = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    cooly_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    total_calculated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_sales'
        ordering = ['-created_at']
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
    
    def __str__(self):
        return f"Sale {self.id} - {self.merchant.name} - ₹{self.final_amount}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total deductions and final amount
        self.total_deductions = self.commission + self.lorry_rent + self.cooly_charges
        self.final_amount = self.total_calculated_amount - self.total_deductions
        super().save(*args, **kwargs)

class SaleVariant(models.Model):
    """Individual variant sales data for each sale"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_variants')
    crop_variant = models.ForeignKey(CropVariant, on_delete=models.CASCADE, related_name='sale_variants')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    amount_per_unit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit = models.CharField(max_length=20)  # Store the unit used at time of sale
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_sale_variants'
        unique_together = ['sale', 'crop_variant']
    
    def __str__(self):
        return f"{self.sale.id} - {self.crop_variant.crop_variant}: {self.quantity} {self.unit}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total amount
        self.total_amount = self.quantity * self.amount_per_unit
        super().save(*args, **kwargs)

class Job(models.Model):
    JOB_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    job_name = models.CharField(max_length=255, verbose_name="Job Name")
    job_date = models.DateField(verbose_name="Job Date")
    job_status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='pending')
    no_of_employees = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_jobs'
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return f"{self.job_name} - {self.job_date}"

class JobFarmSegment(models.Model):
    """Junction table for job and farm segments (many-to-many relationship)"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_farm_segments')
    farm_segment = models.ForeignKey(FarmSegment, on_delete=models.CASCADE, related_name='job_farm_segments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_job_farm_segments'
        unique_together = ['job', 'farm_segment']
    
    def __str__(self):
        return f"{self.job.job_name} - {self.farm_segment.farm_name}"

class JobEmployee(models.Model):
    """Junction table for job and employees (many-to-many relationship)"""
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_employees')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='job_employees')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_job_employees'
        unique_together = ['job', 'employee']
    
    def __str__(self):
        return f"{self.job.job_name} - {self.employee.name}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
    ('Advance', 'Advance'),
    ('Food', 'Food'),
    ('Transport', 'Transport'),
    ('Donation and Give Away', 'Donation and Give Away'),
    ('Driver', 'Driver'),
    ('Miscellinious', 'Miscellinious'),
    ('Machine and Motor Repairs', 'Machine and Motor Repairs'),
    ('Jeep Maintenance', 'Jeep Maintenance'),
    ('Eb/Phone/Admin Exp', 'Eb/Phone/Admin Exp'),
    ('Fuel', 'Fuel'),
    ('Tree Samplings', 'Tree Samplings'),
    ('Farm Maintenance', 'Farm Maintenance'),
    ('Weekly Wages', 'Weekly Wages'),
]

    
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Bank', 'Bank'),
        ('Cheque', 'Cheque'),
    ]
    
    expense_name = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    spent_by = models.CharField(max_length=255)
    mode_of_payment = models.CharField(max_length=100, choices=PAYMENT_MODE_CHOICES)
    expense_image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'xe_expenses'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.expense_name} - {self.amount}"

class Wage(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='wages')
    effective_from = models.DateField(verbose_name="Effective From")
    effective_to = models.DateField(blank=True, null=True, verbose_name="Effective To")
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Wage Amount"
    )
    remarks = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_wages'
        ordering = ['-effective_from', '-created_at']
        verbose_name = 'Wage'
        verbose_name_plural = 'Wages'
        # Ensure no overlapping wage periods for the same employee
        constraints = [
            models.CheckConstraint(
                check=models.Q(effective_to__isnull=True) | models.Q(effective_to__gte=models.F('effective_from')),
                name='wage_effective_to_gte_effective_from'
            )
        ]
    
    def __str__(self):
        return f"{self.employee.name} - ₹{self.amount} (from {self.effective_from})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate that effective_to is after effective_from if provided
        if self.effective_to and self.effective_from and self.effective_to < self.effective_from:
            raise ValidationError('Effective to date must be after effective from date.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_current(self):
        """Check if this wage record is currently active"""
        from datetime import date
        today = date.today()
        
        if self.effective_to:
            return self.effective_from <= today <= self.effective_to
        else:
            return self.effective_from <= today
    
    @classmethod
    def get_current_wage(cls, employee):
        """Get the current active wage for an employee"""
        from datetime import date
        today = date.today()
        
        return cls.objects.filter(
            employee=employee,
            effective_from__lte=today
        ).filter(
            models.Q(effective_to__isnull=True) | models.Q(effective_to__gte=today)
        ).order_by('-effective_from').first()