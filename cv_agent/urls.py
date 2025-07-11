from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_cv_view, name='create_cv'),
    path('status/<str:task_id>/', views.get_cv_task_status, name='cv_task_status'),
] 
