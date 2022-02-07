from django.shortcuts import render, redirect
from django.views import View      # Custom
from django.views.generic import ListView
from django.views.generic import FormView # Creation ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView   # HTTP Verb
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet  # Action (CRUD)
from rest_framework.response import Response
from . import serializers

class HomePageView(ListView):
    template_name = 'core/video_list.html'
    queryset = Video.objects.all()
    paginate_by = 9  # ?page=10

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     ...


class VideUploadView(LoginRequiredMixin, FormView):
    """
    Process Upload of video from user side
    """
    form_class = VideoUploadForm
    template_name = 'core/video_upload_form.html'
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)  # Run clean & clean_ methods


class PlayVideoView(View):
    def get(self, request, uuid):
        v = get_object_or_404(Video, uuid=uuid)
        # v = Video.objects.get(uuid=uuid)
        return render(request, 'core/video_play.html', {'video': v})



class VideoListAPIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        videos = Video.objects.all()
        s = serializers.VideoSerializer(videos, many=True)
        return Response(s.data)

