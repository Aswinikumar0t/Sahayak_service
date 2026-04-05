
from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login_view, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/profile/', views.get_profile, name='profile'),

    path('api/profile/update/', views.update_profile, name='update_profile'),    
]