from django.urls import path
from communities import views

urlpatterns = [
    path('', views.ArticlesFeedView.as_view(), name ='feed_list' ),                          # 게시글 전체보기, 등록
    path('<int:feed_id>/', views.ArticlesFeedDetailView.as_view(), name ='feed_detail_view' ),  # 게시글 상세조회, 수정, 삭제    
    path('search/', views.CommunitySearchView.as_view(), name = 'communities_search_view'),  # 게시글 검색    
]
