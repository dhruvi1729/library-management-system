"""
URL configuration for library_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from library.views import home  # Import the homepage view

urlpatterns = [
    path('', home, name='home'),  # This handles the root URL: http://127.0.0.1:8000/
    path('admin/', admin.site.urls),
    
    # Include your app URLs for both regular routes and API routes
    path('api/', include('library.urls')),  # API routes under /api/
    path('', include('library.urls')),  # Non-API routes under root (i.e., /delete-book/)
]

