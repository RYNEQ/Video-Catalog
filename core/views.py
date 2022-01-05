from django.shortcuts import render, redirect
from django.views import View      # Custom
from django.views.generic import ListView
from django.views.generic import FormView # Creation ModelForm
from .forms import *
from .models import *


class HomePageView(ListView):
    template_name = 'core/video_list.html'
    queryset = Video.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     return super().get_queryset(*args, **kwargs)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     ...




class VideUploadView(FormView):
    """
    Process Upload of video from user side
    """
    form_class = VideoUploadForm
    template_name = 'core/video_upload_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)  # Run clean & clean_ methods
