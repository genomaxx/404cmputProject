from django.test import TestCase, Client
from author.models import Author
from post.models import Post
from django.contrib.auth.models import User

# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="Abram")
        User.objects.create(username="Bill")
    
    def setUpOneAuthor(self, name):
        user = User.objects.get(username=name)
        authorObj = Author.objects.create(id=user)
        authorObj.save()
        return authorObj

    def createAPost(self, authorObj, context, privacy=0):
        post = Post.objects.create(author=authorObj, content=context, privacyLevel=privacy)
        return post

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
        self.assertEqual(post.author, post2.author, "Post is not make by the same author")
        authorObj.delete()

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
    # A bit wonky to test because it essentially tests a query, but it'll also test
    # if the privacy level gets set properly in the back end for querying.
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
        