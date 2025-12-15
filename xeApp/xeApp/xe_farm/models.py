import os
import sys
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.forms import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.validators import URLValidator
from django.db import models
from django.contrib.auth.models import User


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
    crop_image = models.ImageField(upload_to='crops/', null=True, blank=True, verbose_name="Crop Image")
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


def bill_image_upload_path(instance, filename):
    """Generate upload path for bill images"""
    # Get file extension
    ext = filename.split('.')[-1] if '.' in filename else 'jpg'
    # Generate unique filename
    filename = f"yield_bill_{uuid.uuid4().hex[:16]}.{ext}"
    # Return path: uploads/bills/YYYY/MM/filename
    return os.path.join('uploads', 'bills', str(instance.yield_record.harvest_date.year), 
                       str(instance.yield_record.harvest_date.month).zfill(2), filename)


class Yield(models.Model):
    crop = models.ForeignKey('Crop', on_delete=models.CASCADE, related_name='yields')
    harvest_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'xe_yields'
        ordering = ['-created_at']
        verbose_name = 'Yield'
        verbose_name_plural = 'Yields'

    def __str__(self):
        return f"{self.crop.crop_name} - {self.harvest_date.strftime('%Y-%m-%d')}"
    
    @property
    def bill_count(self):
        """Get the number of bill images"""
        return self.bill_images.count()
    
    @property
    def has_bills(self):
        """Check if yield has any bill images"""
        return self.bill_images.exists()
    
    @property
    def bill_urls(self):
        """Get list of bill image URLs for backward compatibility"""
        return [img.get_absolute_url() for img in self.bill_images.all()]


class BillImage(models.Model):
    """Separate model for bill images"""
    yield_record = models.ForeignKey(Yield, on_delete=models.CASCADE, related_name='bill_images')
    image = models.ImageField(upload_to=bill_image_upload_path, max_length=500)
    original_filename = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)  # in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_bill_images'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Bill for {self.yield_record} - {self.original_filename}"
    
    def save(self, *args, **kwargs):
        if self.image and not self.original_filename:
            self.original_filename = self.image.name
        if self.image and not self.file_size:
            self.file_size = self.image.size
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Override delete to remove file from storage"""
        if self.image:
            # Delete the actual file
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    def get_absolute_url(self):
        """Get the absolute URL for the image"""
        if self.image:
            return self.image.url
        return None
    
    @property
    def filename(self):
        """Get just the filename"""
        if self.image:
            return os.path.basename(self.image.name)
        return None


class YieldFarmSegment(models.Model):
    """Junction table for yield and farm segments (many-to-many relationship)"""
    yield_record = models.ForeignKey(Yield, on_delete=models.CASCADE, related_name='yield_farm_segments')
    farm_segment = models.ForeignKey('FarmSegment', on_delete=models.CASCADE, related_name='yield_farm_segments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_yield_farm_segments'
        unique_together = ['yield_record', 'farm_segment']
    
    def __str__(self):
        return f"{self.yield_record} - {self.farm_segment.farm_name}"


class YieldVariant(models.Model):
    """Individual variant quantities for each yield record"""
    yield_record = models.ForeignKey(Yield, on_delete=models.CASCADE, related_name='yield_variants')
    crop_variant = models.ForeignKey('CropVariant', on_delete=models.CASCADE, related_name='yield_variants')
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
    
    # Payment status choices - NEW
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
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
    
    # Payment tracking fields - NEW
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
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
        
        # Auto-calculate payment status and pending amount
        if self.paid_amount >= self.final_amount:
            self.payment_status = 'paid'
            self.pending_amount = Decimal('0.00')
            self.paid_amount = self.final_amount  # Ensure no overpayment
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
            self.pending_amount = self.final_amount - self.paid_amount
        else:
            self.payment_status = 'pending'
            self.pending_amount = self.final_amount
        
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


class SaleImage(models.Model):
    """Model to store multiple images for each sale - NEW"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_images')
    image = models.ImageField(upload_to='sale_images/')
    image_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_sale_images'
        ordering = ['-is_primary', '-uploaded_at']
    
    def __str__(self):
        return f"Sale {self.sale.id} - Image {self.id}"
    
    def save(self, *args, **kwargs):
        # If this is marked as primary, unmark all other images for this sale
        if self.is_primary:
            SaleImage.objects.filter(sale=self.sale, is_primary=True).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)


class PaymentHistory(models.Model):
    """Track payment history for each sale - NEW"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payment_history')
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=Sale.PAYMENT_MODE_CHOICES)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)  # Store user info if needed
    
    class Meta:
        db_table = 'xe_payment_history'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment {self.id} - Sale {self.sale.id} - ₹{self.payment_amount}"

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
    spent_by = models.CharField(max_length=255, blank=True, null=True)
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
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
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
    

class AttendanceRecord(models.Model):
    """
    Single attendance record per date with JSON field containing all employee data
    """
    date = models.DateField(unique=True, verbose_name="Attendance Date")
    
    # JSON field to store array of employee attendance records

    attendance_data = models.JSONField(
        default=list,
        verbose_name="Attendance Data",
        help_text="Array of employee attendance records"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'Employee', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_attendance_records',
        verbose_name="Created By"
    )
    
    class Meta:
        db_table = 'xe_attendance_records'
        ordering = ['-date']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
    
    def __str__(self):
        return f"Attendance for {self.date}"
    
    @property
    def total_employees(self):
        """Get total number of employees in this record"""
        return len(self.attendance_data)
    
    @property
    def total_present(self):
        """Get total number of employees present"""
        return len([emp for emp in self.attendance_data if emp.get('status') == 1])
    
    @property
    def total_absent(self):
        """Get total number of employees absent"""
        return len([emp for emp in self.attendance_data if emp.get('status') == 0])
    
    @property
    def total_half_day(self):
        """Get total number of employees on half day"""
        return len([emp for emp in self.attendance_data if emp.get('status') == 2])
    
    def get_employee_status(self, employee_id):
        """Get attendance status for specific employee"""
        for emp_data in self.attendance_data:
            if str(emp_data.get('employee_id')) == str(employee_id):
                return emp_data.get('status')
        return None
    
    def update_employee_status(self, employee_id, employee_name, status, wage_amount=None):
        """Update or add employee attendance status"""
        # Find existing employee record
        for i, emp_data in enumerate(self.attendance_data):
            if str(emp_data.get('employee_id')) == str(employee_id):
                # Update existing record
                self.attendance_data[i].update({
                    'employee_name': employee_name,
                    'status': status,
                    'wage_amount': float(wage_amount) if wage_amount else emp_data.get('wage_amount')
                })
                self.save()
                return
        
        # Add new employee record
        new_record = {
            'employee_id': str(employee_id),
            'employee_name': employee_name,
            'status': status,
            'wage_amount': float(wage_amount) if wage_amount else 0.0
        }
        self.attendance_data.append(new_record)
        self.save()
    
    def calculate_daily_wages_total(self):
        """Calculate total wages for this day based on present employees"""
        total = Decimal('0.00')
        for emp_data in self.attendance_data:
            if emp_data.get('status') == 1:  # Present
                wage_amount = emp_data.get('wage_amount', 0)
                total += Decimal(str(wage_amount))
            elif emp_data.get('status') == 2:  # Half Day
                wage_amount = emp_data.get('wage_amount', 0)
                total += Decimal(str(wage_amount)) / 2
        return total




class WeeklyWagePayment(models.Model):
    
    """
    Store weekly wage payments as a single record with employee data as JSON array
    Much more efficient than individual records per employee
    """
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Bank', 'Bank'),
        ('Cheque', 'Cheque'),
    ]
    
    # Week identification
    week_start_date = models.DateField(unique=True, verbose_name="Week Start Date")
    week_end_date = models.DateField(verbose_name="Week End Date")
    
    # Employee wage data stored as JSON array
    employee_wages = models.JSONField(
        default=list,
        verbose_name="Employee Wage Data",
        help_text="Array of employee wage objects with payment details"
    )
    
    # Summary fields for quick access
    total_employees = models.PositiveIntegerField(default=0)
    total_gross_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_deductions = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_net_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_paid_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_remaining_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Overall payment status for the week
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional: Link to a single expense entry for the entire week
    expense_entry = models.OneToOneField(
        'Expense',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='weekly_wage_payment',
        verbose_name="Associated Expense Entry"
    )
    
    class Meta:
        db_table = 'xe_weekly_wage_payment'
        ordering = ['-week_start_date']
        verbose_name = 'Weekly Wage Payment Record'
        verbose_name_plural = 'Weekly Wage Payment Records'
    
    def __str__(self):
        return f"Week {self.week_start_date} - {self.total_employees} employees (₹{self.total_net_amount})"
    
    def save(self, *args, **kwargs):
        # Auto-calculate week end date
        if self.week_start_date and not self.week_end_date:
            self.week_end_date = self.week_start_date + timedelta(days=6)
        
        # Update summary fields from employee data
        self._update_summary_fields()
        
        super().save(*args, **kwargs)
    
    def _update_summary_fields(self):
        """Update summary fields based on employee_wages data"""
        if not self.employee_wages:
            return
        
        self.total_employees = len(self.employee_wages)
        self.total_gross_amount = Decimal('0.00')
        self.total_deductions = Decimal('0.00')
        self.total_net_amount = Decimal('0.00')
        self.total_paid_amount = Decimal('0.00')
        self.total_remaining_amount = Decimal('0.00')
        
        paid_count = 0
        pending_count = 0
        
        for emp_data in self.employee_wages:
            gross = Decimal(str(emp_data.get('gross_amount', 0)))
            deductions = Decimal(str(emp_data.get('total_deductions', 0)))
            net = Decimal(str(emp_data.get('net_amount', 0)))
            paid = Decimal(str(emp_data.get('paid_amount', 0)))
            remaining = Decimal(str(emp_data.get('remaining_amount', 0)))
            
            self.total_gross_amount += gross
            self.total_deductions += deductions
            self.total_net_amount += net
            self.total_paid_amount += paid
            self.total_remaining_amount += remaining
            
            # Count payment statuses
            emp_status = emp_data.get('payment_status', 'pending')
            if emp_status == 'paid':
                paid_count += 1
            elif emp_status == 'pending':
                pending_count += 1
        
        # Determine overall payment status
        if paid_count == self.total_employees:
            self.payment_status = 'paid'
        elif paid_count == 0:
            self.payment_status = 'pending'
        else:
            self.payment_status = 'partial'

    
    @classmethod
    def generate_weekly_wage_record(cls, week_start_date):
        """
        Generate weekly wage record for all employees for given week
        Returns the created record with employee wage data
        """
        from datetime import timedelta
        
        # Check if record already exists
        existing_record = cls.objects.filter(week_start_date=week_start_date).first()
        if existing_record:
            return existing_record
        
        week_end_date = week_start_date + timedelta(days=6)
        week_dates = [week_start_date + timedelta(days=i) for i in range(7)]
        
        # Get attendance records for the week
        attendance_records = AttendanceRecord.objects.filter(
            date__in=week_dates
        )
        
        # Create attendance lookup
        attendance_lookup = {record.date: record.attendance_data for record in attendance_records}
        
        # Get all active employees
        employees = Employee.objects.filter(status=True)
        
        employee_wages_data = []
        
        for employee in employees:
            emp_id = str(employee.id)
            current_wage = Wage.get_current_wage(employee)
            daily_wage = current_wage.amount if current_wage else Decimal('0')
            
            if daily_wage == 0:
                continue  # Skip employees without wage rates
            
            # Calculate attendance for this employee
            present_days = 0
            half_days = 0
            late_days = 0
            attendance_details = {}
            
            for week_date in week_dates:
                date_str = week_date.isoformat()
                employee_status = None
                
                if week_date in attendance_lookup and attendance_lookup[week_date]:
                    # Find this employee's status
                    for emp_data in attendance_lookup[week_date]:
                        if str(emp_data.get('employee_id')) == emp_id:
                            employee_status = emp_data.get('status')
                            break
                
                attendance_details[date_str] = employee_status
                
                # Count days by status
                if employee_status == 1:  # Present
                    present_days += 1
                elif employee_status == 2:  # Half day
                    half_days += 1
                elif employee_status == 3:  # Late (treat as present)
                    late_days += 1
                    present_days += 1
            
            # Calculate wages
            gross_amount = (present_days * daily_wage) + (half_days * daily_wage / 2)
            
            # Employee wage data object
            employee_wage_data = {
                'employee_id': emp_id,
                'employee_name': employee.name,
                'present_days': present_days,
                'half_days': half_days,
                'late_days': late_days,
                'daily_wage': float(daily_wage),
                'gross_amount': float(gross_amount),
                'advance_deduction': 0.0,
                'other_deductions': 0.0,
                'total_deductions': 0.0,
                'net_amount': float(gross_amount),
                'paid_amount': 0.0,
                'remaining_amount': float(gross_amount),
                'payment_status': 'pending',
                'payment_mode': None,
                'payment_date': None,
                'payment_reference': '',
                'remarks': '',
                'attendance_details': attendance_details
            }
            
            employee_wages_data.append(employee_wage_data)
        
        # Create the record
        record = cls.objects.create(
            week_start_date=week_start_date,
            employee_wages=employee_wages_data
        )
        
        return record
    
    def get_employee_wage_data(self, employee_id):
        """Get wage data for a specific employee"""
        for emp_data in self.employee_wages:
            if str(emp_data.get('employee_id')) == str(employee_id):
                return emp_data
        return None
    
    def update_employee_payment(self, employee_id, payment_amount, payment_mode='Cash', reference='', remarks=''):
        """
        Update employee payment with validation against historical wage calculations
        """
        employee_id = str(employee_id)
        employee = Employee.objects.get(id=employee_id)
        
        # Find this employee in the wages data
        employee_found = False
        for i, emp_data in enumerate(self.employee_wages):
            if emp_data.get('employee_id') == employee_id:
                employee_found = True
                current_paid = Decimal(str(emp_data.get('paid_amount', 0)))
                net_amount = Decimal(str(emp_data.get('net_amount', 0)))
                
                # Validate payment doesn't exceed net amount
                if current_paid + payment_amount > net_amount:
                    raise ValueError(
                        f"Payment amount ${payment_amount} exceeds remaining balance ${net_amount - current_paid}"
                    )
                
                # Update payment details
                new_paid_amount = current_paid + payment_amount
                remaining_amount = net_amount - new_paid_amount
                
                # Determine payment status
                if remaining_amount <= 0:
                    payment_status = 'paid'
                elif new_paid_amount > 0:
                    payment_status = 'partial'
                else:
                    payment_status = 'pending'
                
                # Update the employee data
                self.employee_wages[i].update({
                    'paid_amount': float(new_paid_amount),
                    'remaining_amount': float(remaining_amount),
                    'payment_status': payment_status,
                    'last_payment_date': timezone.now().date().isoformat(),
                    'payment_mode': payment_mode,
                    'payment_reference': reference,
                    'payment_remarks': remarks
                })
                
                break
        
        if not employee_found:
            raise ValueError(f"Employee {employee.name} not found in this wage record")
        
        # Recalculate totals
        total_paid = sum(Decimal(str(emp.get('paid_amount', 0))) for emp in self.employee_wages)
        total_remaining = sum(Decimal(str(emp.get('remaining_amount', 0))) for emp in self.employee_wages)
        
        self.total_paid_amount = total_paid
        self.total_remaining_amount = total_remaining
        
        # Update overall payment status
        if total_remaining <= 0:
            self.payment_status = 'Fully Paid'
        elif total_paid > 0:
            self.payment_status = 'Partial'
        else:
            self.payment_status = 'Pending'
        
        self.save()
        return new_paid_amount

    
    def make_bulk_payment(self, payment_mode='Cash', reference='', remarks=''):
        """
        Pay all pending wages in bulk
        """
        total_payment = Decimal('0.00')
        
        for emp_data in self.employee_wages:
            remaining = Decimal(str(emp_data.get('remaining_amount', 0)))
            
            if remaining > 0:
                emp_data['paid_amount'] = emp_data['net_amount']
                emp_data['remaining_amount'] = 0.0
                emp_data['payment_status'] = 'paid'
                emp_data['payment_mode'] = payment_mode
                emp_data['payment_reference'] = reference
                emp_data['payment_date'] = timezone.now().isoformat()
                
                if remarks:
                    emp_data['remarks'] = remarks
                
                total_payment += remaining
        
        # Create single expense entry for bulk payment
        if total_payment > 0 and not self.expense_entry:
            expense = Expense.objects.create(
                expense_name=f'Weekly Wages - Week {self.week_start_date}',
                date=timezone.now().date(),
                category='Weekly Wages',
                description=f'Bulk wage payment for week {self.week_start_date} to {self.week_end_date} ({self.total_employees} employees)',
                amount=total_payment,
                spent_by='Admin',
                mode_of_payment=payment_mode
            )
            self.expense_entry = expense
        
        self.save()
        return float(total_payment)
    
    def get_payment_summary(self):
        """Get payment summary for the week"""
        summary = {
            'week_start_date': self.week_start_date.isoformat(),
            'week_end_date': self.week_end_date.isoformat(),
            'total_employees': self.total_employees,
            'total_gross_amount': float(self.total_gross_amount),
            'total_net_amount': float(self.total_net_amount),
            'total_paid_amount': float(self.total_paid_amount),
            'total_remaining_amount': float(self.total_remaining_amount),
            'payment_status': self.payment_status,
            'employees_paid': len([e for e in self.employee_wages if e.get('payment_status') == 'paid']),
            'employees_partial': len([e for e in self.employee_wages if e.get('payment_status') == 'partial']),
            'employees_pending': len([e for e in self.employee_wages if e.get('payment_status') == 'pending'])
        }
        return summary
    
class WeeklyWagePaymentManager:
    """Updated manager methods for WeeklyWagePayment"""
    
    @classmethod
    def generate_weekly_wage_record_with_historical_rates(cls, week_start_date):
        """
        Generate weekly wage record using historical wage rates for each attendance date
        This replaces the existing generate_weekly_wage_record method
        """
        from django.db import transaction
        from collections import defaultdict
        from datetime import timedelta
        # Import your models here
        from .models import WeeklyWagePayment, AttendanceRecord, Employee  # Adjust import path as needed
        
        week_end_date = week_start_date + timedelta(days=6)
        week_dates = [week_start_date + timedelta(days=i) for i in range(7)]
        
        # Check if record already exists - FIXED: Use WeeklyWagePayment.objects
        existing_record = WeeklyWagePayment.objects.filter(week_start_date=week_start_date).first()
        if existing_record:
            return existing_record
        
        # Get all attendance records for the week
        attendance_records = AttendanceRecord.objects.filter(
            date__in=week_dates
        )
        
        # Build employee wage data using historical rates
        employee_wages_data = []
        employees_processed = set()
        
        # Process each attendance record
        for attendance_record in attendance_records:
            attendance_date = attendance_record.date
            
            for emp_attendance in attendance_record.attendance_data:
                emp_id = emp_attendance.get('employee_id')
                emp_name = emp_attendance.get('employee_name')
                status = emp_attendance.get('status')
                
                if emp_id not in employees_processed:
                    employees_processed.add(emp_id)
                    
                    try:
                        employee = Employee.objects.get(id=emp_id, status=True)
                        
                        # Calculate wages for this employee across the week using historical rates
                        employee_week_data = cls._calculate_employee_week_wages_historical(
                            employee, week_dates, attendance_records
                        )
                        
                        if employee_week_data and employee_week_data['net_amount'] > 0:  # Only include if employee worked
                            employee_wages_data.append(employee_week_data)
                            
                    except Employee.DoesNotExist:
                        continue
        
        # Create the wage record - FIXED: Use WeeklyWagePayment.objects
        with transaction.atomic():
            wage_record = WeeklyWagePayment.objects.create(
                week_start_date=week_start_date,
                week_end_date=week_end_date,
                employee_wages=employee_wages_data,
                total_employees=len(employee_wages_data),
                total_gross_amount=sum(Decimal(str(emp['gross_amount'])) for emp in employee_wages_data),
                total_net_amount=sum(Decimal(str(emp['net_amount'])) for emp in employee_wages_data),
                total_paid_amount=Decimal('0'),
                total_remaining_amount=sum(Decimal(str(emp['net_amount'])) for emp in employee_wages_data),
                payment_status='pending'
            )
        
        return wage_record

    @classmethod  
    def _calculate_employee_week_wages_historical(cls, employee, week_dates, attendance_records):
        """
        Calculate employee wages for a week using historical wage rates for each day
        FIXED: Ensures daily_wage field uses historical rate, not current rate
        """
        import sys
        from decimal import Decimal
        
        
        emp_id = str(employee.id)
        week_start_date = week_dates[0]  # First date of the week
        
        # CRITICAL FIX: Get historical wage rate for the week start date
        primary_historical_wage = get_wage_for_date(employee, week_start_date)
        if not primary_historical_wage:
            # If no historical wage found for week start, try to find any wage for this employee
            all_wages = employee.wage_set.filter(
                effective_from__lte=week_start_date
            ).order_by('-effective_from').first()
            
            if not all_wages:
                print(f"No wage rate found for employee {employee.name} on {week_start_date}", file=sys.stderr)
                return None
            
            primary_historical_wage = all_wages
        
        # This should be the historical rate (e.g., 45), not current rate (e.g., 500)
        primary_daily_wage = primary_historical_wage.amount
        
        print(f"Employee {employee.name}: Using historical wage rate {primary_daily_wage} for week {week_start_date}", file=sys.stderr)
        
        # Build attendance lookup
        attendance_lookup = {}
        for record in attendance_records:
            attendance_lookup[record.date] = {
                emp['employee_id']: emp for emp in record.attendance_data
            }
        
        # Calculate attendance and wages day by day with historical rates
        total_present_days = 0
        total_half_days = 0
        total_late_days = 0
        total_wages = Decimal('0')
        attendance_details = {}
        daily_wage_rates_used = []
        
        for day_date in week_dates:
            date_str = day_date.isoformat()
            
            # Get historical wage rate for this specific date
            daily_historical_wage = get_wage_for_date(employee, day_date)
            daily_wage_for_this_date = daily_historical_wage.amount if daily_historical_wage else primary_daily_wage
            daily_wage_rates_used.append(float(daily_wage_for_this_date))
            
            # Get attendance status for this day
            attendance_status = None
            day_wage_earned = Decimal('0')
            
            if day_date in attendance_lookup and emp_id in attendance_lookup[day_date]:
                emp_day_data = attendance_lookup[day_date][emp_id]
                attendance_status = emp_day_data.get('status')
                
                # Calculate wage using historical rate for this specific date
                if attendance_status == 1:  # Present
                    day_wage_earned = daily_wage_for_this_date
                    total_present_days += 1
                elif attendance_status == 2:  # Half day
                    day_wage_earned = daily_wage_for_this_date / 2
                    total_half_days += 1
                elif attendance_status == 3:  # Late (treat as present)
                    day_wage_earned = daily_wage_for_this_date
                    total_late_days += 1
                    total_present_days += 1  # Count as present for totals
            
            total_wages += day_wage_earned
            
            # Store detailed attendance with actual wage rate used
            attendance_details[date_str] = {
                'status': attendance_status,
                'wage_rate': float(daily_wage_for_this_date),
                'wage_earned': float(day_wage_earned),
                'wage_effective_from': daily_historical_wage.effective_from.isoformat() if daily_historical_wage else primary_historical_wage.effective_from.isoformat(),
                'wage_effective_to': daily_historical_wage.effective_to.isoformat() if daily_historical_wage and daily_historical_wage.effective_to else None
            }
        
        # Calculate deductions (implement as needed)
        advance_deduction = Decimal('0')
        other_deductions = Decimal('0')
        total_deductions = advance_deduction + other_deductions
        net_amount = total_wages - total_deductions
        
        print(f"Employee {employee.name} calculations:", file=sys.stderr)
        print(f"  - Primary historical wage: {primary_daily_wage}", file=sys.stderr)
        print(f"  - Daily rates used: {daily_wage_rates_used}", file=sys.stderr)
        print(f"  - Total wages: {total_wages}", file=sys.stderr)
        
        return {
            'employee_id': emp_id,
            'employee_name': employee.name,
            'present_days': total_present_days,
            'half_days': total_half_days,
            'late_days': total_late_days,
            'daily_wage': float(primary_daily_wage),  # FIXED: This is now historical rate
            'gross_amount': float(total_wages),
            'advance_deduction': float(advance_deduction),
            'other_deductions': float(other_deductions),
            'total_deductions': float(total_deductions),
            'net_amount': float(net_amount),
            'paid_amount': 0.0,
            'remaining_amount': float(net_amount),
            'payment_status': 'pending',
            'payment_mode': '',
            'payment_date': None,
            'payment_reference': '',
            'remarks': '',
            'attendance_details': attendance_details,
            'last_payment_date': None,
            'payment_remarks': '',
            'historical_wage_calculation': {
                'enabled': True,
                'primary_wage_rate': float(primary_daily_wage),
                'effective_from': primary_historical_wage.effective_from.isoformat(),
                'effective_to': primary_historical_wage.effective_to.isoformat() if primary_historical_wage.effective_to else None,
                'daily_rates_used': daily_wage_rates_used,
                'multiple_rates_in_week': len(set(daily_wage_rates_used)) > 1,
                'calculation_date': week_start_date.isoformat()
            }
        }


    def recalculate_with_historical_rates(self):
        """
        Recalculate existing wage record using historical rates
        FIXED: Ensures daily_wage field reflects historical rates
        """
        week_dates = [self.week_start_date + timedelta(days=i) for i in range(7)]
        attendance_records = AttendanceRecord.objects.filter(date__in=week_dates)
        
        print(f"Recalculating wage record {self.id} for week {self.week_start_date} with historical rates")
        
        # Recalculate each employee's data
        updated_employee_wages = []
        
        for emp_data in self.employee_wages:
            employee_id = emp_data['employee_id']
            
            try:
                employee = Employee.objects.get(id=employee_id, status=True)
            except Employee.DoesNotExist:
                # Keep existing data if employee not found
                updated_employee_wages.append(emp_data)
                continue
            
            # Get historical wage data for this employee
            recalculated_data = self._calculate_employee_week_wages_historical(
                employee, week_dates, attendance_records
            )
            
            if recalculated_data is None:
                # Keep existing data if calculation failed
                updated_employee_wages.append(emp_data)
                continue
            
            # Preserve existing payment information
            paid_amount = Decimal(str(emp_data.get('paid_amount', 0)))
            payment_status = emp_data.get('payment_status', 'pending')
            payment_mode = emp_data.get('payment_mode', '')
            payment_reference = emp_data.get('payment_reference', '')
            last_payment_date = emp_data.get('last_payment_date')
            payment_remarks = emp_data.get('payment_remarks', '')
            
            # Update with recalculated wage amounts but preserve payments
            net_amount = Decimal(str(recalculated_data['net_amount']))
            remaining_amount = net_amount - paid_amount
            
            updated_data = {
                **recalculated_data,  # Use recalculated wage data
                'paid_amount': float(paid_amount),
                'remaining_amount': float(remaining_amount),
                'payment_status': payment_status,
                'payment_mode': payment_mode,
                'payment_reference': payment_reference,
                'last_payment_date': last_payment_date,
                'payment_remarks': payment_remarks
            }
            
            old_daily_wage = emp_data.get('daily_wage', 0)
            new_daily_wage = updated_data['daily_wage']
            
            print(f"Employee {employee.name}: daily_wage changed from {old_daily_wage} to {new_daily_wage}")
            
            updated_employee_wages.append(updated_data)
        
        # Update totals
        self.employee_wages = updated_employee_wages
        self.total_gross_amount = sum(Decimal(str(emp['gross_amount'])) for emp in updated_employee_wages)
        self.total_net_amount = sum(Decimal(str(emp['net_amount'])) for emp in updated_employee_wages)
        self.total_remaining_amount = sum(Decimal(str(emp['remaining_amount'])) for emp in updated_employee_wages)
        
        self.save()
        
        print(f"Wage record {self.id} successfully recalculated with historical rates")
        return self


class WagePaymentTransaction(models.Model):
    """
    Track individual payment transactions for wage payments
    """
    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('adjustment', 'Adjustment'),
    ]
    
    wage_payment = models.ForeignKey(
        WeeklyWagePayment,
        on_delete=models.CASCADE,
        related_name='payment_transactions'
    )
    employee_id = models.CharField(max_length=50,default=1)  # Store employee ID for this transaction
    employee_name = models.CharField(max_length=255, default="Unknown")  # Store name for easy reference
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        default='payment'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_mode = models.CharField(
        max_length=20,
        choices=WeeklyWagePayment.PAYMENT_MODE_CHOICES
    )
    reference_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    transaction_date = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xe_wage_payment_transactions'
        ordering = ['-transaction_date']
        verbose_name = 'Wage Payment Transaction'
        verbose_name_plural = 'Wage Payment Transactions'
    
    def __str__(self):
        return f"{self.employee_name} - {self.get_transaction_type_display()} ₹{self.amount}"


class AttendanceWeeklySummary(models.Model):
    """
    Weekly summary of attendance and wage calculations
    """
    week_start_date = models.DateField(
        unique=True,
        verbose_name="Week Start Date"
    )
    week_end_date = models.DateField(verbose_name="Week End Date")
    total_employees = models.IntegerField(
        default=0,
        verbose_name="Total Employees"
    )
    total_present_days = models.IntegerField(
        default=0,
        verbose_name="Total Present Days (Sum)"
    )
    total_half_days = models.IntegerField(
        default=0,
        verbose_name="Total Half Days (Sum)"
    )
    total_gross_wages = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total Gross Wages"
    )
    total_deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total Deductions"
    )
    total_net_wages = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total Net Wages"
    )
    total_paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total Paid Amount"
    )
    total_pending_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Total Pending Amount"
    )
    is_wages_paid = models.BooleanField(
        default=False,
        verbose_name="All Wages Paid"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_attendance_weekly_summary'
        ordering = ['-week_start_date']
        verbose_name = 'Weekly Attendance Summary'
        verbose_name_plural = 'Weekly Attendance Summaries'
    
    def __str__(self):
        return f"Week {self.week_start_date} Summary - ₹{self.total_net_wages}"
    
    @classmethod
    def generate_summary(cls, week_start_date):
        """
        Generate or update weekly summary for given week
        """
        week_end_date = week_start_date + timedelta(days=6)
        
        # Get or create summary
        summary, created = cls.objects.get_or_create(
            week_start_date=week_start_date,
            defaults={'week_end_date': week_end_date}
        )
        
        # Calculate totals from weekly wage payments
        wage_payments = WeeklyWagePayment.objects.filter(
            week_start_date=week_start_date
        )
        
        summary.total_employees = wage_payments.count()
        summary.total_present_days = sum(payment.total_present_days for payment in wage_payments)
        summary.total_half_days = sum(payment.total_half_days for payment in wage_payments)
        summary.total_gross_wages = sum(payment.gross_amount for payment in wage_payments)
        summary.total_deductions = sum(payment.total_deductions for payment in wage_payments)
        summary.total_net_wages = sum(payment.net_amount for payment in wage_payments)
        summary.total_paid_amount = sum(payment.paid_amount for payment in wage_payments)
        summary.total_pending_amount = summary.total_net_wages - summary.total_paid_amount
        summary.is_wages_paid = summary.total_pending_amount == Decimal('0.00')
        
        summary.save()
        return summary

class BulkWagePayment(models.Model):
    """Model for storing bulk wage payments (pay all employees at once)"""
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
        ('Cheque', 'Cheque'),
        ('Card', 'Card'),
    ]
    
    week_start_date = models.DateField()
    week_end_date = models.DateField()
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Store all employee payment details as JSON
    employee_payments = models.JSONField(default=list)  # Array of employee payment objects
    
    # Summary fields
    total_employees = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Payment details
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default='Cash')
    payment_reference = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    
    # Optional: Add expense tracking
    expense_category = models.CharField(max_length=50, default='Wages')
    
    # Audit fields
    paid_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bulk_wage_payments'
        unique_together = ['week_start_date', 'week_end_date']
    
    def __str__(self):
        return f"Bulk Payment - Week {self.week_start_date} to {self.week_end_date}"
    
    @classmethod
    def create_bulk_payment(cls, week_start_date, employee_data, payment_mode='Cash', 
                           payment_reference='', remarks='', paid_by=None):
        """
        Create a bulk wage payment record
        
        employee_data format:
        [
            {
                'employee_id': '1',
                'employee_name': 'John Doe',
                'present_days': 5,
                'half_days': 1,
                'absent_days': 1,
                'daily_wage': 500.00,
                'total_wages': 2750.00,
                'attendance_details': {...}  # Optional: detailed attendance
            },
            ...
        ]
        """
        from .utils import get_week_dates
        
        week_dates = get_week_dates(week_start_date)
        week_end_date = week_dates[-1]
        
        total_amount = sum(emp['total_wages'] for emp in employee_data)
        
        bulk_payment = cls.objects.create(
            week_start_date=week_start_date,
            week_end_date=week_end_date,
            employee_payments=employee_data,
            total_employees=len(employee_data),
            total_amount=total_amount,
            payment_mode=payment_mode,
            payment_reference=payment_reference,
            remarks=remarks,
            paid_by=paid_by
        )
        
        return bulk_payment

def get_wage_for_date(employee, target_date):
    """
    Get the wage rate that was effective for an employee on a specific date
    
    Args:
        employee: Employee instance
        target_date: date object for which wage is needed
    
    Returns:
        Wage instance or None if no wage was effective on that date
    """
    from .models import Wage
    
    # Find wages that were effective on the target date
    wages = Wage.objects.filter(
        employee=employee,
        effective_from__lte=target_date
    ).filter(
        # Either no end date (ongoing) or end date is after target date
        models.Q(effective_to__isnull=True) | models.Q(effective_to__gte=target_date)
    ).order_by('-effective_from')  # Get the most recent one if multiple
    
    return wages.first() if wages.exists() else None
    
    
# events for new website scrapping website through open api
class ScrapedEvent(models.Model):
    # Event identification
    event_id = models.CharField(max_length=255, unique=True)
    source_platform = models.CharField(max_length=100)
    source_url = models.URLField(max_length=500)
    
    # Basic info
    event_name = models.CharField(max_length=500)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    event_category = models.CharField(max_length=100, null=True, blank=True)
    event_format = models.CharField(max_length=50, null=True, blank=True)
    event_status = models.CharField(max_length=50, default='Scheduled')
    recurrence = models.CharField(max_length=50, null=True, blank=True)
    
    # Datetime fields
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    duration_iso = models.CharField(max_length=50, null=True, blank=True)
    registration_open = models.DateTimeField(null=True, blank=True)
    registration_close = models.DateTimeField(null=True, blank=True)
    submission_deadline = models.DateTimeField(null=True, blank=True)
    
    # Location
    venue_name = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    venue_capacity = models.IntegerField(null=True, blank=True)
    
    # Financial
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    
    # Arrays (use JSONField for SQLite, ArrayField for PostgreSQL)
    sponsors = models.JSONField(default=list, blank=True)
    partners = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Organiser
    organiser_name = models.CharField(max_length=300, null=True, blank=True)
    organiser_contact_email = models.EmailField(null=True, blank=True)
    organiser_contact_phone = models.CharField(max_length=50, null=True, blank=True)
    organiser_location_country = models.CharField(max_length=100, null=True, blank=True)
    
    # Additional info
    target_audience = models.TextField(null=True, blank=True)
    eligibility_criteria = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    agenda_link = models.URLField(max_length=500, null=True, blank=True)
    post_event_materials_link = models.URLField(max_length=500, null=True, blank=True)
    expected_attendance = models.IntegerField(null=True, blank=True)
    registration_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-start_datetime']
        indexes = [
            models.Index(fields=['start_datetime']),
            models.Index(fields=['city', 'country']),
            models.Index(fields=['event_category']),
        ]
        
#jobs
class Jobs(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name    
       
class JobAssignment(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    def __str__(self):
        return self.job.name

#Register 
class Role(models.Model):
    name = models.CharField(max_length = 100, unique=True)
    
    def __str__(self):
        return self.name
    
class Page(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
     
    def __str__(self): 
        return self.user.username
    
class AssignPage(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('role', 'page')
    
    def __str__(self):
        return {self.role.name}