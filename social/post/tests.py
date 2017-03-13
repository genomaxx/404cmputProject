from django.test import TestCase, Client
from django.contrib.auth.models import User
from author.models import Follow, Author
from post.models import Post
from urllib import request
import base64, mimetypes


# Create your tests here.
class PrivacyTestCase(TestCase):

    def setUp(self):
        self.author_user = User.objects.create_user(username="author")
        self.viewer_user = User.objects.create_user(username="viewer")
        self.author = Author.objects.create(id=self.author_user)
        self.viewer = Author.objects.create(id=self.viewer_user)

    def test_public_post(self):
        post = Post.objects.create(author=self.author, privacyLevel=0)
        self.assertEqual(self.viewer.canViewPost(post), True)
        self.assertEqual(self.author.canViewPost(post), True)

    def test_private_post(self):
        post = Post.objects.create(author=self.author, privacyLevel=4)
        self.assertEqual(self.viewer.canViewPost(post), False)
        self.assertEqual(self.author.canViewPost(post), True)

    def test_friends_post(self):
        post = Post.objects.create(author=self.author, privacyLevel=1)

        self.assertEqual(self.viewer.canViewPost(post), False)
        self.assertEqual(self.author.canViewPost(post), True)

        Follow.objects.create(follower=self.viewer, followee=self.author)

        self.assertEqual(self.viewer.canViewPost(post), False)
        self.assertEqual(self.author.canViewPost(post), True)

        Follow.objects.create(follower=self.author, followee=self.viewer)

        self.assertEqual(self.viewer.canViewPost(post), True)
        self.assertEqual(self.author.canViewPost(post), True)


# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Abram")
        User.objects.create(username="Bill")

    def doLoginSetUp(self):
        # Set up users
        User.objects.create(username="Jerry", email="bill@nye.com", password="tweety")
        User.objects.create(username="Tom", email="abram@hindle.com", password="tweety")
        userObj = User.objects.get(username="Jerry")
        userObj.set_password(userObj.password)

        # Set up authors
        authorObj = Author.objects.create(id=userObj)
        authorObj.save()
        userObj.save()

        # Return a user and author object
        return userObj, authorObj

    def setUpOneAuthor(self, name):
        user = User.objects.get(username=name)
        authorObj = Author.objects.create(id=user)
        authorObj.save()
        return authorObj

    def createAPost(self, authorObj, context, privacy=0):
        post = Post.objects.create(author=authorObj, content=context, privacyLevel=privacy)
        return post

    def createAnImagePost(self, authorObj, context, privacy, input_image, imageurl):
        img = open(input_image, "rb").read()
        f = bytearray(img)
        mimetypes.init()
        newPost = Post.objects.create(author=authorObj, content=context,
                       privacyLevel=privacy, image = base64.b64encode(f),\
                       image_url = imageurl,\
                       image_type = mimetypes.guess_type(input_image))
        return newPost

    def queryForPublicPosts(self):
        return

    # Test if the author can make a post
    def test_canUserMakePost(self):
        authorObj = self.setUpOneAuthor("Abram")
        try:
            post = self.createAPost(authorObj, "test")
            post.save()
        except:
            self.assertFalse(True, "Author could not create a post")

        post2 = Post.objects.get(author=authorObj)
        self.assertEqual(post.author, post2.author, "Post is not made by the same author")
        authorObj.delete()

    # Tests if an author can post an image
    def test_canUserPostImage(self):
        authorObj = self.setUpOneAuthor("Abram")
        imagename = "local-filename.jpg"
        request.urlretrieve("http://www.chrysanthemums.org/wp-content/uploads/2016/04/White-chrysanthemum-flowers-beautifull.png", imagename)
        try:
            post = self.createAnImagePost(authorObj, "test image post", 0, imagename, "https://0.0.0.0:5000/post/1/")
            post.save()
        except:
            self.assertFalse(True, "Image post couldn't be made")

        get_post = Post.objects.get(author=authorObj)
        self.assertEqual(post.author, get_post.author, "Image post is not made by the same author")
        authorObj.delete()


    # Tests if posts can be deleted
    def test_canUserDeletePost(self):
        authorObj = self.setUpOneAuthor("Abram")
        post = self.createAPost(authorObj, "This is a test post!!!")
        post.save()
        post.delete()
        with self.assertRaises(Exception) as ex:
            getPost = Post.objects.get(author=authorObj)
            self.assertIsNone(getPost, "Post was not deleted")

        authorObj.delete()

    # Tests if posts can be deleted by the correct author_user
    def test_canSpecificAuthorDeletePost(self):
        c = Client()
        user, auth = self.doLoginSetUp()
        # response = c.login(username=user.username, password=user.password)
        response = c.post('/login/', {'user': user.username, 'password': user.password})
        self.assertEqual(response.status_code, 200, "User is not authenticated and logged in")
        response = c.get('/author/')
        self.assertEqual(response.status_code, 302, "User is not persistant across views")
        response = c.post('/author/author_post/', {'post_content':"I made a post, ain't that cool!", 'privacyLevel':"0"})
        self.assertEqual(response.status_code, 302, "User is not persistant across views")
        post2 = Post.objects.get(author=auth)
        print(post2.content)
        self.assertEqual("I made a post, ain't that cool!", post2.content, "Post is not made by the same author")

        response = c.get('/post/1/')
        print(response.content)
        user.delete()

    # Test if a post is public
    def test_isPostPublic(self):
        authorObj = self.setUpOneAuthor("Abram")
        post = self.createAPost(authorObj, "test")
        post.save()
        self.assertEqual(post.privacyLevel, 0, "Post is not default to public")
        authorObj.delete()

    # Test if a post is private
    def test_isPostPrivate(self):
        authorObj = self.setUpOneAuthor("Abram")
        post = self.createAPost(authorObj, "test", 4)
        post.save()
        self.assertEqual(post.privacyLevel, 4, "Post is not private")
        authorObj.delete()

    # Test if anyone can browse public posts
    # A bit wonky to test because it essentially tests a query, but it'll also
    # test if the privacy level gets set properly in the back end for querying.
    def test_arePublicPostOpenToEveryone(self):
        abram = self.setUpOneAuthor("Abram")
        post = self.createAPost(abram, "test")
        post.save()
        print(post.privacyLevel)
        getPost = Post.objects.get(privacyLevel=0)
        self.assertIsNotNone(getPost, "No posts returned")
        self.assertEqual(getPost.author.id.username, abram.id.username, "This author is not the same")
        self.assertEqual(getPost.content, "test", "The content is not the same")
        abram.delete()

    # Test if posts are private to only the author.
    def test_isAuthorPostPrivate(self):
        abram = self.setUpOneAuthor("Abram")
        bill = self.setUpOneAuthor("Bill")
        post = self.createAPost(abram, "test", 4)
        post.save()
        getPost = Post.objects.get(privacyLevel=4, author__id=abram.id)
        with self.assertRaises(Exception) as ex:
            getPost2 = Post.objects.get(privacyLevel=4, author__id=bill.id)
            self.assertIsNone(getPost2, "Bill got Abram's stuff")

        abram.delete()
        bill.delete()
