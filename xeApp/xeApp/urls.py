
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from xe_farm.views.employee.emp_views import (save_employee_data,get_employee_list, get_employee_detail,  edit_employee_data, delete_employee, restore_employee, change_employee_status, toggle_employee_status)
from xe_farm.views.merchant.merchant_views import (save_merchant_data, get_all_merchants, get_merchant_by_id, update_merchant_data, delete_merchant)
from xe_farm.views.farm_segment.farm_segment_views import (save_farm_segment_data, get_all_farm_segments, get_farm_segment_by_id, update_farm_segment_data, delete_farm_segment)
from xe_farm.views.crops.crop_views import (save_crop_data, get_all_crops, get_crop_by_id, update_crop_data, delete_crop)
from xe_farm.views.crop_variant.crop_variant_views import (get_all_crop_variants, save_crop_variant, get_crop_variant_by_id, update_crop_variant, delete_crop_variant, get_crop_variants_by_crop)
from xe_farm.views.yield_data.yield_views import (get_all_yields, save_yield_data, get_yield_by_id, update_yield_data, delete_yield, get_yield_summary)
from xe_farm.views.sales.sale_view import (save_sale_data, get_all_sales, get_sale_by_id, update_sale_data, delete_sale, update_sale_status, get_sales_by_merchant, get_sale_summary, get_sales_analytics)
from xe_farm.views.jobs.job_view import (
    create_job, get_all_jobs, get_job_by_id, update_job, delete_job,
)
from xe_farm.views.expense.expense_view import (save_expense_data, get_expense_list, get_expense_detail, edit_expense_data, delete_expense, get_expense_statistics
)   
from xe_farm.views.wages.wages_view import (save_wage_data, get_wage_list, get_wage_detail, edit_wage_data, delete_wage, get_employee_wages, end_current_wage, get_wage_statistics)
from xe_farm.views.attendance.attendance_view import (
    check_attendance_exists, create_daily_attendance, create_wage_payment, delete_attendance, get_attendance_dashboard, get_attendance_list, get_attendance_detail, get_employee_attendance_history, get_monthly_attendance_report, get_wage_payments, get_wage_summary_detail, mark_attendance_processed,
    update_employee_attendance, generate_wage_summary, get_wage_summaries,
    bulk_update_attendance, export_attendance_report
)
urlpatterns = [
    path('api/employees/', save_employee_data, name='save_employee_data'),

    # Employee GET endpoints
    path('api/employees', get_employee_list, name='get_employee_list'),
    path('api/employees/<int:employee_id>/', get_employee_detail, name='get_employee_detail'),
    path('api/employees/<int:employee_id>/edit', edit_employee_data, name='edit_employee'),

    # Employee Delete APIs
    path('api/employees/<int:employee_id>/delete', delete_employee, name='delete_employee'),
    path('api/employees/<int:employee_id>/restore',restore_employee, name='restore_employee'),
    path('api/employees/<int:employee_id>/status', change_employee_status, name='change_employee_status'),
    path('api/employees/<int:employee_id>/toggle-status', toggle_employee_status, name='toggle_employee_status'),


    #Merchant URLs
    path('api/merchants/', save_merchant_data, name='save_merchant'),
    path('api/merchants/all/', get_all_merchants, name='get_all_merchants'),
    path('api/merchants/<str:merchant_id>/', get_merchant_by_id, name='get_merchant_by_id'),
    path('api/merchants/<str:merchant_id>/update/', update_merchant_data, name='update_merchant'),
    path('api/merchants/<str:merchant_id>/delete/', delete_merchant, name='delete_merchant'),

    # Farm Segment URLs
    path('api/farm-segments/', save_farm_segment_data, name='save_farm_segment'),
    path('api/farm-segments/all/', get_all_farm_segments, name='get_all_farm_segments'),
    path('api/farm-segments/<str:farm_id>/',get_farm_segment_by_id, name='get_farm_segment_by_id'),
    path('api/farm-segments/<str:farm_id>/update/', update_farm_segment_data, name='update_farm_segment'),
    path('api/farm-segments/<str:farm_id>/delete/', delete_farm_segment, name='delete_farm_segment'),

    # Crop URLs
    path('api/crops/', save_crop_data, name='save_crop'),
    path('api/crops/all/', get_all_crops, name='get_all_crops'),
    path('api/crops/<str:crop_id>/', get_crop_by_id, name='get_crop_by_id'),
    path('api/crops/<str:crop_id>/update/', update_crop_data, name='update_crop'),
    path('api/crops/<str:crop_id>/delete/', delete_crop, name='delete_crop'),

    # Crop Variant URLs
    path('api/crop-variants/', get_all_crop_variants, name='get_all_crop_variants'),
    path('api/crop-variants/create/', save_crop_variant, name='save_crop_variant'),
    path('api/crop-variants/<int:variant_id>/', get_crop_variant_by_id, name='get_crop_variant_by_id'),
    path('api/crop-variants/<int:variant_id>/update/', update_crop_variant, name='update_crop_variant'),
    path('api/crop-variants/<int:variant_id>/delete/', delete_crop_variant, name='delete_crop_variant'),
    path('api/crops/<str:crop_id>/variants/', get_crop_variants_by_crop, name='get_crop_variants_by_crop'),

    # Yield URLs
    path('api/yields/', get_all_yields, name='get_all_yields'),
    path('api/yields/create/', save_yield_data, name='save_yield_data'),
    path('api/yields/<int:yield_id>/', get_yield_by_id, name='get_yield_by_id'),
    path('api/yields/<int:yield_id>/update/', update_yield_data, name='update_yield_data'),
    path('api/yields/<int:yield_id>/delete/', delete_yield, name='delete_yield'),
    path('api/yields/summary/', get_yield_summary, name='get_yield_summary'),

    # Sale URLs
    path('api/sales/', save_sale_data, name='save_sale'),
    path('api/sales/all/', get_all_sales, name='get_all_sales'),
    path('api/sales/<int:sale_id>/', get_sale_by_id, name='get_sale_by_id'),
    path('api/sales/<int:sale_id>/update/', update_sale_data, name='update_sale'),
    path('api/sales/<int:sale_id>/delete/', delete_sale, name='delete_sale'),
    path('api/sales/<int:sale_id>/status/', update_sale_status, name='update_sale_status'),
    path('api/sales/merchant/<int:merchant_id>/', get_sales_by_merchant, name='get_sales_by_merchant'),
    path('api/sales/summary/', get_sale_summary, name='get_sale_summary'),
    path('api/sales/analytics/', get_sales_analytics, name='get_sales_analytics'),

    # Job URLs
    path('api/jobs/', create_job, name='create_job'),
    path('api/jobs/all/', get_all_jobs, name='get_all_jobs'),
    path('api/jobs/<int:job_id>/', get_job_by_id, name='get_job_by_id'),
    path('api/jobs/<int:job_id>/update/', update_job, name='update_job'),
    path('api/jobs/<int:job_id>/delete/', delete_job, name='delete_job'),

     # Expense URLs
    path('api/expenses/', save_expense_data, name='save_expense'),
    path('api/expenses/all/', get_expense_list, name='get_all_expenses'),
    path('api/expenses/<int:expense_id>/', get_expense_detail, name='get_expense_by_id'),
    path('api/expenses/<int:expense_id>/update/', edit_expense_data, name='update_expense'),
    path('api/expenses/<int:expense_id>/delete/', delete_expense, name='delete_expense'),
    path('api/expenses/statistics/', get_expense_statistics, name='get_expense_statistics'),

    # Wage CRUD Operations
    path('api/wages/', save_wage_data, name='save_wage_data'),  # POST - Create wage
    path('api/wages/list/', get_wage_list, name='get_wage_list'),  # GET - List wages with filters
    path('api/wages/<int:wage_id>/', get_wage_detail, name='get_wage_detail'),  # GET - Get wage details
    path('api/wages/<int:wage_id>/update/', edit_wage_data, name='edit_wage_data'),  # PUT - Update wage
    path('api/wages/<int:wage_id>/delete/', delete_wage, name='delete_wage'),  # DELETE - Delete wage
    
    # Employee Wages
    path('api/employees/<int:employee_id>/wages/', get_employee_wages, name='get_employee_wages'),  # GET - Get all wages for employee
    
    # Wage Management
    path('api/wages/<int:wage_id>/end/', end_current_wage, name='end_current_wage'),  # POST - End current wage
    
    # Statistics
    path('api/wages/statistics/', get_wage_statistics, name='get_wage_statistics'),  # GET - Wage statistics

    # Daily Attendance
    path('api/attendance/create/', create_daily_attendance, name='create_daily_attendance'),
    path('api/attendance/list/', get_attendance_list, name='get_attendance_list'),
    path('api/attendance/<int:attendance_id>/', get_attendance_detail, name='get_attendance_detail'),
    path('api/attendance/<int:attendance_id>/delete/', delete_attendance, name='delete_attendance'),
    path('api/attendance/<int:attendance_id>/mark-processed/', mark_attendance_processed, name='mark_attendance_processed'),
    path('api/attendance/check-exists/', check_attendance_exists, name='check_attendance_exists'),
    
    # Employee Attendance
    path('api/attendance/employee/<int:attendance_id>/update/', update_employee_attendance, name='update_employee_attendance'),
    path('api/attendance/bulk-update/', bulk_update_attendance, name='bulk_update_attendance'),
    path('api/employee/<int:employee_id>/attendance-history/', get_employee_attendance_history, name='get_employee_attendance_history'),
    
    # ============= WAGE MANAGEMENT =============
    
    # Wage Summaries
    path('api/wages/summaries/generate/', generate_wage_summary, name='generate_wage_summary'),
    path('api/wages/summaries/list/', get_wage_summaries, name='get_wage_summaries'),
    path('api/wages/summaries/<int:summary_id>/', get_wage_summary_detail, name='get_wage_summary_detail'),
    
    # Wage Payments
    path('api/wages/payments/create/', create_wage_payment, name='create_wage_payment'),
    path('api/wages/payments/list/', get_wage_payments, name='get_wage_payments'),
    
    # ============= REPORTS & ANALYTICS =============
    
    # Dashboard
    path('api/dashboard/attendance/', get_attendance_dashboard, name='get_attendance_dashboard'),
    
    # Reports
    path('api/reports/monthly-attendance/', get_monthly_attendance_report, name='get_monthly_attendance_report'),
    path('api/reports/attendance/export/', export_attendance_report, name='export_attendance_report'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)