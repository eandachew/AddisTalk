"""
URL configuration for AddisTalk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    
    # Home page - keep this first
    path('', blog_views.PostList.as_view(), name='home'),
    
    # Specific paths before catch-all blog patterns
    path('about/', include('about.urls'), name='about-urls'),
    path('contact/', include('contact.urls'), name='contact-urls'),
    
    # Blog URLs - these come AFTER specific paths
    path('blog/', include('blog.urls')),  # Add 'blog/' prefix to avoid conflicts
    
    # Authentication URLs
    path('accounts/', include('allauth.urls')),
]