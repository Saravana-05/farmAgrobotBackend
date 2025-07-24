
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from xe_farm.views.employee.emp_views import (save_employee_data,get_employee_list, get_employee_detail,  edit_employee_data, delete_employee, restore_employee)
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

urlpatterns = [
    path('api/employees/', save_employee_data, name='save_employee_data'),

    # Employee GET endpoints
    path('api/employees', get_employee_list, name='get_employee_list'),
    path('api/employees/<int:employee_id>/', get_employee_detail, name='get_employee_detail'),
    path('api/employees/<int:employee_id>/edit', edit_employee_data, name='edit_employee'),

    # Employee Delete APIs
    path('api/employees/<int:employee_id>/delete', delete_employee, name='delete_employee'),
    path('api/employees/<int:employee_id>/restore',restore_employee, name='restore_employee'),

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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)