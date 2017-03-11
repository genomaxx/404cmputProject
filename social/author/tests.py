from django.test import TestCase, Client
from author.models import Author, Follow
from django.contrib.auth.models import User
from .utils.follow import is_friend, is_follower

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
        with self.assertRaises(Exception) as ex:
            ex = Author.object.create(id=user)

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
        response = c.get('/a/')
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
        author2 = Author.objects.create(id=user2)

        self.assertIsNot(author1, author2, "Two authors are the same")

        try:
            author1.save()
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
        Author.objects.create(id=self.emmett_user)
        Author.objects.create(id=self.scrunt_user)

    def test_follower(self):
        emmett = Author.objects.get(id=self.emmett_user)
        scrunt = Author.objects.get(id=self.scrunt_user)

        self.assertEqual(is_follower(emmett, scrunt), False)
        self.assertEqual(is_follower(scrunt, emmett), False)

        Follow.objects.create(follower=emmett, followee=scrunt)

        self.assertEqual(is_follower(emmett, scrunt), True)
        self.assertEqual(is_follower(scrunt, emmett), False)

    def test_friend(self):
        emmett = Author.objects.get(id=self.emmett_user)
        scrunt = Author.objects.get(id=self.scrunt_user)

        self.assertEqual(is_follower(emmett, scrunt), False)
        self.assertEqual(is_follower(scrunt, emmett), False)

        Follow.objects.create(follower=emmett, followee=scrunt)
        Follow.objects.create(follower=scrunt, followee=emmett)

        self.assertEqual(is_friend(emmett, scrunt), True)
        self.assertEqual(is_friend(scrunt, emmett), True)
