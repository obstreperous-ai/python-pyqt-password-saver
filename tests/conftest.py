"""Pytest configuration and shared fixtures for the Password Saver tests."""

import shutil
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def master_password() -> str:
    """Provide a test master password."""
    return "test_master_password_123"


@pytest.fixture
def sample_passwords() -> dict[str, dict[str, Any]]:
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
