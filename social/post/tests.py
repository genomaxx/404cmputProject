from django.test import TestCase
from django.contrib.auth.models import User
from author.models import Follow, Author
from post.models import Post
# from .utils.follow import is_friend, is_follower


# Create your tests here.
class PrivacyTestCase(TestCase):

    def setUp(self):
        self.author_user = User.objects.create_user(username="author")
        self.viewer_user = User.objects.create_user(username="viewer")
        self.author = Author.objects.create(id=self.author_user)
        self.viewer = Author.objects.create(id=self.viewer_user)

    def test_public_post(self):
        post = Post.objects.create(author=self.author, privacyLevel=0)
        self.assertEqual(self.viewer.canView(post), True)
        self.assertEqual(self.author.canView(post), True)

    def test_private_post(self):
        post = Post.objects.create(author=self.author, privacyLevel=4)
        self.assertEqual(self.viewer.canView(post), False)
        self.assertEqual(self.author.canView(post), True)

    def test_friends_post(self):
        post = Post.objects.create(author=self.author, privacyLevel=1)

        self.assertEqual(self.viewer.canView(post), False)
        self.assertEqual(self.author.canView(post), True)

        Follow.objects.create(follower=self.viewer, followee=self.author)

        self.assertEqual(self.viewer.canView(post), False)
        self.assertEqual(self.author.canView(post), True)

        Follow.objects.create(follower=self.author, followee=self.viewer)

        self.assertEqual(self.viewer.canView(post), True)
        self.assertEqual(self.author.canView(post), True)
