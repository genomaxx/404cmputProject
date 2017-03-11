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

    def test_friends_of_friends(self):
        emmett = Author.objects.get(id=self.emmett_user)
        scrunt = Author.objects.get(id=self.scrunt_user)
        u1 = User.objects.create_user(username="u1")
        u2 = User.objects.create_user(username="u2")
        fof1 = Author.objects.create(id=u1)
        fof2 = Author.objects.create(id=u2)

        self.assertEqual(emmett.isFriendOfFriend(fof1), False)
        self.assertEqual(scrunt.isFriendOfFriend(fof2), False)

        Follow.objects.create(follower=emmett, followee=scrunt)
        Follow.objects.create(follower=scrunt, followee=emmett)

        self.assertEqual(emmett.isFriendOfFriend(fof1), False)
        self.assertEqual(scrunt.isFriendOfFriend(fof2), False)

        Follow.objects.create(follower=scrunt, followee=fof1)
        Follow.objects.create(follower=fof1, followee=scrunt)
        Follow.objects.create(follower=fof1, followee=fof2)
        Follow.objects.create(follower=fof2, followee=fof1)

        self.assertEqual(emmett.isFriendOfFriend(fof1), True)
        self.assertEqual(emmett.isFriendOfFriend(fof2), False)
        self.assertEqual(emmett.isFriendOfFriend(scrunt), False)
