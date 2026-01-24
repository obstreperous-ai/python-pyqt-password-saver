"""Password Saver - A secure, cross-platform desktop password manager."""

__version__ = "0.1.0"

from password_saver.main import main
from password_saver.storage import PasswordStorage

__all__ = ["main", "PasswordStorage", "__version__"]
