"""Custom exception classes for the application."""


class AppError(Exception):
    """Base application error."""
    pass


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""
    pass


class ValidationError(AppError):
    """Raised when input validation fails."""
    pass


class DatabaseError(AppError):
    """Raised when a database operation fails."""
    pass

class ApplicationNotFoundError(Exception):
    def __init__(self, application_id: int):
        self.application_id = application_id
        super().__init__(f"Application with id {application_id} not found")