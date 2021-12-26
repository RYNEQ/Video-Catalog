import os.path
from django.db import models
import uuid
import datetime
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver

class BaseCoreModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True


# @receiver(pre_save, sender='Video')
# def make_slug(sender, instance:'Video', **kwargs):
#     instance.slug = ...


class Video(BaseCoreModel):
    @staticmethod
    def get_upload_path(instance, file):
        filename, ext = os.path.split(file)
        uuid_name = uuid.uuid5(uuid.NAMESPACE_URL, filename)
        base_path = datetime.datetime.now().strftime("media/videos/%Y/%m/%d/")
        path = os.path.join(base_path, f"{uuid_name}{ext}")
        return path

    VIDEO_TYPE_PUBLIC = 1
    VIDEO_TYPE_PRIVATE = 2
    VIDEO_TYPE_CHOICES = ((VIDEO_TYPE_PRIVATE, _('Private')),
                          (VIDEO_TYPE_PUBLIC, _('Public')))

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=get_upload_path)
    video_type = models.IntegerField(choices=VIDEO_TYPE_CHOICES)
    tags = models.ManyToManyField('Tag', related_name='videos')
    category = models.ForeignKey('Category', related_name='videos',
                                 on_delete=models.PROTECT)

    slug = models.SlugField(allow_unicode=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ...
        return super().save(*args, **kwargs)


class Tag(BaseCoreModel):
    name = models.CharField(max_length=100)


class Category(BaseCoreModel):
    name = models.CharField(max_length=100)
