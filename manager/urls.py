from django.urls import path
from manager import views

urlpatterns = [

    path('reportfeed/', views.ReportFeedView.as_view(), name ='report_feed_list' ), # 신고게시글 열람
    path('reportfeed/<int:feed_id>/', views.ReportFeedDetailView.as_view(), name ='report_feed_detail'), # 관리자 페이지 기능
 
]

    



