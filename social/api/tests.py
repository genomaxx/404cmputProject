# Django
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Django REST
from rest_framework.test import APIClient, APITestCase
# App
from comment.models import Comment
from author.models import Author, Follow
from post.models import Post
from node.models import Node
from settings.models import Settings
from api.posts import *
# Python
#from bson import json_util
import json
import uuid
APP_URL = settings.APP_URL

# Create your tests here.
class PostApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.userObj = User.objects.create(username="TestCase__Bill__", email="billsemail@email.com", password="test")
        self.userObj.set_password(self.userObj.password)
        self.userObj.is_active = True
        self.userObj.save()
        newUser = User.objects.get(email=self.userObj.email)
        self.authorObj = Author(id=newUser)
        self.authorObj.setDisplayName()
        self.authorObj.setAuthorURL()
        self.authorObj.setApiID()
        self.authorObj.approved = True
        self.authorObj.save()

        self.userObj2 = User.objects.create(username="TestCase__Tim__", email="tim@email.com", password="test")
        self.userObj2.set_password(self.userObj2.password)
        self.userObj2.is_active = True
        self.userObj2.save()
        newUser = User.objects.get(email=self.userObj2.email)
        self.authorObj2 = Author(id=newUser)
        self.authorObj2.setDisplayName()
        self.authorObj2.setApiID()
        self.authorObj2.approved = True
        self.authorObj2.save()

        self.follow1 = Follow(follower=self.authorObj,
                              followee=self.authorObj2)
        self.follow1.save()
        self.follow2 = Follow(follower=self.authorObj2,
                              followee=self.authorObj)
        self.follow2.save()

        self.n1 = Node(
            url="http://coolbear.herokuapp.com/",
            user=self.userObj,
            username="group8",
            password="tester123",
            trusted=True
        )
        self.n1.save()

        self.setting = Settings(
            auth_required = False)
        self.setting.save()

        self.post1 = Post.objects.create(author=self.authorObj,
                                         content="Test post 1",
                                         privacyLevel=0,
                                         origin="http://polar-savannah-14727/")
        self.post1.setApiID()
        self.post1.save()

        self.post2 = Post.objects.create(author=self.authorObj,
                                         content="Test post2",
                                         privacyLevel=1)
        self.post2.setApiID()
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
        ### make sure post is there
        # postcheck = Post.objects.get(privacyLevel=0)
        # self.assertEqual(self.post1.author, postcheck.author, "Post is not made by the same author")

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
        comment =  Comment.objects.create(post=self.post1, author=self.authorObj, content='test comment')
        comment.setApiID()

        msg = {'query': 'addComment',
                   'post': self.post1.apiID,
                   'comment': {
                       'author': {
                           'id': self.authorObj.apiID,
                           'host': APP_URL,
                           'displayName': self.authorObj.displayName,
                           'url': self.authorObj.url,
                           'github': self.authorObj.github,
                            },
                       'comment': comment.content,
                       'contentType': comment.contentType,
                       'published': comment.publishDate,
                       'id': comment.apiID,
                       },
                   }
        response = self.client.post('/api/posts/' + self.post1.apiID + '/comments/', msg, format='json')
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        self.client.logout()
        
        # Test GET requeest for an author's profile
    def test_getProfile(self):
        response = self.client.login(username=self.userObj.username, password="test")
        uri = '/api/author/' + str(self.authorObj.UID) + '/'
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        displayName = response.data['displayName']
        self.assertEqual(displayName, 'TestCase__Bill__', "Wrong user")
        self.client.logout()
        
        # Test GET single post
    def test_getSinglePost(self):
        response = self.client.login(username=self.userObj.username, password="test")
        uri = '/api/posts/' + str(self.post1.UID) + '/'
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        content = response.data['content']
        self.assertEqual(content, "Test post 1", "Wrong content")
        self.client.logout()

    def test_getFriends(self):
        response = self.client.login(username=self.userObj.username, password="test")
        uri = '/api/author/' + str(self.authorObj.UID) + '/friends/' + str(self.authorObj2.UID)
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200, "Status code is not 200")
        friends = response.data['friends']
        print(friends)
        self.assertTrue(friends, "Should be friends")
        self.client.logout()