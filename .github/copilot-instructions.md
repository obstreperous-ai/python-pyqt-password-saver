# Copilot Instructions for python-pyqt-password-saver

## Project Overview

This is a secure, cross-platform desktop password manager built with PyQt6 and Python 3.12. The application uses AES-256-CBC encryption to protect user passwords locally, with OS keyring integration for storing the encryption salt.

## Project Structure

```
python-pyqt-password-saver/
├── main.py              # Application entry point and GUI logic (PyQt6)
├── storage.py           # Encrypted storage and cryptography logic (AES-256)
├── ui/
│   └── mainwindow.ui   # PyQt6 UI definition file
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration and metadata
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
└── .github/
    └── workflows/      # CI/CD workflows (build, test, code-quality, security, release)
```

## Executable Commands

### Installation and Setup
```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running the Application
```bash
# Run the password manager GUI
python main.py
```

### Code Quality and Linting
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Format code with Black
black .

# Lint with Ruff (fast)
ruff check .

# Comprehensive linting with Pylint
pylint --rcfile=pyproject.toml .

# Type checking with MyPy
mypy --config-file=pyproject.toml --ignore-missing-imports --no-strict-optional .
```

### Security Scanning
```bash
# Security scanning with Bandit
bandit -r . -c pyproject.toml

# Check for dependency vulnerabilities
pip-audit --desc -r requirements.txt

# Detect secrets/credentials
detect-secrets scan --baseline .secrets.baseline
```

### Testing
```bash
# Run tests with pytest (Linux with display server)
xvfb-run -a pytest -v --tb=short

# Run tests with pytest (macOS)
pytest -v --tb=short
```

### Building
```bash
# Build distribution packages
python -m build --sdist --wheel .
```

## Code Style and Conventions

### Python Style
- **Target Version**: Python 3.12
- **Line Length**: 100 characters (enforced by Black)
- **Formatter**: Black (line-length: 100)
- **Linter**: Ruff (select: E, F, W, I, N, UP, B, A, C4, PT, SIM)
- **Type Checking**: MyPy with strict settings
- **Comprehensive Checks**: Pylint with custom configuration

### Type Hints
- Always use type hints for function parameters and return values
- Use modern Python 3.12 type syntax (e.g., `str | None` instead of `Optional[str]`)
- Example from codebase:
```python
def __init__(self, parent: QMainWindow | None = None):
    super().__init__(parent)
```

### Docstrings
- Use triple-quoted docstrings for modules, classes, and functions
- Follow this format:
```python
def initialize_master_key(self, password: str) -> None:
    """Initialize or retrieve the master encryption key.

    Args:
        password: Master password to derive encryption key from
    """
```

### Import Organization
- Standard library imports first
- Third-party imports second
- Local imports last
- Alphabetically sorted within each group
- Example from codebase:
```python
import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import Qt

from storage import PasswordStorage
```

### Naming Conventions
- Classes: PascalCase (e.g., `PasswordStorage`, `MasterPasswordDialog`)
- Functions/Methods: snake_case (e.g., `initialize_master_key`, `_setup_ui`)
- Constants: UPPER_SNAKE_CASE (e.g., `SERVICE_NAME`, `MASTER_KEY_ID`)
- Private methods: prefix with underscore (e.g., `_setup_ui`, `_master_key`)

### PyQt6 Specifics
- Use modern PyQt6 imports and patterns
- Prefer explicit enum values (e.g., `QLineEdit.EchoMode.Password`)
- Connect signals using `.connect()` method
- Example:
```python
self.password_input.returnPressed.connect(self.accept)
```

## Security Best Practices

### Critical Security Rules
1. **Never log or print passwords or encryption keys**
2. **Never store master password in plain text**
3. **Always use parameterized queries if SQL is added**
4. **Use secure random generation for salts and IVs**
5. **Never commit secrets to version control**

### Cryptography Standards
- **Encryption**: AES-256-CBC
- **Key Derivation**: PBKDF2HMAC with SHA256
- **Iterations**: 100,000 for PBKDF2
- **Storage**: Encrypted files in `~/.password_saver/`
- **Keyring**: Use OS keyring for salt storage when available, fallback to file

### Example from codebase:
```python
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend(),
)
```

## Testing Approach

### Current State
- The repository uses pytest for testing
- GUI tests require display server (Xvfb on Linux)
- Tests should be added to validate core functionality

### When Adding Tests
- Place test files in a `tests/` directory
- Name test files with `test_*.py` prefix
- Use pytest fixtures for setup/teardown
- Mock PyQt6 GUI components when possible
- Test encryption/decryption logic thoroughly
- Test keyring fallback behavior

### Example Test Structure
```python
import pytest
from storage import PasswordStorage

def test_password_storage_initialization():
    """Test that PasswordStorage initializes correctly."""
    storage = PasswordStorage()
    assert storage.data_dir.exists()
```

## Git Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- Feature branches: Create from `develop`, merge back via PR

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (e.g., "Add", "Fix", "Update", "Refactor")
- Keep first line under 72 characters
- Examples:
  - "Add password strength validation"
  - "Fix keyring fallback on Linux"
  - "Update encryption to use AES-256-GCM"

### Pull Requests
- All changes go through pull requests
- CI must pass before merging (build, test, code quality, security)
- Address pre-commit hook failures before pushing

## Boundaries and Restrictions

### Never Modify
- `.secrets.baseline` - managed by detect-secrets
- `.git/` directory
- Virtual environment directories (venv, .venv)
- Build artifacts (`dist/`, `build/`, `*.egg-info/`)

### Security Boundaries
- Do not add dependencies without checking for vulnerabilities with `pip-audit`
- Do not disable security tools (Bandit, detect-secrets)
- Do not weaken encryption parameters (key size, iterations)
- Do not add logging that could expose sensitive data

### Code Quality Standards
- Do not disable linting rules without justification
- Do not commit code that fails pre-commit hooks
- Do not ignore type checking errors without `# type: ignore` comment with explanation
- Do not add code that decreases test coverage (when tests exist)

## CI/CD Workflows

### Automated Checks
1. **Build and Test** (`build-test.yml`): Runs on push/PR to main/develop
   - Tests on Ubuntu and macOS
   - Validates PyQt6 compatibility
   - Builds distribution packages

2. **Code Quality** (`code-quality.yml`): Runs on push/PR
   - Black formatting check
   - Ruff linting
   - Pylint comprehensive checks
   - MyPy type checking
   - Bandit security scan

3. **Security** (`security.yml`): Runs on push/PR and weekly
   - pip-audit for dependency vulnerabilities
   - Bandit for code security issues
   - detect-secrets for credential leaks

4. **Release** (`release.yml`): Triggered on version tags
   - Creates GitHub releases
   - Builds platform-specific binaries

### Before Pushing Code
1. Run `pre-commit run --all-files` locally
2. Ensure all linters pass
3. Run tests if modifying core logic
4. Check that no secrets are being committed

## Dependencies

### Core Dependencies
- `PyQt6>=6.6.0` - GUI framework
- `cryptography>=41.0.0` - Encryption library
- `keyring>=24.0.0` - OS keyring integration

### Development Dependencies
- `black>=23.0.0` - Code formatter
- `ruff>=0.1.0` - Fast linter
- `mypy>=1.7.0` - Type checker
- `pylint>=3.0.0` - Comprehensive linter
- `pre-commit>=3.5.0` - Pre-commit hooks
- `bandit[toml]>=1.7.5` - Security scanner
- `pip-audit>=2.6.0` - Dependency vulnerability scanner

### Adding New Dependencies
1. Check for vulnerabilities: `pip-audit` on the new package
2. Add to `requirements.txt` (runtime) or `pyproject.toml` (dev)
3. Pin minimum version with `>=`
4. Update documentation if dependency adds new features

## Common Tasks

### Adding a New Feature
1. Create feature branch from `develop`
2. Implement feature with tests
3. Run `pre-commit run --all-files`
4. Ensure CI passes
5. Create PR to `develop`

### Fixing a Bug
1. Identify the bug location
2. Add test that reproduces the bug
3. Fix the bug
4. Verify test passes
5. Run linters and type checker
6. Create PR

### Updating Dependencies
1. Update version in `requirements.txt` or `pyproject.toml`
2. Run `pip-audit` to check for vulnerabilities
3. Test application still works
4. Update CI if needed
5. Document breaking changes

## Examples from Codebase

### Encryption Pattern
```python
# Generate random salt and IV
salt = os.urandom(16)
iv = os.urandom(16)

# Derive key from password
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend(),
)
key = kdf.derive(password.encode())

# Encrypt data
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
```

### PyQt6 Dialog Pattern
```python
class MasterPasswordDialog(QDialog):
    """Dialog for entering the master password."""

    def __init__(self, parent: QMainWindow | None = None):
        super().__init__(parent)
        self.setWindowTitle("Master Password")
        self.setModal(True)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the dialog UI."""
        layout = QVBoxLayout()
        # Add widgets to layout
```

### Keyring with Fallback Pattern
```python
try:
    stored_salt = keyring.get_password(self.SERVICE_NAME, "salt")
except (KeyringError, RuntimeError):
    stored_salt = None

if stored_salt is None:
    # Fallback to file-based storage
    if salt_file.exists():
        with open(salt_file, "rb") as f:
            salt = f.read()
```

## Questions and Clarifications

If you encounter:
- **Unclear requirements**: Ask for clarification before implementing
- **Breaking changes**: Document impact and get approval
- **Security concerns**: Raise them immediately
- **Architecture decisions**: Discuss trade-offs before proceeding
- **Test failures**: Investigate root cause before making changes

## Additional Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [cryptography Library Docs](https://cryptography.io/en/latest/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html)
