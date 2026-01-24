# Copilot Instructions for python-pyqt-password-saver

## Critical Rules for CoPilot

**READ THIS FIRST - These rules are mandatory:**

1. **ALWAYS follow Test-Driven Development (TDD)**
   - Write tests BEFORE implementation code
   - Run tests to verify they fail
   - Implement minimal code to pass tests
   - Never skip writing tests

2. **ALWAYS verify builds succeed**
   - Run `python -m build --sdist --wheel .` before committing
   - Fix any build errors immediately
   - Never commit code that doesn't build

3. **ALWAYS run formatters before committing**
   - Run `black .` to format all Python files
   - Run `ruff check . --fix` to fix linting issues
   - Accept formatter changes without question

4. **ALWAYS run all tests before committing**
   - Run `xvfb-run -a pytest -v` (Linux) or `pytest -v` (macOS)
   - All tests must pass before committing
   - Fix failing tests, do not skip or disable them

5. **ALWAYS run pre-commit hooks before committing**
   - Run `pre-commit run --all-files`
   - Fix all issues reported by hooks
   - Do not commit if hooks fail

6. **Follow the mandatory workflow** (see "Mandatory Pre-Commit Workflow" section)
   - Complete all 10 steps in order
   - Do not skip any steps
   - Fix issues at each step before proceeding

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
# Run the password manager GUI (development)
python main.py

# Or use the installed command (after pip install)
password-saver
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
# Note: pytest tests are not yet implemented in the repository
# When tests are added, use these commands:

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

### Test-Driven Development (TDD) Workflow

**ALWAYS follow TDD when adding new features or fixing bugs:**

1. **Write the test first** - Before writing any implementation code
   - Create test file in `tests/` directory with `test_*.py` prefix
   - Write failing test(s) that define the expected behavior
   - Run the test to confirm it fails for the right reason

2. **Implement minimal code** - Write just enough code to make the test pass
   - Focus on making the test pass, not on perfect code
   - Avoid over-engineering or adding extra features

3. **Refactor** - Improve the code while keeping tests green
   - Clean up implementation
   - Ensure all tests still pass
   - Run formatters and linters

**Example TDD Workflow:**
```bash
# 1. Write test first (it should fail)
# Create tests/test_new_feature.py with your test

# 2. Run the test to see it fail
xvfb-run -a pytest tests/test_new_feature.py -v

# 3. Implement minimal code to make test pass
# Edit your implementation files

# 4. Run test again to verify it passes
xvfb-run -a pytest tests/test_new_feature.py -v

# 5. Run all tests to ensure no regressions
xvfb-run -a pytest -v

# 6. Format and lint your code
black .
ruff check . --fix
pylint --rcfile=pyproject.toml .

# 7. Commit your changes
git add .
git commit -m "Add new feature with tests"
```

### When Adding Tests
- Place test files in a `tests/` directory
- Name test files with `test_*.py` prefix
- Use pytest fixtures for setup/teardown (see `tests/conftest.py`)
- Mock PyQt6 GUI components when possible to avoid GUI dependencies
- Test encryption/decryption logic thoroughly
- Test keyring fallback behavior
- Use descriptive test names that explain what is being tested
- Add docstrings to test functions explaining the test scenario

### PyQt6 Testing Best Practices
- Use `pytest-qt` plugin for Qt-specific testing features
- Test GUI logic separately from business logic when possible
- Use signals/slots for testable GUI interactions
- Mock QApplication when testing non-GUI components
- Use Xvfb on Linux for headless GUI testing
- Test dialogs by simulating button clicks and input
- Verify signal emissions with `qtbot.waitSignal()`

### PyQt6 TDD Example Pattern

**Example: Adding a password strength indicator to the GUI**

1. **Write test first:**
```python
# tests/test_password_strength.py
import pytest
from PyQt6.QtWidgets import QApplication
from main import PasswordStrengthWidget

def test_password_strength_weak(qtbot):
    """Test that weak password shows red indicator."""
    widget = PasswordStrengthWidget()
    qtbot.addWidget(widget)
    
    widget.set_password("123")
    assert widget.get_strength() == "weak"
    assert widget.get_color() == "red"

def test_password_strength_strong(qtbot):
    """Test that strong password shows green indicator."""
    widget = PasswordStrengthWidget()
    qtbot.addWidget(widget)
    
    widget.set_password("MyStr0ng!P@ssw0rd")
    assert widget.get_strength() == "strong"
    assert widget.get_color() == "green"
```

2. **Run test to see it fail:**
```bash
xvfb-run -a pytest tests/test_password_strength.py -v
# Should fail because PasswordStrengthWidget doesn't exist yet
```

3. **Implement minimal code:**
```python
# main.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PasswordStrengthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._strength = "weak"
        self._color = "red"
        
    def set_password(self, password: str) -> None:
        # Check password strength based on multiple criteria
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if len(password) < 8:
            self._strength = "weak"
            self._color = "red"
        elif has_upper and has_digit and has_special:
            self._strength = "strong"
            self._color = "green"
        else:
            self._strength = "medium"
            self._color = "yellow"
    
    def get_strength(self) -> str:
        return self._strength
    
    def get_color(self) -> str:
        return self._color
```

4. **Run test to verify it passes:**
```bash
xvfb-run -a pytest tests/test_password_strength.py -v
```

5. **Refactor and add GUI integration:**
```python
# Now add visual elements, layout, etc.
# Run tests again to ensure nothing broke
```

### Testing Storage/Encryption (Non-GUI Example)

**Example: Adding password export feature**

1. **Write test first:**
```python
# tests/test_export.py
import json
from pathlib import Path
from storage import PasswordStorage

def test_export_passwords_to_json(temp_dir, master_password):
    """Test exporting passwords to JSON file."""
    storage = PasswordStorage(data_dir=temp_dir)
    storage.initialize_master_key(master_password)
    storage.add_password("test.com", "user", "pass", "notes")
    
    export_file = temp_dir / "export.json"
    storage.export_to_json(export_file)
    
    assert export_file.exists()
    with open(export_file) as f:
        data = json.load(f)
    assert "test.com" in data
    assert data["test.com"]["username"] == "user"
```

2. **Run to see it fail:**
```bash
xvfb-run -a pytest tests/test_export.py -v
# Fails: AttributeError: 'PasswordStorage' object has no attribute 'export_to_json'
```

3. **Implement:**
```python
# storage.py
def export_to_json(self, export_file: Path) -> None:
    """Export passwords to JSON file.
    
    WARNING: This exports passwords in PLAIN TEXT. The exported file
    is not encrypted and should be handled with extreme caution.
    Only use this for backup purposes and delete the file immediately
    after importing to a secure location.
    """
    passwords = self.load_passwords()
    with open(export_file, 'w') as f:
        json.dump(passwords, f, indent=2)
```

4. **Verify test passes:**
```bash
xvfb-run -a pytest tests/test_export.py -v
```

### Example Test Structure
```python
import pytest
from storage import PasswordStorage

def test_password_storage_initialization():
    """Test that PasswordStorage initializes correctly."""
    storage = PasswordStorage()
    assert storage.data_dir.exists()

def test_password_storage_with_custom_dir(temp_dir):
    """Test initialization with custom directory using fixture."""
    storage = PasswordStorage(data_dir=temp_dir)
    assert storage.data_dir == temp_dir
    assert temp_dir.exists()
```

### Test Coverage Goals
- Aim for high coverage of business logic (storage, encryption)
- Cover edge cases and error conditions
- Test with invalid inputs
- Verify error messages are user-friendly

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

### Mandatory Pre-Commit Workflow

**ALWAYS follow this workflow before committing any code changes:**

```bash
# 1. Verify the project builds successfully
python -m build --sdist --wheel .

# 2. Run ALL tests to ensure nothing is broken
xvfb-run -a pytest -v --tb=short

# 3. Format code with Black (this modifies files)
black .

# 4. Fix linting issues with Ruff
ruff check . --fix

# 5. Run comprehensive linting checks
pylint --rcfile=pyproject.toml .

# 6. Run type checking
mypy --config-file=pyproject.toml --ignore-missing-imports --no-strict-optional .

# 7. Run security scanning
bandit -r . -c pyproject.toml

# 8. Run all pre-commit hooks
pre-commit run --all-files

# 9. Check git status - only expected files should be modified
git status

# 10. Stage and commit changes
git add .
git commit -m "Your commit message"
```

**CRITICAL RULES:**
- **NEVER commit without running the full workflow above**
- **NEVER disable linting rules without justification**
- **NEVER skip tests - all tests must pass before committing**
- **ALWAYS run Black formatter before committing (fixes formatting automatically)**
- **ALWAYS verify build succeeds before committing**
- If any step fails, fix the issues before proceeding to the next step
- If tests fail, fix the code or tests - do not skip
- If formatters change files, review the changes before committing

### Quick Pre-Commit Check
For faster feedback during development:
```bash
# Run this after each small change
black . && ruff check . --fix && xvfb-run -a pytest -v
```

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
- `pytest>=7.0.0` - Testing framework (for future test implementation)
- `pytest-qt` - PyQt6 testing support (for future test implementation)
- `pytest-xvfb` - Headless testing on Linux (for future test implementation)

### Adding New Dependencies
1. Check for vulnerabilities: `pip-audit` on the new package
2. Add to `requirements.txt` (runtime) or `pyproject.toml` (dev)
3. Pin minimum version with `>=`
4. Update documentation if dependency adds new features

## Common Tasks

### Adding a New Feature (TDD Approach)
**Follow this workflow strictly:**

1. **Write tests first (TDD)**
   ```bash
   # Create test file
   touch tests/test_new_feature.py
   # Write failing tests that define expected behavior
   # Edit tests/test_new_feature.py
   ```

2. **Run tests to see them fail**
   ```bash
   xvfb-run -a pytest tests/test_new_feature.py -v
   # Verify tests fail for the right reason
   ```

3. **Implement minimal code**
   ```bash
   # Edit implementation files
   # Write just enough code to make tests pass
   ```

4. **Run tests to verify they pass**
   ```bash
   xvfb-run -a pytest tests/test_new_feature.py -v
   ```

5. **Run all tests to ensure no regressions**
   ```bash
   xvfb-run -a pytest -v
   ```

6. **Build the project to ensure it still builds**
   ```bash
   python -m build --sdist --wheel .
   ```

7. **Format and lint your code**
   ```bash
   black .
   ruff check . --fix
   pylint --rcfile=pyproject.toml .
   mypy --config-file=pyproject.toml --ignore-missing-imports --no-strict-optional .
   ```

8. **Run pre-commit hooks**
   ```bash
   pre-commit run --all-files
   ```

9. **Review and commit**
   ```bash
   git status
   git add .
   git commit -m "Add feature: <description>"
   ```

10. **Create PR to `develop`**

### Fixing a Bug (TDD Approach)
**Follow this workflow strictly:**

1. **Identify the bug location**
   - Reproduce the bug
   - Locate the faulty code

2. **Write a test that reproduces the bug**
   ```bash
   # Add test to appropriate test file or create new one
   # The test should FAIL before the fix
   xvfb-run -a pytest tests/test_bug.py -v
   ```

3. **Fix the bug with minimal changes**
   - Edit only the necessary code
   - Keep changes surgical and focused

4. **Verify the test now passes**
   ```bash
   xvfb-run -a pytest tests/test_bug.py -v
   ```

5. **Run all tests to ensure no regressions**
   ```bash
   xvfb-run -a pytest -v
   ```

6. **Build and verify**
   ```bash
   python -m build --sdist --wheel .
   ```

7. **Run formatters and linters**
   ```bash
   black .
   ruff check . --fix
   pylint --rcfile=pyproject.toml .
   mypy --config-file=pyproject.toml --ignore-missing-imports --no-strict-optional .
   ```

8. **Run pre-commit hooks**
   ```bash
   pre-commit run --all-files
   ```

9. **Commit and create PR**
   ```bash
   git add .
   git commit -m "Fix: <bug description>"
   ```

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

## Troubleshooting Common Issues

### Build Failures
**Problem**: `python -m build` fails
```bash
# Check for syntax errors
python -m py_compile main.py storage.py

# Check pyproject.toml is valid
python -c "import tomllib; with open('pyproject.toml', 'rb') as f: tomllib.load(f)"

# Ensure all dependencies are installed
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Test Failures
**Problem**: Tests fail on Linux but work locally
```bash
# Ensure you're using xvfb for GUI tests on Linux
xvfb-run -a pytest -v

# Check if Qt platform plugin is available
export QT_DEBUG_PLUGINS=1
xvfb-run -a python -c "from PyQt6.QtWidgets import QApplication; import sys; app = QApplication(sys.argv)"
```

**Problem**: Tests pass locally but fail in CI
- Verify you're testing in the same environment (Python 3.12)
- Check CI logs for specific error messages
- Ensure all test dependencies are in pyproject.toml dev extras

### Formatter/Linter Failures
**Problem**: Black makes changes but you're not sure if they're correct
```bash
# Black formatting is ALWAYS correct - accept the changes
black .
git diff  # Review what changed
git add .  # Accept the formatted code
```

**Problem**: Ruff reports errors you don't understand
```bash
# Get detailed explanation of a rule
ruff rule <RULE_CODE>

# Example: explain E501 (line too long)
ruff rule E501

# Fix automatically when possible
ruff check . --fix
```

**Problem**: Pylint reports false positives for PyQt6 code
```bash
# PyQt6 modules are already ignored in pyproject.toml
# If you get false positives, check [tool.pylint.typecheck] section
# Add specific ignores only if absolutely necessary
```

**Problem**: MyPy type checking errors
```bash
# Specific PyQt6 modules can have type issues
# Use `# type: ignore` with explanation only when necessary
# Example:
self.ui = uic.loadUi("mainwindow.ui", self)  # type: ignore[misc]
```

### Pre-commit Hook Failures
**Problem**: Pre-commit hooks fail
```bash
# Update hooks to latest version
pre-commit autoupdate

# Clear cache and retry
pre-commit clean
pre-commit run --all-files

# If a specific hook fails, run it manually to debug
black .
ruff check .
pylint --rcfile=pyproject.toml .
```

### Import Errors
**Problem**: Cannot import PyQt6 or other dependencies
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
pip install -e ".[dev]"

# Verify PyQt6 is installed
python -c "from PyQt6 import QtCore; print(QtCore.PYQT_VERSION_STR)"
```

### Performance Issues
**Problem**: Tests or builds are too slow
```bash
# Run specific test file instead of all tests during development
xvfb-run -a pytest tests/test_storage.py -v

# Use pytest markers to run subsets of tests
pytest -v -m "not slow"

# Skip security scans during development (but run before committing)
# Just run: black . && ruff check . --fix && pytest -v
```

## Additional Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [cryptography Library Docs](https://cryptography.io/en/latest/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [pytest-qt Documentation](https://pytest-qt.readthedocs.io/)

## Summary: CoPilot Success Checklist

Every time you make a code change, verify:

✅ **Tests written first** (TDD)
- [ ] Tests exist for new functionality
- [ ] Tests initially failed
- [ ] Tests now pass

✅ **Build succeeds**
- [ ] `python -m build --sdist --wheel .` completes successfully

✅ **All tests pass**
- [ ] `xvfb-run -a pytest -v` (Linux) or `pytest -v` (macOS) shows all green

✅ **Code formatted**
- [ ] `black .` has been run
- [ ] `ruff check . --fix` has been run

✅ **Code quality checks pass**
- [ ] `pylint --rcfile=pyproject.toml .` passes
- [ ] `mypy --config-file=pyproject.toml --ignore-missing-imports --no-strict-optional .` passes
- [ ] `bandit -r . -c pyproject.toml` passes

✅ **Pre-commit hooks pass**
- [ ] `pre-commit run --all-files` succeeds

✅ **Git status clean**
- [ ] Only expected files are modified
- [ ] No build artifacts, temp files, or __pycache__ in commit

✅ **Ready to commit**
- [ ] Changes are minimal and focused
- [ ] Commit message is clear and descriptive

**If ANY checkbox is unchecked, DO NOT COMMIT. Fix the issue first.**
