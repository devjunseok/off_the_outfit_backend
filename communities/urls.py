from django.urls import path
from communities import views

urlpatterns = [

    path('', views.ArticlesFeedView.as_view(), name ='feed_list' ), # 게시글 전체보기
    path('reportfeed/', views.ReportFeedView.as_view(), name ='report_feed_list' ), # 신고게시글 열람
    path('reportfeed/<int:feed_id>/', views.ReportFeedDetailView.as_view(), name ='report_feed_detail'), # 관리자 페이지 기능
    path('report/<int:feed_id>/', views.ReportView.as_view(), name='report_view'), # 버튼 클릭 포인트 획득   
    path('search/', views.CommunitySearchView.as_view(), name = 'communities_search_view'),  # 게시글 검색   
    path('<int:feed_id>/', views.ArticlesFeedDetailView.as_view(), name ='feed_detail_view' ),  # 게시글 상세조회, 수정, 삭제 
    path('<int:feed_id>/comment/', views.FeedCommentView.as_view(), name = 'feed_comment'),   # 댓글 등록 url
    path('<int:feed_id>/comment/<int:comment_id>/', views.FeedCommentDetailView.as_view(), name = 'feed_comment_detail_view'), # 댓글 수정, 삭제 url
    path('<int:feed_id>/like/', views.CommunitiesFeedLikeView.as_view(), name = 'feed_like_view'),    # 게시글 좋아요 url
    path('<int:feed_id>/unlike/', views.CommunitiesFeedUnlikeView.as_view(), name = 'feed_unlike_view'),    # 게시글 싫어요 url
    path('<int:feed_id>/comment/<int:comment_id>/like/', views.CommentLike.as_view(), name = 'comment_like_view'),    # 댓글 좋아요 url
    path('<int:feed_id>/comment/<int:comment_id>/recomment/', views.ReCommentUpload.as_view(), name = 'recomment_upload'),   #대댓글 등록 url
    path('<int:feed_id>/comment/<int:comment_id>/recomment/<int:recomment_id>/', views.ReCommentDetailView.as_view(), name = 'recomment_view'),   #대댓글 삭제 url
    path('<int:feed_id>/comment/<int:comment_id>/recomment/<int:recomment_id>/like/', views.ReCommentLike.as_view(), name = 'recomment_like_view')   #대댓글 좋아요 url 
    

]

    



