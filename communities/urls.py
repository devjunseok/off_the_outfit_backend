from django.urls import path
from communities import views

urlpatterns = [


    path('', views.ArticlesFeedView.as_view(), name ='feed_list' ), # 게시글 전체보기
    path('<int:feed_id>/comment/', views.FeedCommentView.as_view(), name = 'feed_comment_view'),   # 댓글 등록 url
    path('<int:feed_id>/comment/<int:comment_id>/', views.FeedCommentDetailView.as_view(), name = 'feed_comment_detail_view'), # 댓글 수정, 삭제 url
    path('<int:feed_id>/', views.ArticlesFeedDetailView.as_view(), name ='feed_detail_view' ),     # 게시글 상세조회, 수정, 삭제

]
