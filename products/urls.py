from django.urls import path
from products import views

urlpatterns = [
    path('brand/update/', views.BrandInfoUpdate.as_view(), name ='brand_update' ),
    path('category/update/', views.CategoryListUpdate.as_view(), name ='category_update' ),
    path('update/', views.ProductsView.as_view(), name ='products_update' ),
]
