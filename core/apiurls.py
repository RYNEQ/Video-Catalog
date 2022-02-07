from django.urls import path
from . import views

app_name = 'coreapi'

urlpatterns = [
    path('videos', views.VideoListAPIView.as_view(), name='api_video_list'),
]