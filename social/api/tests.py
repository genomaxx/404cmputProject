# Django
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
# Django REST
from rest_framework.test import APIClient, APITestCase
# App
from comment.models import Comment
from author.models import Author
from post.models import Post
from api.posts import *
# Python
#from bson import json_util
import json
import uuid

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

    # Test GET request to end-point: api/post/
    def test_getAllPublicPosts(self):
        response = self.client.login(username=self.userObj.username, password="test")
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.client.logout()
    
    # Test POST request to end-point: api/post/
    def test_postAllPublicPosts(self):
        response = self.client.login(username=self.userObj.username, password="test")
        response = self.client.post('/api/posts/', {'test': 'test'}, format='json')
        self.assertEqual(response.status_code, 405, "Status code is not 405")
        self.client.logout()

    # Test ADD COMMENT request to end-point: api/posts/<uuid>/comments
    def test_addCommentToPost(self):
        response = self.client.login(username=self.userObj.username, password="test")
        user = User.objects.create(username="stupid")
        author = Author.objects.create(id=user, displayName="auth")
        author.setApiID()
        author.id.username = author.apiID
        post = Post.objects.get(author=self.authorObj, content=self.post1.content)
        post.setApiID()
        comment =  Comment.objects.create(post=post, author=self.authorObj, content='test comment')
        comment.setApiID()
        msg = {'query': 'addComment',
                   'post': 'whatever/test',
                   'comment': {
                       'author': {
                           'id': '0d5ea6edace642178ac5a29d43e14bfe',
                           'host': 'local host',
                           'displayName': str(author.displayName),
                           'url': author.url,
                           'github': author.github,
                            },
                       'comment': comment.content,
                       'contentType': comment.contentType,
                       'published': comment.publishDate,
                       'guid': '0d5ea6edace642178ac5a29d43e14fff',
                       },
                   }
        print('/api/posts/' + post.apiID + '/comments/')
        response = self.client.post('/api/posts/' + post.apiID + '/comments/', msg, format='json')
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.client.logout()
