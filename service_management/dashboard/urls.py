from django.urls import path
from . import views

urlpatterns = [
    # Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    
    # Services URLs
    path('services/', views.services, name='services'),
    path('subcategories/<int:category_id>/', views.subcategories, name='subcategories'),
    path('toggle-category/<int:pk>/', views.toggle_category, name='toggle_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('toggle-subcategory/<int:pk>/', views.toggle_subcategory, name='toggle_subcategory'),
    path('delete-subcategory/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
    
    # Rate Plans URLs
    path('rate_plans/', views.rate_plans, name='rate_plans'),
    path('rate_plans/toggle/<int:pk>/', views.toggle_plan, name='toggle_plan'),
    path('rate_plans/delete/<int:pk>/', views.delete_plan, name='delete_plan'),
    
    # Partners URLs
    path('service-partners/', views.service_partner_list, name='service_partner_list'),
    path('corporate-partners/', views.corporate_partners, name='corporate_partners'),
    path('solo-partners/', views.solo_partners, name='solo_partners'),
    path('service-partner-add/', views.service_partner_add, name='service_partner_add'),
    
    # Other URLs
    path('applications/', views.applications, name='applications'),
    path('bookings/', views.bookings, name='bookings'),
    path('reports/', views.reports, name='reports'),
    path('payments/', views.payments, name='payments'),
    path('access-control/', views.access_control, name='access_control'),
    path('booking-management/', views.booking_management, name='booking_management'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    
    # API URLs
    path('api/categories/', views.api_categories, name='api_categories'),
    path('api/subcategories/', views.api_subcategories, name='api_subcategories'),
    path('api/rate-plans/', views.api_rate_plans, name='api_rate_plans'),
]