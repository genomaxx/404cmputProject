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

def unlistedView(viewer, post):
    return True

def unlistedFeed(viewer, post):
    return False



post_predicates = [
    public,
    friends,
    friends_of_friends,
    private_message,
    private,
    unlistedView,
]

feed_predicates = [
    public,
    friends,
    friends_of_friends,
    private_message,
    private,
    unlistedFeed,
]


def can_view_post(viewer, post):
    return post_predicates[post.privacyLevel](viewer, post)

def can_view_feed(viewer, post):
    return feed_predicates[post.privacyLevel](viewer, post)
