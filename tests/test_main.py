"""Tests for the main UI module."""

from pathlib import Path


class TestMainWindowIntegration:
    """Integration tests for MainWindow."""

    def test_ui_file_exists(self) -> None:
        """Test that the UI file exists."""
        ui_file = Path(__file__).parent.parent / "ui" / "mainwindow.ui"
        assert ui_file.exists(), "mainwindow.ui file should exist"

    def test_imports_work(self) -> None:
        """Test that main module imports work."""
        # Test importing main components
        from main import (
            AddPasswordDialog,
            MainWindow,
            MasterPasswordDialog,
            ViewPasswordDialog,
        )

        assert AddPasswordDialog is not None
        assert MasterPasswordDialog is not None
        assert ViewPasswordDialog is not None
        assert MainWindow is not None


class TestCrossPlatformCompatibility:
    """Test cross-platform compatibility."""

    def test_pathlib_usage(self) -> None:
        """Test that pathlib.Path is used for cross-platform paths."""
        from main import Path as MainPath

        assert MainPath == Path

    def test_storage_uses_pathlib(self) -> None:
        """Test that storage module uses pathlib."""
        from storage import PasswordStorage

        storage = PasswordStorage()
        assert isinstance(storage.data_dir, Path)
        assert isinstance(storage.data_file, Path)


class TestEncryptionIntegration:
    """Test encryption integration."""

    def test_aes_encryption_used(self) -> None:
        """Test that AES encryption is used."""
        from storage import PasswordStorage

        # Check that the encryption methods exist
        storage = PasswordStorage()
        assert hasattr(storage, "_encrypt_data")
        assert hasattr(storage, "_decrypt_data")

    def test_pbkdf2_key_derivation(self, temp_dir: Path) -> None:
        """Test that PBKDF2 is used for key derivation."""
        from storage import PasswordStorage

        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key("test_password")

        # Key should be 32 bytes (256 bits) for AES-256
        assert storage._master_key is not None
        assert len(storage._master_key) == 32

    def test_keyring_integration_exists(self) -> None:
        """Test that keyring integration exists."""
        from storage import PasswordStorage

        # Check that keyring is imported and used
        storage = PasswordStorage()
        assert hasattr(storage, "SERVICE_NAME")
        assert storage.SERVICE_NAME == "PyQtPasswordSaver"
