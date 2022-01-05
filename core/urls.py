from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('upload_video', views.VideUploadView.as_view(), name='video_upload')
]