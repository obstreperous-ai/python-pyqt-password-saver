"""Pytest configuration and shared fixtures for the Password Saver tests."""

import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def master_password():
    """Provide a test master password."""
    return "test_master_password_123"


@pytest.fixture
def sample_passwords():
    """Provide sample password data for testing."""
    return {
        "github.com": {
            "username": "testuser",
            "password": "github_pass_123",
            "notes": "Development account",
        },
        "email.com": {
            "username": "user@example.com",
            "password": "email_pass_456",
            "notes": "Personal email",
        },
    }
