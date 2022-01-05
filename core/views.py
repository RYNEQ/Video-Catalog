from django.shortcuts import render, redirect
from django.views import View      # Custom
from django.views.generic import ListView
from django.views.generic import FormView # Creation ModelForm
from .forms import *
from .models import *
from pymediainfo import MediaInfo


class HomePageView(ListView):
    template_name = 'core/video_list.html'
    queryset = Video.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     ...

class VideUploadView(FormView):
    form_class = VideoUploadForm
    template_name = 'core/video_upload_form.html'
    success_url = '/'

    def form_valid(self, form):
        duration = None
        video: Video = form.save(commit=False)
        # Block Background Task
        media = MediaInfo.parse(video.file.path)
        for t in media.tracks:
            if t.track_type == "Video":
                duration = t.duration
                break
        video.duration = duration
        video.save()
        return super().form_valid(form)
