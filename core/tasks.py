from celery import shared_task
from . import models

@shared_task
def process_uploaded_video(objid: int):
    obj = models.Video.all_objects.get(pk=objid)
    if not obj.duration:
        obj.update_duration_from_video()
    obj.generate_cover_image()
    obj.status = obj.VIDEO_STATUS_PUBLISHED
    obj.save()
    return f"Video {obj.uuid} published successfully"