class AppError(Exception):
    """Base exception for the application."""


class NotFoundError(AppError):
    """Raised when an entity is not found."""


class ValidationError(AppError):
    """Raised when data validation fails."""


class OutOfStockError(AppError):
    """Raised when trying to loan an item with no stock available."""


class DuplicateLoanError(AppError):
    """Raised when a member tries to loan the same tool twice (active)."""