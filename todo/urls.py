from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Task CRUD
    path('task/add/', views.add_task, name='add_task'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('task/pin/<int:task_id>/', views.toggle_pin, name='toggle_pin'),

    # Categories
    path('category/add/', views.add_category, name='add_category'),
    path('category/delete/<int:cat_id>/', views.delete_category, name='delete_category'),

    # API
    path('api/task/<int:task_id>/status/', views.api_task_status, name='api_task_status'),
]