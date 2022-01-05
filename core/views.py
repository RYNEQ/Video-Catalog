from django.shortcuts import render, redirect
from django.views import View      # Custom
from django.views.generic import ListView
from django.views.generic import FormView # Creation ModelForm
from .forms import *
from .models import *
from pymediainfo import MediaInfo
import ffmpeg
import os
from django.conf import settings

class HomePageView(ListView):
    template_name = 'core/video_list.html'
    queryset = Video.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     ...

def generate_thumbnail(in_filename, out_filename):
    probe = ffmpeg.probe(in_filename)
    time = float(probe['streams'][0]['duration']) // 2
    width = probe['streams'][0]['width']
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)



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
        thumb_path = os.path.join(os.path.dirname(video.file.path), 'thumbs', os.path.splitext(os.path.basename(video.file.path))[0]+'.jpg')
        os.makedirs(os.path.dirname(thumb_path), exists_ok=True)
        generate_thumbnail(video.file.path, thumb_path)
        video.thumnail = thumb_path
        video.save()
        return super().form_valid(form)
