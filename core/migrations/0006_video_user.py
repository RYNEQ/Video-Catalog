# Generated by Django 4.0 on 2022-01-16 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0005_category_enabled_tag_enabled_video_enabled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
    ]
