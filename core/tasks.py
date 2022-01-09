from celery import shared_task
from .models import *

@shared_task
def process_uploaded_video(obj: 'Video'):
    if not obj.duration:
        obj.update_duration_from_video()
    obj.generate_cover_image()
    obj.status = obj.VIDEO_STATUS_PUBLISHED
    obj.save()
    return f"Video {obj.uuid} published successfully"