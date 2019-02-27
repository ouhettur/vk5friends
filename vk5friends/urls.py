from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    url(r'', include('app.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
