"""Tests for the storage module."""

from pathlib import Path
from typing import Any

import pytest

from storage import PasswordStorage


class TestPasswordStorage:
    """Test suite for PasswordStorage class."""

    def test_initialization_with_default_dir(self) -> None:
        """Test initialization with default directory."""
        storage = PasswordStorage()
        assert storage.data_dir == Path.home() / ".password_saver"
        assert storage.data_file == storage.data_dir / "passwords.enc"

    def test_initialization_with_custom_dir(self, temp_dir: Path) -> None:
        """Test initialization with custom directory."""
        storage = PasswordStorage(data_dir=temp_dir)
        assert storage.data_dir == temp_dir
        assert storage.data_file == temp_dir / "passwords.enc"
        assert temp_dir.exists()

    def test_initialize_master_key(self, temp_dir: Path, master_password: str) -> None:
        """Test master key initialization."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)
        assert storage._master_key is not None
        assert len(storage._master_key) == 32  # AES-256 requires 32 bytes

    def test_master_key_consistency(self, temp_dir: Path, master_password: str) -> None:
        """Test that same password generates same key with same salt."""
        storage1 = PasswordStorage(data_dir=temp_dir)
        storage1.initialize_master_key(master_password)
        key1 = storage1._master_key

        # Create new storage instance with same directory (should use same salt)
        storage2 = PasswordStorage(data_dir=temp_dir)
        storage2.initialize_master_key(master_password)
        key2 = storage2._master_key

        assert key1 == key2

    def test_encrypt_decrypt_data(self, temp_dir: Path, master_password: str) -> None:
        """Test encryption and decryption of data."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        test_data = b"This is a test message with special chars: !@#$%^&*()"
        encrypted = storage._encrypt_data(test_data)
        assert encrypted != test_data
        assert len(encrypted) > len(test_data)  # IV + encrypted data

        decrypted = storage._decrypt_data(encrypted)
        assert decrypted == test_data

    def test_encrypt_without_master_key(self, temp_dir: Path) -> None:
        """Test that encryption fails without master key."""
        storage = PasswordStorage(data_dir=temp_dir)
        with pytest.raises(ValueError, match="Master key not initialized"):
            storage._encrypt_data(b"test")

    def test_decrypt_without_master_key(self, temp_dir: Path) -> None:
        """Test that decryption fails without master key."""
        storage = PasswordStorage(data_dir=temp_dir)
        with pytest.raises(ValueError, match="Master key not initialized"):
            storage._decrypt_data(b"test")

    def test_save_and_load_passwords(
        self, temp_dir: Path, master_password: str, sample_passwords: dict[str, dict[str, Any]]
    ) -> None:
        """Test saving and loading passwords."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        # Save passwords
        storage.save_passwords(sample_passwords)
        assert storage.data_file.exists()

        # Load passwords
        loaded = storage.load_passwords()
        assert loaded == sample_passwords

    def test_load_passwords_empty_file(self, temp_dir: Path, master_password: str) -> None:
        """Test loading passwords when file doesn't exist."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        loaded = storage.load_passwords()
        assert loaded == {}

    def test_load_passwords_wrong_key(
        self, temp_dir: Path, master_password: str, sample_passwords: dict[str, dict[str, Any]]
    ) -> None:
        """Test that loading with wrong password fails."""
        storage1 = PasswordStorage(data_dir=temp_dir)
        storage1.initialize_master_key(master_password)
        storage1.save_passwords(sample_passwords)

        # Try to load with different password
        # First remove the salt file to force new salt generation
        salt_file = temp_dir / ".salt"
        if salt_file.exists():
            salt_file.unlink()

        storage2 = PasswordStorage(data_dir=temp_dir)
        storage2.initialize_master_key("wrong_password")

        with pytest.raises(ValueError, match="Failed to load passwords"):
            storage2.load_passwords()

    def test_add_password(self, temp_dir: Path, master_password: str) -> None:
        """Test adding a password."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        storage.add_password("test.com", "testuser", "testpass", "Test notes")

        # Verify password was saved
        passwords = storage.load_passwords()
        assert "test.com" in passwords
        assert passwords["test.com"]["username"] == "testuser"
        assert passwords["test.com"]["password"] == "testpass"
        assert passwords["test.com"]["notes"] == "Test notes"

    def test_add_password_update_existing(self, temp_dir: Path, master_password: str) -> None:
        """Test updating an existing password."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        # Add initial password
        storage.add_password("test.com", "user1", "pass1", "notes1")

        # Update the same service
        storage.add_password("test.com", "user2", "pass2", "notes2")

        # Verify it was updated
        passwords = storage.load_passwords()
        assert len(passwords) == 1
        assert passwords["test.com"]["username"] == "user2"
        assert passwords["test.com"]["password"] == "pass2"
        assert passwords["test.com"]["notes"] == "notes2"

    def test_get_password(
        self, temp_dir: Path, master_password: str, sample_passwords: dict[str, dict[str, Any]]
    ) -> None:
        """Test retrieving a password."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)
        storage.save_passwords(sample_passwords)

        # Get existing password
        data = storage.get_password("github.com")
        assert data is not None
        assert data["username"] == "testuser"
        assert data["password"] == "github_pass_123"
        assert data["notes"] == "Development account"

    def test_get_password_not_found(self, temp_dir: Path, master_password: str) -> None:
        """Test getting non-existent password."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        data = storage.get_password("nonexistent.com")
        assert data is None

    def test_delete_password(
        self, temp_dir: Path, master_password: str, sample_passwords: dict[str, dict[str, Any]]
    ) -> None:
        """Test deleting a password."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)
        storage.save_passwords(sample_passwords)

        # Delete password
        result = storage.delete_password("github.com")
        assert result is True

        # Verify deletion
        passwords = storage.load_passwords()
        assert "github.com" not in passwords
        assert "email.com" in passwords

    def test_delete_password_not_found(self, temp_dir: Path, master_password: str) -> None:
        """Test deleting non-existent password."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        result = storage.delete_password("nonexistent.com")
        assert result is False

    def test_list_services(
        self, temp_dir: Path, master_password: str, sample_passwords: dict[str, dict[str, Any]]
    ) -> None:
        """Test listing services."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)
        storage.save_passwords(sample_passwords)

        services = storage.list_services()
        assert services == ["email.com", "github.com"]  # Should be sorted

    def test_list_services_empty(self, temp_dir: Path, master_password: str) -> None:
        """Test listing services when none exist."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        services = storage.list_services()
        assert services == []

    def test_encryption_uses_random_iv(self, temp_dir: Path, master_password: str) -> None:
        """Test that encryption uses random IV for each operation."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        test_data = b"Same data"
        encrypted1 = storage._encrypt_data(test_data)
        encrypted2 = storage._encrypt_data(test_data)

        # Same data should produce different encrypted output due to random IV
        assert encrypted1 != encrypted2

        # But both should decrypt to same data
        assert storage._decrypt_data(encrypted1) == test_data
        assert storage._decrypt_data(encrypted2) == test_data

    def test_add_password_without_notes(self, temp_dir: Path, master_password: str) -> None:
        """Test adding password without notes."""
        storage = PasswordStorage(data_dir=temp_dir)
        storage.initialize_master_key(master_password)

        storage.add_password("test.com", "user", "pass")

        data = storage.get_password("test.com")
        assert data is not None
        assert data["notes"] == ""

    def test_cross_platform_paths(self, temp_dir: Path, master_password: str) -> None:
        """Test that paths work correctly (uses pathlib.Path)."""
        storage = PasswordStorage(data_dir=temp_dir)
        assert isinstance(storage.data_dir, Path)
        assert isinstance(storage.data_file, Path)

        storage.initialize_master_key(master_password)
        storage.add_password("test.com", "user", "pass")

        # Verify file was created with correct path
        assert storage.data_file.exists()
        assert storage.data_file.is_file()
