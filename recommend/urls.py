from django.urls import path
from . import views

urlpatterns = [
    path('refresh/', views.ProductRecommendView.as_view(), name='recommend'),
    
]
