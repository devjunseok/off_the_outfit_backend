from django.urls import path
from weather import views

urlpatterns = [

    path('', views.WeatherInfoView.as_view(), name='weather_view' ),           # 날씨 url

]
