from django.contrib import admin
from django.urls import path, include
from images.views import home

urlpatterns = [
       path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('images/', include('images.urls')), 
]
