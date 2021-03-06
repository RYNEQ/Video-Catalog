# Generated by Django 4.0 on 2022-01-05 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_video_cover_video_duration_alter_category_uuid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='status',
            field=models.IntegerField(choices=[(1, 'Published'), (2, 'Suspended'), (3, 'Processing')], default=3),
        ),
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.IntegerField(blank=True),
        ),
    ]
