import os.path
from django.db import models
import uuid
import datetime
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.core.cache import cache as default_cache


class BaseCoreModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name=_("UUID"))
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# @receiver(pre_save, sender='Video')
# def make_slug(sender, instance:'Video', **kwargs):
#     instance.slug = ...

def _get_video_upload_path(instance, file):
        filename, ext = os.path.splitext(file)
        uuid_name = uuid.uuid5(uuid.NAMESPACE_URL, filename)
        base_path = datetime.datetime.now().strftime("videos/%Y/%m/%d/")
        path = os.path.join(base_path, f"{uuid_name}{ext}")
        print("Path -> ", path)
        return path

def _get_video_thumb_upload_path(instance, file):
        filename, ext = os.path.splitext(file)
        uuid_name = uuid.uuid5(uuid.NAMESPACE_URL, filename)
        base_path = datetime.datetime.now().strftime("videos/%Y/%m/%d/thumbs")
        path = os.path.join(base_path, f"{uuid_name}{ext}")
        print("Path -> ", path)
        return path


class Video(BaseCoreModel):
    VIDEO_TYPE_PUBLIC = 1
    VIDEO_TYPE_PRIVATE = 2
    VIDEO_TYPE_CHOICES = ((VIDEO_TYPE_PRIVATE, _('Private')),
                          (VIDEO_TYPE_PUBLIC, _('Public')))

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=_get_video_upload_path)
    video_type = models.IntegerField(choices=VIDEO_TYPE_CHOICES, default=VIDEO_TYPE_PUBLIC)
    tags = models.ManyToManyField('Tag', related_name='videos', blank=True)
    category = models.ForeignKey('Category', related_name='videos',
                                 on_delete=models.PROTECT)

    slug = models.SlugField(allow_unicode=True, unique=True, default=None)
    duration = models.IntegerField()
    thumbnail = models.FileField(upload_to=_get_video_thumb_upload_path, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def age(self):
        age = default_cache.get(f'video_age_{self.pk}')
        if not age:
            now = timezone.now()
            tommorow = datetime.timedelta(days=1)+self.create_date
            midnight = datetime.datetime.combine(tommorow, datetime.time.min)

            start_of_day_create = datetime.datetime.combine(self.create_date, datetime.time.min)
            diff = now - timezone.make_aware(start_of_day_create)
            age = diff.days
            default_cache.set(f'video_age_{self.pk}', age, timeout=(timezone.make_aware(midnight)-now).seconds)

        return age



class Tag(BaseCoreModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(BaseCoreModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
