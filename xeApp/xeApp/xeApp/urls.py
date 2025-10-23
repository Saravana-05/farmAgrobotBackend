
import profile
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from xe_farm.views.attendance.attendance_view import employee_report, employee_summary_report, single_employee_report, wage_payment_details, wage_payment_history, export_attendance, get_active_employees, get_attendance, mark_attendance, pay_wages, update_attendance, update_single_attendance, validate_employees_for_attendance, wage_summary, weekly_data, weekly_wages_report
from xe_farm.views.attendance.pdf_wage_report_view import download_employee_wage_detail_pdf, download_payroll_summary_pdf, download_weekly_wage_summary_pdf, generate_wage_range_pdf, generate_weekly_wage_pdf
from xe_farm.views.employee.emp_views import (save_employee_data,get_employee_list, get_employee_detail,  edit_employee_data, delete_employee, restore_employee, change_employee_status, toggle_employee_status)
from xe_farm.views.merchant.merchant_views import (save_merchant_data, get_all_merchants, get_merchant_by_id, update_merchant_data, delete_merchant)
from xe_farm.views.farm_segment.farm_segment_views import (save_farm_segment_data, get_all_farm_segments, get_farm_segment_by_id, search_farm_segments, update_farm_segment_data, delete_farm_segment)
from xe_farm.views.crops.crop_views import (save_crop_data, get_all_crops, get_crop_by_id, update_crop_data, delete_crop)
from xe_farm.views.crop_variant.crop_variant_views import (get_all_crop_variants,  save_crop_variant, get_crop_variant_by_id, update_crop_variant, delete_crop_variant, get_crop_variants_by_crop)
from xe_farm.views.yield_data.yield_views import (add_bill_image, get_crop_comparison_dashboard, get_crop_dashboard, get_crop_performance_metrics,update_yield_with_image_options, get_all_yields, get_bill_images, remove_bill_image, replace_bill_images, save_yield_data, get_yield_by_id, update_yield_data, delete_yield, get_yield_summary)
from xe_farm.views.sales.sale_view import (add_payment, add_sale_images, advanced_sales_search, delete_sale_image, generate_bulk_pdf_report, generate_excel_report, generate_pdf_bill, get_available_yields, get_dashboard_revenue, get_payment_history, get_payment_modes, get_quick_stats, get_revenue_by_period, get_sale_images, get_yield_variants, save_sale_data, get_all_sales, get_sale_by_id, search_suggestions, update_sale_data, delete_sale, update_sale_image, update_sale_status, get_sales_by_merchant, get_sale_summary, get_sales_analytics)
from xe_farm.views.jobs.job_view import (
    create_job, get_all_jobs, get_job_by_id, update_job, delete_job,
)
from xe_farm.views.expense.expense_view import (get_expense_comparison_stats, get_expense_dashboard_stats, get_expense_summary_by_period, get_monthly_trend_data, save_expense_data, get_expense_list, get_expense_detail, edit_expense_data, delete_expense, get_expense_statistics
)   
from xe_farm.views.wages.wages_view import ( save_wage_data, get_wage_list, get_wage_detail, edit_wage_data, delete_wage, get_employee_wages, end_current_wage, get_wage_statistics)

urlpatterns = [
    # Employee GET endpoints
    path('api/employees/', save_employee_data, name='save_employee_data'),
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
    path('api/farm-segments/search/', search_farm_segments, name='search_farm_segments'),
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
    path('api/yields/update/<int:yield_id>/', update_yield_data, name='update_yield_data'),
    path('api/yields/delete/<int:yield_id>/', delete_yield, name='delete_yield'),
    path('api/yields/summary/', get_yield_summary, name='get_yield_summary'),
    path('api/yields/add-bill-image/<int:yield_id>/', add_bill_image, name='add-bill-image'),
    path('api/yields/update-with-options/<int:yield_id>/', update_yield_with_image_options, name='update_yield_with_options'),
    # Bill image management
    path('api/yields/<int:yield_id>/images/', get_bill_images, name='get_bill_images'),  # GET - Get all images for yield
    path('api/yields/<int:yield_id>/images/replace/', replace_bill_images, name='replace_bill_images'),  # POST - Replace all images
    path('api/yields/<int:yield_id>/images/<int:image_id>/delete/', remove_bill_image, name='remove_bill_image'),  # DELETE - Remove specific image
    path('api/crop-dashboard/', get_crop_dashboard, name='crop_dashboard'),
    path('api/crop-comparison-dashboard/', get_crop_comparison_dashboard, name='crop_comparison_dashboard'),
    path('api/crop-performance-metrics/', get_crop_performance_metrics, name='crop_performance_metrics'),
    
    

    # Sale URLs
    path('api/sales/', save_sale_data, name='save_sale_data'),
    path('api/sales/all/', get_all_sales, name='get_all_sales'),
    path('api/sales/<int:sale_id>/', get_sale_by_id, name='get_sale_by_id'),
    path('api/sales/<int:sale_id>/update/', update_sale_data, name='update_sale_data'),
    path('api/sales/delete/<int:sale_id>/', delete_sale, name='delete_sale'),
    path('api/sales/<int:sale_id>/status/', update_sale_status, name='update_sale_status'),
    path('api/sales/merchant/<int:merchant_id>/', get_sales_by_merchant, name='get_sales_by_merchant'),
    path('api/sales/summary/', get_sale_summary, name='get_sale_summary'),
    path('api/sales/analytics/', get_sales_analytics, name='get_sales_analytics'),
    
    # NEW: Payment management endpoints
    path('api/sales/<int:sale_id>/payment/add/', add_payment, name='add_payment'),
    path('api/sales/<int:sale_id>/payment/history/', get_payment_history, name='get_payment_history'),
    path('api/payment-modes/', get_payment_modes, name='get_payment_modes'),
    
    # NEW: Image management endpoints
    path('api/sales/<int:sale_id>/images/', get_sale_images, name='get_sale_images'),
    path('api/sales/<int:sale_id>/images/add/', add_sale_images, name='add_sale_images'),
    path('api/sales/<int:sale_id>/images/<int:image_id>/update/', update_sale_image, name='update_sale_image'),
    path('api/sales/<int:sale_id>/images/<int:image_id>/delete/', delete_sale_image, name='delete_sale_image'),
    path('api/dashboard/revenue/', get_dashboard_revenue, name='dashboard-revenue'),
    path('api/dashboard/quick-stats/', get_quick_stats, name='quick-stats'),
    path('api/dashboard/revenue/<str:period_type>/', get_revenue_by_period, name='get_revenue_by_period'),
    
    # NEW: Utility endpoints
    path('api/yields/available/', get_available_yields, name='get_available_yields'),
    path('api/yields/<int:yield_id>/variants/', get_yield_variants, name='get_yield_variants'),
    path('api/search/', advanced_sales_search, name='advanced_sales_search'),
    path('api/search/suggestions/', search_suggestions, name='search_suggestions'),
    
    # NEW: Report generation
    path('api/reports/excel/', generate_excel_report, name='generate_excel_report'),
    path('api/reports/pdf/<int:sale_id>/', generate_pdf_bill, name='generate_pdf_bill'),
    path('api/reports/bulk-pdf/', generate_bulk_pdf_report, name='generate_bulk_pdf_report'),

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
    path('api/dashboard/stats/', get_expense_dashboard_stats, name='get_expense_dashboard_stats'),
    path('api/dashboard/monthly-trend/', get_monthly_trend_data, name='get_monthly_trend_data'),
    path('api/dashboard/comparison/', get_expense_comparison_stats, name='get_expense_comparison_stats'),
    path('api/dashboard/summary/<str:period_type>/',get_expense_summary_by_period, name='get_expense_summary_by_period'),

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
    
    # Attendance Management
    path('api/weekly-data/', weekly_data, name='weekly-data'),
    path('api/mark-attendance/', mark_attendance, name='mark-attendance'),
    path('api/attendance/<str:date_str>/', get_attendance, name='get-attendance'),
    path('api/attendance/<str:date_str>/update/', update_attendance, name='update-attendance'),
    path('api/update-single-attendance/', update_single_attendance, name='update-single-attendance'),
    path('api/get-active-employees/', get_active_employees, name='get_active_employees'),
    path('validate-employees/', validate_employees_for_attendance, name='validate_employees'),
    # Wage Management
    path('api/pay-wages/', pay_wages, name='pay-wages'),
    path('api/wage-summary/',wage_summary, name='wage-summary'),
    
    # Export
    path('api/export-attendance/', export_attendance, name='export-attendance'),

    
    # bulk payment system
    path('bulk-payment-history/', wage_payment_history, name='wage_payment_history'),
    path('bulk-payment-details/<int:payment_id>/', wage_payment_details, name='wage_payment_details'),

    # PDF wage reports
    path('api/wages/pdf/weekly/',generate_weekly_wage_pdf, name='weekly_wage_pdf'),
    path('api/wages/pdf/range/', generate_wage_range_pdf, name='wage_range_pdf'),
    path('api/wages/pdf/summary/', download_weekly_wage_summary_pdf, name='wage_summary_pdf'),
    path('api/wages/pdf/employee-detail/', download_employee_wage_detail_pdf, name='employee_wage_detail_pdf'),
    # path('api/attendance/pdf/register/', download_attendance_register_pdf, name='attendance_register_pdf'),
    path('api/payroll/pdf/summary/', download_payroll_summary_pdf, name='payroll_summary_pdf'),

    # Reports and Analytics
    path('api/employee-report/', employee_report, name='employee-report'),
    path('api/employee/<int:employee_id>/report/', single_employee_report, name='single_employee_report'),
    path('api/employee-summary-report/', employee_summary_report, name='employee-summary-report'),
    path('api/weekly-wages-report/', weekly_wages_report, name='weekly-wages-report'),
    path('api/export-attendance/', export_attendance, name='export-attendance'),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)