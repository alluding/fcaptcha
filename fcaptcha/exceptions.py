class InvalidJSON(Exception):
    """
    Base exception raised when the given JSON data is invalid/improper.
    """
    pass

class InvalidArgs(Exception):
    """
    Base exception raised when the incorrect arguments are given, or are not given.
    """
    pass

class NoBalance(Exception):
    """
    Base exception raised when a key has no balance.
    """
    pass

class InvalidAPIKey(Exception):
    """
    Base exception raised when the authorization/API key is invalid.
    """
    pass

class TaskNotFound(Exception):
    """
    Base exception raised when the task ID isn't found.
    """
    pass

class UnknownError(Exception):
    """
    Base exception raised when something besides the known errors occurs.
    """
    pass
