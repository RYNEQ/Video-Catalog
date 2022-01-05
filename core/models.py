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
import ffmpeg
import os
from django.conf import settings
from pymediainfo import MediaInfo

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

def _get_video_cover_upload_path(instance, file):
        filename, ext = os.path.splitext(file)
        uuid_name = uuid.uuid5(uuid.NAMESPACE_URL, filename)
        base_path = datetime.datetime.now().strftime("videos/%Y/%m/%d/thumbs")
        path = os.path.join(base_path, f"{uuid_name}{ext}")
        print("Path -> ", path)
        return path

def generate_thumbnail(in_filename, out_filename, screen_width=300):
    probe = ffmpeg.probe(in_filename)
    time = float(probe['streams'][0]['duration']) // 2
    width = probe['streams'][0]['width']
    try:
        (
            ffmpeg
            .input(in_filename, ss=time) # -> X
            .filter('scale', screen_width, -1)  # -> X
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        # print(e.stderr.decode(), file=sys.stderr)
        raise

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
    duration = models.IntegerField(blank=True)
    cover = models.FileField(upload_to=_get_video_cover_upload_path, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.duration:
            self.update_duration_from_video()

        self.generate_cover_image()

        return super().save(*args, **kwargs)

    def clean(self):
        print(self.file)

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

    def update_duration_from_video(self):
        duration = None
        if isinstance(self.file.file, TemporaryUploadedFile):
            path = self.file.file.file.name
        else:
            path = self.file.path
        media = MediaInfo.parse(path)
        for t in media.tracks:
            if t.track_type == "Video":
                duration = t.duration
                break
        self.duration = duration
        return self.duration

    def generate_cover_image(self):
        if isinstance(self.file.file, TemporaryUploadedFile):
            path = self.file.file.file.name
        else:
            path = self.file.path
        thumb_path = os.path.join(os.path.dirname(path),
                                  'thumbs',
                                  os.path.splitext(os.path.basename(path))[0]+'.jpg')

        os.makedirs(os.path.dirname(thumb_path), exists_ok=True)  # Bad
        generate_thumbnail(path, thumb_path)
        self.cover = thumb_path
        return self.cover


class Tag(BaseCoreModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(BaseCoreModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
