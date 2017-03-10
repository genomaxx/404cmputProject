from author.models import Follow


def is_friend(author1, author2):

    return is_follower(author1, author2) and is_follower(author2, author1)


def is_follower(author1, author2):

    follows = Follow.objects.filter(follower=author1, followee=author2)
    return follows.exists()
