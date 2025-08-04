from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.forms import ValidationError

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
    
class Attendance(models.Model):
    """Daily attendance record for all employees"""
    
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('overtime', 'Overtime'),
        ('leave', 'Leave'),
    ]
    
    date = models.DateField(verbose_name="Attendance Date")
    total_employees_present = models.PositiveIntegerField(default=0, verbose_name="Total Present")
    remarks = models.TextField(blank=True, null=True, verbose_name="Daily Remarks")
    is_processed = models.BooleanField(default=False, verbose_name="Wages Calculated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_attendance'
        ordering = ['-date']
        verbose_name = 'Daily Attendance'
        verbose_name_plural = 'Daily Attendances'
        unique_together = ['date']  # One record per date
    
    def __str__(self):
        return f"Attendance - {self.date} ({self.total_employees_present} present)"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total present employees
        if self.pk:  # If updating existing record
            self.total_employees_present = self.employee_attendances.filter(
                status__in=['present', 'half_day', 'overtime']
            ).count()
        super().save(*args, **kwargs)


class EmployeeAttendance(models.Model):
    """Individual employee attendance for each day"""
    
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('overtime', 'Overtime'),
        ('leave', 'Leave'),
    ]
    
    attendance = models.ForeignKey(
        Attendance, 
        on_delete=models.CASCADE, 
        related_name='employee_attendances'
    )
    employee = models.ForeignKey(
        'Employee',  # Reference to your existing Employee model
        on_delete=models.CASCADE, 
        related_name='daily_attendances'
    )
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES)
    hours_worked = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=8.00,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Hours Worked"
    )
    overtime_hours = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Overtime Hours"
    )
    daily_wage_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Daily Wage Earned"
    )
    overtime_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Overtime Amount"
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Total Amount Earned"
    )
    remarks = models.CharField(max_length=500, blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_employee_attendance'
        ordering = ['-attendance__date', 'employee__name']
        verbose_name = 'Employee Attendance'
        verbose_name_plural = 'Employee Attendances'
        unique_together = ['attendance', 'employee']  # One record per employee per day
    
    def __str__(self):
        return f"{self.employee.name} - {self.attendance.date} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Auto-calculate wage amounts based on current wage rate
        if not self.daily_wage_amount or self.daily_wage_amount == 0:
            current_wage = Wage.get_current_wage(self.employee)
            if current_wage:
                base_daily_rate = current_wage.amount
                
                # Calculate based on status
                if self.status == 'present':
                    self.daily_wage_amount = base_daily_rate
                elif self.status == 'half_day':
                    self.daily_wage_amount = base_daily_rate / 2
                elif self.status == 'overtime':
                    self.daily_wage_amount = base_daily_rate
                    # Overtime rate (1.5x for overtime hours)
                    self.overtime_amount = (base_daily_rate / 8) * self.overtime_hours * Decimal('1.5')
                elif self.status in ['absent', 'leave']:
                    self.daily_wage_amount = Decimal('0')
                    self.overtime_amount = Decimal('0')
        
        # Calculate total amount
        self.total_amount = self.daily_wage_amount + self.overtime_amount
        
        super().save(*args, **kwargs)


class EmployeeWageSummary(models.Model):
    """Monthly/Weekly wage summary for each employee"""
    
    PERIOD_TYPE_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom Period'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='wage_summaries'
    )
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPE_CHOICES, default='weekly')
    period_start = models.DateField(verbose_name="Period Start Date")
    period_end = models.DateField(verbose_name="Period End Date")
    
    # Attendance Summary
    total_days_present = models.PositiveIntegerField(default=0)
    total_days_absent = models.PositiveIntegerField(default=0)
    total_half_days = models.PositiveIntegerField(default=0)
    total_overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Financial Summary
    total_wage_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Total Wage Amount"
    )
    total_overtime_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Total Overtime Amount"
    )
    bonus_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Bonus Amount"
    )
    deduction_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Deductions"
    )
    gross_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Gross Amount"
    )
    net_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Net Payable Amount"
    )
    
    # Payment Tracking
    paid_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Amount Paid"
    )
    pending_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Pending Amount"
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Metadata
    is_processed = models.BooleanField(default=False, verbose_name="Summary Processed")
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_employee_wage_summary'
        ordering = ['-period_end', 'employee__name']
        verbose_name = 'Employee Wage Summary'
        verbose_name_plural = 'Employee Wage Summaries'
        unique_together = ['employee', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.employee.name} - {self.period_start} to {self.period_end} (₹{self.net_amount})"
    
    def save(self, *args, **kwargs):
        # Auto-calculate amounts
        self.gross_amount = self.total_wage_amount + self.total_overtime_amount + self.bonus_amount
        self.net_amount = self.gross_amount - self.deduction_amount
        self.pending_amount = self.net_amount - self.paid_amount
        
        # Update payment status based on amounts
        if self.paid_amount == 0:
            self.payment_status = 'pending'
        elif self.paid_amount >= self.net_amount:
            self.payment_status = 'paid'
            self.pending_amount = Decimal('0')
        else:
            self.payment_status = 'partial'
        
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.period_end < self.period_start:
            raise ValidationError('Period end date must be after start date.')
        
        if self.paid_amount > self.net_amount:
            raise ValidationError('Paid amount cannot exceed net amount.')


class WagePayment(models.Model):
    """Track individual wage payments"""
    
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('upi', 'UPI'),
        ('cheque', 'Cheque'),
        ('card', 'Card'),
    ]
    
    wage_summary = models.ForeignKey(
        EmployeeWageSummary,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payment_date = models.DateField(verbose_name="Payment Date")
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Payment Amount"
    )
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    reference_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Reference/Transaction ID")
    paid_by = models.CharField(max_length=255, verbose_name="Paid By")
    remarks = models.TextField(blank=True, null=True)
    receipt_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Receipt/Proof URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'xe_wage_payments'
        ordering = ['-payment_date', '-created_at']
        verbose_name = 'Wage Payment'
        verbose_name_plural = 'Wage Payments'
    
    def __str__(self):
        return f"Payment ₹{self.amount} to {self.wage_summary.employee.name} on {self.payment_date}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Update wage summary paid amount
        total_paid = self.wage_summary.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0')
        
        self.wage_summary.paid_amount = total_paid
        self.wage_summary.save()


# Helper function to create attendance records
def create_daily_attendance(attendance_date, employee_data):
    """
    Helper function to create daily attendance
    
    employee_data format:
    [
        {'employee_id': 1, 'status': 'present', 'hours_worked': 8, 'overtime_hours': 2},
        {'employee_id': 2, 'status': 'absent'},
        ...
    ]
    """
    from .models import Employee
    
    # Create or get attendance record for the date
    attendance, created = Attendance.objects.get_or_create(
        date=attendance_date,
        defaults={'total_employees_present': 0}
    )
    
    # Create employee attendance records
    for emp_data in employee_data:
        employee = Employee.objects.get(id=emp_data['employee_id'])
        
        emp_attendance, created = EmployeeAttendance.objects.get_or_create(
            attendance=attendance,
            employee=employee,
            defaults={
                'status': emp_data.get('status', 'absent'),
                'hours_worked': emp_data.get('hours_worked', 8.0),
                'overtime_hours': emp_data.get('overtime_hours', 0.0),
            }
        )
    
    # Update total present count
    attendance.save()
    
    return attendance


# Helper function to generate wage summary
def generate_wage_summary(employee, start_date, end_date, period_type='weekly'):
    """Generate wage summary for an employee for a given period"""
    
    attendances = EmployeeAttendance.objects.filter(
        employee=employee,
        attendance__date__range=[start_date, end_date]
    )
    
    # Calculate totals
    total_present = attendances.filter(status='present').count()
    total_absent = attendances.filter(status='absent').count()
    total_half_days = attendances.filter(status='half_day').count()
    total_overtime_hours = attendances.aggregate(
        total=models.Sum('overtime_hours')
    )['total'] or Decimal('0')
    
    total_wage = attendances.aggregate(
        total=models.Sum('daily_wage_amount')
    )['total'] or Decimal('0')
    
    total_overtime = attendances.aggregate(
        total=models.Sum('overtime_amount')
    )['total'] or Decimal('0')
    
    # Create or update wage summary
    summary, created = EmployeeWageSummary.objects.get_or_create(
        employee=employee,
        period_start=start_date,
        period_end=end_date,
        defaults={
            'period_type': period_type,
            'total_days_present': total_present,
            'total_days_absent': total_absent,
            'total_half_days': total_half_days,
            'total_overtime_hours': total_overtime_hours,
            'total_wage_amount': total_wage,
            'total_overtime_amount': total_overtime,
            'is_processed': True,
        }
    )
    
    return summary