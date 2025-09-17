"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
import os

def serve_manifest(request):
    """Serve the PWA manifest with correct content type"""
    manifest_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'manifest.json')
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='application/manifest+json')
    except FileNotFoundError:
        return HttpResponse('{}', content_type='application/manifest+json', status=404)

def serve_sw(request):
    """Serve the service worker with correct content type"""
    sw_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'sw.js')
    try:
        with open(sw_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse('// Service worker not found', content_type='application/javascript', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path("user/", include("userauths.urls")),
    path("useradmin/", include("useradmin.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    
    # PWA files
    path('manifest.json', serve_manifest, name='manifest'),
    path('sw.js', serve_sw, name='sw'),
    path('offline.html', TemplateView.as_view(template_name='core/offline.html'), name='offline-static'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
