# Generated by Django 4.0 on 2022-01-05 12:38

import core.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.FileField(blank=True, upload_to=core.models._get_video_thumb_upload_path),
        ),
        migrations.AlterField(
            model_name='category',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(upload_to=core.models._get_video_upload_path),
        ),
        migrations.AlterField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='videos', to='core.Tag'),
        ),
        migrations.AlterField(
            model_name='video',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='UUID'),
        ),
    ]