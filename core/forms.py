from django import forms
from .models import *

class VideoUploadForm(forms.ModelForm):
    # tags = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'required': 'false'}))

    class Meta:
        model = Video
        fields = '__all__'
        exclude = ['uuid', 'slug', 'cover', 'duration', 'status']
