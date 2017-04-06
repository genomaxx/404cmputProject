from django.test import TestCase, Client
from author.models import Author, Follow
from django.contrib.auth.models import User


# Create your tests here.
class AuthorTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Bill", email="bill@nye.com", password="test")
        User.objects.create(username="Abram", email="abram@hindle.com", password="test")

    def loginSetUp(self):
        userObj = User.objects.get(username="Bill")
        userObj.set_password(userObj.password)
        userObj.save()
        return userObj

    # Testing for normalization. Each author should have only 1 account per username.
    def test_isAuthorOneToOnePerUser(self):
        user = User.objects.get(username="Bill")
        author1 = Author.objects.create(id=user)
        self.assertIsNotNone(author1, "Author 1 was not created")

        try:
            author1.save()
            author1.delete()
        except Exception as e:
            self.assertFalse(True, "Author did not save")

        # Trying to create an author linked to the same user throws exception
        with self.assertRaises(Exception):
            Author.object.create(id=user)

    # Testing for persistance. If user has correct credentials they should be able to login
    # authentication and should be able to log out
    def test_isUserAuthenticatedAndLoggedIn(self):
        user = self.loginSetUp()
        c = Client()
        response = c.post('/login/', {'user': user.username, 'password': user.password})
        self.assertEqual(response.status_code, 200, "User is not authenticated and logged in")
        user.delete()

    # Testing for persistance across views
    def test_isUserPersistant(self):
        user = self.loginSetUp()
        c = Client()
        response = c.login(username=user.username, password=user.password)
        response = c.get('/author/')
        self.assertEqual(response.status_code, 302, "User is not persistant across views")
        user.delete()

    # Testing if the user can log in and log back out to demonstrate persistance on the server
    def test_isUserLoggedOut(self):
        user = self.loginSetUp()
        c = Client()
        response = c.post('/login/', {'user': user.username, 'password': user.password})
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 302, "User did not log out")
        user.delete()

    # Testing for multiple users. Ensure the server can create
    # multiple authors (and therefore save multiple authors to the db)
    def test_areAuthorsUnique(self):
        user1 = User.objects.get(username="Bill")
        user2 = User.objects.get(username="Abram")
        author1 = Author.objects.create(id=user1)
        author1.setApiID()
        author1.approved = True
        author1.save()
        author2 = Author.objects.create(id=user2)
        author2.setApiID()
        author2.approved = True

        self.assertIsNot(author1, author2, "Two authors are the same")

        try:
            author2.save()
        except Exception as e:
            self.assertFalse(True, "Author did not save")

        author1.delete()
        author2.delete()


# Create your tests here.
class FollowTestCase(TestCase):

    def setUp(self):
        self.emmett_user = User.objects.create_user(username="emmettu")
        self.scrunt_user = User.objects.create_user(username="scruntscrunt")
        a1 = Author.objects.create(id=self.emmett_user)
        a1.setApiID()
        a1.approved = True
        a1.save()
        a2 = Author.objects.create(id=self.scrunt_user)
        a2.setApiID()
        a2.approved = True
        a2.save()

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
        fof1.setApiID()
        fof1.approved = True
        fof1.save()
        fof2 = Author.objects.create(id=u2)
        fof2.setApiID()
        fof2.approved = True
        fof2.save()

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
