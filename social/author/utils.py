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


def get_friend_status(author, visitor):
    if author == visitor:
        return "This is your profile"
    elif author.isFriend(visitor):
        return "You're friends"
    elif author.isFollowing(visitor):
        return "They follow you"
    elif visitor.isFollowing(author):
        return "You follow them"
    else:
        return "You're not friends"
