def public(viewer, post):
    return True


def friends(viewer, post):
    return viewer.isFriend(post.author) or private(viewer, post)


def friends_of_friends(viewer, post):
    return viewer.isFriendOfFriend(post.author) \
           or private(viewer, post) \
           or viewer.isFriend(post.author)


def private_message(viewer, post):
    return False


def private(viewer, post):
    return viewer == post.author


post_predicates = [
    public,
    friends,
    friends_of_friends,
    private_message,
    private
]


def can_view(viewer, post):
    return post_predicates[post.privacyLevel](viewer, post)
