from django.test import TestCase, Client
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
        self.client = Client()

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

    def test_category(self):
        cat = models.Category.objects.create(name='testcat')
        self.assertIsNotNone(cat.pk)
        count = models.Category.objects.all().count()
        self.assertEqual(count, 1)

    def test_video_upload(self):
        cat = models.Category.objects.create(name='testcat')
        # with open('video.mp4', 'rb') as f:
        #     data = {
        #         'title': 'test video 1',
        #         'video_type': models.Video.VIDEO_TYPE_PUBLIC,
        #         'category': cat.pk,
        #         'file': f
        #     }
        #     response = self.client.post('/upload_video')
        uf = SimpleUploadedFile('sample_video.mp4', b"some data", content_type='video/mp4')
        data = {
            'title': 'test video 1',
            'video_type': models.Video.VIDEO_TYPE_PUBLIC,
            'category': cat.pk,
            'file': uf
        }
        response = self.client.post('/upload_video', data)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(models.Video.objects.all().count(), 1)
        self.assertEqual(models.Video.all_objects.all().count(), 1)


    def test_video_list(self):
        cat = models.Category.objects.create(name='testcat')
        uf = SimpleUploadedFile('sample_video.mp4', b"some data", content_type='video/mp4')
        v = models.Video.objects.create(title='Test Video number 1',
                                        status=models.Video.VIDEO_STATUS_PUBLISHED,
                                        category=cat,
                                        cover='image.jpg',
                                        duration=1000,
                                        file=uf)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Video number 1')
        self.assertEqual(len(response.context['object_list']), 1)


    # def test_all_in_order(self):
    #     self.test_video_upload()
    #     self.test_video_list()