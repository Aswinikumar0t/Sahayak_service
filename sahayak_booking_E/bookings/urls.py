
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_page, name='services'), 
    path('services/<str:service_key>/', views.service_subcategories, name='service_subcategories'), 
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),

    #booking urls
    path('book/', views.booking_page, name='booking_page'),  
    path('booking/confirmation/', views.booking_confirmation, name='booking_confirmation'),  
    path('my-bookings/', views.my_bookings, name='my_bookings'),  
    path('booking-detail/<str:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('profile/', views.profile_page, name='profile'), 
    path('api/cancel-booking/<str:booking_id>/', views.cancel_booking_api, name='cancel_booking_api'),

]