from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path('api/communities/', include('communities.urls')),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/recommend/', include('recommend.urls')),
    path('api/weather/', include('weather.urls')),
    path('api/manager/', include('manager.urls')),
    path('api/recommend/', include('recommend.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
