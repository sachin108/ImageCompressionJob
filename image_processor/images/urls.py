from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('status/<str:request_id>/', views.check_status, name='check_status'),
    path('products/', views.product_list, name='product_list'),
]

