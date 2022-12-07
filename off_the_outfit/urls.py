from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('communities/', include('communities.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('recommend/', include('recommend.urls')),
    path('weather/', include('weather.urls')),
    path('manager/', include('manager.urls')),
    path('recommend/', include('recommend.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)