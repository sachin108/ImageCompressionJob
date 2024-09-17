from django.urls import path
from . import views

urlpatterns = [
 
    path('upload/', views.upload_csv, name='upload_csv'),
    path('products/', views.product_list, name='product_list'),
    path('status/<uuid:task_id>/', views.check_status, name='check_status'),
]

