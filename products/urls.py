from django.urls import path
from products import views

urlpatterns = [
    path('brand/', views.BrandInfoView.as_view(), name ='brand_view' ),                                            # 브랜드 전체 조회, 개별 등록 url
    path('brand/update/', views.BrandInfoUpdateView.as_view(), name ='brand_update' ),                             # 브랜드 정보 업데이트 url
    path('category/', views.CategoryInfoView.as_view(), name ='category_view' ),                                   # 카테고리 전체 조회, 개별 등록 url
    path('category/update/', views.CategoryInfoUpdateView.as_view(), name ='category_update' ),                    # 카테고리 정보 업데이트 url
    path('product/update/', views.ProductInfoUdateView.as_view(), name ='product_update' ),                        # 상품 정보 업데이트 url
    path('product/', views.ProductInfoView.as_view(), name = 'product_view' ),                                     # 상품 정보 전체 조회, 개별 등록 url
    path('product/<int:product_number>/', views.ProductInfoDetailView.as_view(), name= 'product_detail_view'),     # 상품 정보 상세 조회, 수정, 삭제 url
    path('product/<int:product_number>/review/', views.ProductReviewBoardView.as_view(), name= 'product_review_view'), # 상품 리뷰 전체 조회, 등록 url
    path('product/<int:product_number>/review/<int:review_id>/', views.ProductReviewDetailView.as_view(), name= 'product_review_detail_view'), # 상품 리뷰 상세 조회, 수정, 삭제 url
    path('product/<int:product_number>/review/<int:review_id>/reply/', views.ProductReviewReplyView.as_view(), name= 'product_review_reply_view'), # 상품 리뷰 댓글 전체 조회, 등록 url
    path('product/<int:product_number>/review/<int:review_id>/reply/<int:reply_id>/', views.ProductReviewReplyDetailView.as_view(), name= 'product_review_reply_detail_view'), # 상품 리뷰 댓글 삭제 url
    
]
