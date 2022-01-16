from django.contrib import admin
from .models import *

class SharedFeatures:
    readonly_fields = ['uuid']

class CategoryAdmin(admin.ModelAdmin, SharedFeatures):
    list_display = ['uuid', 'name', 'video_count']

    def video_count(self, obj, *args, **kwargs):
        return obj.videos.count()

class TagAdmin(admin.ModelAdmin, SharedFeatures):
    ...

class VideoAdmin(admin.ModelAdmin, SharedFeatures):
    list_display = ['uuid', 'title', 'status']
    readonly_fields = ['uuid', 'user']

    # def get_queryset(self, request):
    #     return Video.all_objects.all()

admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Tag, TagAdmin)
