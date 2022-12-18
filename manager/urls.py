from django.urls import path
from manager import views

urlpatterns = [

    path('reportfeed/', views.ReportFeedView.as_view(), name ='report_feed_view' ),                    #신고게시글 열람
    path('feedmanage/<int:feed_id>/', views.FeedManageView.as_view(), name ='feed_manage_view'),       # 게시글 관리 기능
    path('usermanage/', views.UserManageView.as_view(), name ='user_manage_view'),                     # 관리자 유저 목록 열람 기능
    path('usermanage/<int:user_id>/', views.UserManageDetailView.as_view(), name ='user_manage_view'), # 관리자 유저 관리 기능
    path('userdelete/', views.UserDeleteView.as_view(), name='user_delete_view')                       # 휴면 유저 삭제 기능
 
 
]

    



