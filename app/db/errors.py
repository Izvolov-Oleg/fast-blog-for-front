class UserDoesNotExist(Exception):
    """Raised when user was not found in DB"""


class PostDoesNotExist(Exception):
    """Raised when post with id was not found in DB"""


class CommentDoesNotExist(Exception):
    """Raised when comment with id was not found in DB"""
