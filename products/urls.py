from django.urls import path
from products import views

urlpatterns = [
    # brand
    path('brand/', views.BrandInfoView.as_view(), name='brand_view' ),                                                                                                # 브랜드 전체 조회, 개별 등록 url
    path('brand/update/', views.BrandInfoUpdateView.as_view(), name='brand_update' ),                                                                                 # 브랜드 정보 업데이트 url
    
    # category
    path('category/', views.CategoryInfoView.as_view(), name='category_view' ),                                                                                       # 카테고리 전체 조회, 개별 등록 url
    path('category/update/', views.CategoryInfoUpdateView.as_view(), name='category_update' ),                                                                        # 카테고리 정보 업데이트 url
    
    # product
    path('product/update/', views.ProductInfoUdateView.as_view(), name='product_update' ),                                                                            # 상품 정보 업데이트 url
    path('product/', views.ProductInfoView.as_view(), name='product_view' ),                                                                                          # 상품 정보 전체 조회, 개별 등록 url
    path('product/category/<int:category_id>/', views.ProductInfoCategoryView.as_view(), name='product_cateogry_view' ),                                              # 상품 정보 카테고리 별 조회
    path('product/brand/<int:brand_id>/', views.ProductInfoBrandView.as_view(), name='product_brand_view' ),                                                          # 상품 정보 브랜드 별 조회
    path('product/<int:product_number>/', views.ProductInfoDetailView.as_view(), name='product_detail_view'),                                                         # 상품 정보 상세 조회, 수정, 삭제 url
    path('product/<int:product_number>/board/', views.ProductPostView.as_view(), name='product_post_view'),                                                           # 상품 정보 게시글 전체 조회, 등록 url
    path('product/<int:product_number>/board/<int:post_id>/', views.ProductPostDetailView.as_view(), name='product_post_detail_view'),                                # 상품 정보 게시글 상세 조회, 수정, 삭제 url
    path('product/<int:product_number>/board/<int:post_id>/reply/', views.ProductPostReplyView.as_view(), name='product_post_reply_view'),                            # 상품 정보 게시글 댓글 전체 조회, 등록 url
    path('product/<int:product_number>/board/<int:post_id>/reply/<int:reply_id>/', views.ProductPostReplyDetailView.as_view(), name='product_post_reply_detail_view'),# 상품 정보 게시글 댓글 삭제 url
    path('product/<int:product_number>/closet/', views.ClosetView.as_view(), name='closet_view'),                                                                     # 상품 기준 옷장 조회, 등록 url
    path('product/<int:product_number>/closet/<int:closet_id>/', views.ClosetDetailView.as_view(), name='closet_detail_view'),                                        #상품 기준 옷장 상세보기 수정, 삭제 url
    path('search/', views.ProductsSearchView.as_view(), name='product_search_view'),                                                                                  # 상품 검색 url
    
    # closet
    path('product/closet/<int:user_id>/', views.UserClosetView.as_view(), name='user_closet_view'),                                                                   # 유저 기준 옷장 조회 url
    path('product/nametag/', views.NameTagView.as_view(), name='name_tag_view'),                                                                                      # 옷장 네임 태그 등록, 유저 옷장 태그 조회 url
    path('product/nametag/<int:nametag_id>/like/', views.NameTagLikeView.as_view(), name='name_tag_like_view'),                                                       # 옷장 네임 태그 좋아요 url
]
