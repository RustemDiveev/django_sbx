"""django_sbx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# include - позволяет ссылаться на другие конфигурации URL - нужно использовать всегда 
# если задано app_name, то достаточно просто заинклюдить без пути 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('django_tutorial/', include('django_tutorial.urls')),
    path('drf/', include('drf_tutorial.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('drf-nested-url/', include('drf_nested_url.urls')),
    path('transaction-management/', include('transaction_management.urls')),
]

# при добавлении представлений для логина и логаута - необходимо к URL добавлять login и logout 