class TargetsConsumed(Exception):
    """
    Thrown when all targets returned no valid posts
    """
    pass


class NoMorePosts(Exception):
    """
    Thrown when all saved media have been posted
    """
    pass

