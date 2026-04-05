from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

        # ✅ User management moved here from dashboard
    path('users/', views.manage_users, name='manage_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:id>/', views.delete_user, name='delete_user'),
]