from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('portfolio.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
