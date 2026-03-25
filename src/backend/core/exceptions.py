class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(DomainException):
    """Raised when a specific entity is not found in the database or service logic."""
    pass
