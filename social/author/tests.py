from django.test import TestCase
from django.contrib.auth.models import User
from .models import Follow, Author
# from .utils.follow import is_friend, is_follower


# Create your tests here.
class FollowTestCase(TestCase):

    def setUp(self):
        self.emmett_user = User.objects.create_user(username="emmettu")
        self.scrunt_user = User.objects.create_user(username="scruntscrunt")
        Author.objects.create(id=self.emmett_user)
        Author.objects.create(id=self.scrunt_user)

    def test_follower(self):
        emmett = Author.objects.get(id=self.emmett_user)
        scrunt = Author.objects.get(id=self.scrunt_user)

        self.assertEqual(emmett.isFollowing(scrunt), False)
        self.assertEqual(scrunt.isFollowing(emmett), False)

        Follow.objects.create(follower=emmett, followee=scrunt)

        self.assertEqual(emmett.isFollowing(scrunt), True)
        self.assertEqual(scrunt.isFollowing(emmett), False)

    def test_friend(self):
        emmett = Author.objects.get(id=self.emmett_user)
        scrunt = Author.objects.get(id=self.scrunt_user)

        self.assertEqual(emmett.isFriend(scrunt), False)
        self.assertEqual(scrunt.isFriend(emmett), False)

        Follow.objects.create(follower=emmett, followee=scrunt)
        Follow.objects.create(follower=scrunt, followee=emmett)

        self.assertEqual(emmett.isFriend(scrunt), True)
        self.assertEqual(scrunt.isFriend(emmett), True)
