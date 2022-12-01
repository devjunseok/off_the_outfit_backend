from django.urls import path
from products import views

urlpatterns = [
    path('', views.Products.as_view(), name ='Products' ),
]
