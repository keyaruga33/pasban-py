class DatabaseNotFound(Exception):
    pass


class WordAlreadyExistsError(Exception):
    """Raised when trying to add a word that already exists in the database."""
    pass


class WordNotFoundError(Exception):
    """Raised when a word is not found in the database."""
    pass
