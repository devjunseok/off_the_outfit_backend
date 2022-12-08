from django.urls import path

from recommend import views

urlpatterns = [
    path('closet/user/', views.ClosetUserRecommend.as_view(), name='closet_user_recommend_view' ),           # 옷장 기반 유저 추천 url
    path('closet/product/', views.ClosetProductRecommend.as_view(), name='closet_product_recommend_view' ),  # 옷장 기반 상품 추천 url
    path('refresh/', views.ProductRecommendView.as_view(), name='recommend'), # 날씨 기반 상품 추천 url
]

