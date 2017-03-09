from django.test import TestCase, Client
from django.core import exceptions
from author.models import Author
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your tests here.
class AuthorTestCast(TestCase):
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
            self.assertFalse(False, "Author did not save")

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
            self.assertFalse(False, "Author did not save")

        author1.delete()
        author2.delete()





   