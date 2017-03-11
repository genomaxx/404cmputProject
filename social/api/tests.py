# Django
from django.test import TestCase
from django.contrib.auth.models import User
# Django REST
from rest_framework.test import APIClient, APITestCase
# App
from author.models import Author
from post.models import Post
from api.posts import *
# Python
import json

# Create your tests here.
class PostApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.userObj = User.objects.create(username="TestCase__Bill__", password="test")
        self.userObj.set_password(self.userObj.password)
        self.userObj.save()
        self.authorObj = Author.objects.create(id=self.userObj)
        self.authorObj.save()


        self.post1 = Post.objects.create(author=self.authorObj,
                                         content="Test post 1",
                                         privacyLevel=0)
        self.post2 = Post.objects.create(author=self.authorObj,
                                         content="Test post2",
                                         privacyLevel=0)
        self.post1.save()
        self.post2.save()

    def tearDown(self):
        self.userObj.delete()
        self.post1.delete()
        self.post2.delete()
        del self.authorObj
        del self.userObj
        del self.client
        del self.post1
        del self.post2

    # Test GET request to end-point: service/post/
    def test_getAllPublicPosts(self):
        response = self.client.login(username=self.userObj.username, password="test")
        response = self.client.get('/service/post/')
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.client.logout()
    
    # Test POST request to end-point: service/post/
    def test_postAllPublicPosts(self):
        response = self.client.login(username=self.userObj.username, password="test")
        response = self.client.post('/service/post/', {'test': 'test'}, format='json')
        self.assertEqual(response.status_code, 405, "Status code is not 405")
        self.client.logout()