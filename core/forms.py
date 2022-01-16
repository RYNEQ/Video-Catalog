from django import forms
from .models import *

class VideoUploadForm(forms.ModelForm):
    # tags = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'required': 'false'}))

    # def clean(self):
    #     slug = slugify(self.title)
    #     # Chek slug in db and make error if exists

    class Meta:
        model = Video
        fields = '__all__'
        exclude = ['uuid', 'slug', 'cover', 'duration', 'status', 'enabled', 'user', 'tags']

