from post.models import Post
from author.models import Author


def getPosts(author):
    return Post.objects.filter(
        author=author
    )


def getPostsFromFriends(author):
    posts = []
    for f in author.getFriends():
        posts += getPosts(f)
    return posts


def friend_posts(id):
    author = Author.objects.get(
        id__id=id
    )
    return getPostsFromFriends(author)
