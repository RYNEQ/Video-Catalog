from django.test import TestCase
import unittest
from . import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import tag
import datetime

# class VideoTestCase(unittest.TestCase):
class VideoTestCase(TestCase):
    # databases = ['test']
    # fixtures = [{...}]

    def setUp(self):
        ...

    @tag('fast', 'core')
    def test_slug(self):
        cat = models.Category.objects.create(name='testcat')
        #                                                                       MIME Type
        uf = SimpleUploadedFile('sample_video.mp4', b"some data", content_type='video/mp4')
        v = models.Video(title='Test Video number 1', category=cat, file=uf)
        v.save()
        self.assertIsNotNone(v.slug)
        self.assertGreater(len(v.slug), 0)

    @tag('fast', 'dynamics')
    def test_age_calculation(self):
        cat = models.Category.objects.create(name='testcat')
        uf = SimpleUploadedFile('sample_video.mp4', b"some data", content_type='video/mp4')
        past = datetime.datetime.now() - datetime.timedelta(days=10)
        v = models.Video.objects.create(title='Test Video number 1', category=cat, file=uf)
        v.create_date = past
        # 2. unittest mock
        # 3. fixture!
        self.assertEqual(v.age, 10)