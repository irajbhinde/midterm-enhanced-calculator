class OperationError(Exception):
    """Raised when an invalid operation or arithmetic error occurs."""

class ValidationError(Exception):
    """Raised when user inputs are invalid or out of bounds."""

class HistoryError(Exception):
    """Raised for undo/redo/history issues."""

class PersistenceError(Exception):
    """Raised when saving/loading history fails."""