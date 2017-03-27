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


def is_friends(author, visitor):
    if author.is_remote():
        return check_remote_friends(author, visitor)
    return author.isFriends(visitor)


def check_remote_friends(author, visitor):
    return None


def get_friend_status(author, visitor):
    if author == visitor:
        return "this is your profile"
    elif author.isFriend(visitor):
        return "you two are friends"
    elif author.isFollowing(visitor):
        return "they follow you"
    elif visitor.isFollowing(author):
        return "you follow them"
    else:
        return "you two aren't friends"
