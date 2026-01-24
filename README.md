# python-pyqt-password-saver

A secure, cross-platform desktop password manager built with PyQt6 and Python 3.12.

## Features

- 🔐 **AES-256 Encryption**: All passwords are encrypted using industry-standard AES-256-CBC encryption
- 🔑 **Master Password**: Single master password to access your password vault
- 💾 **Local Storage**: Passwords stored locally in encrypted format
- 🖥️ **Cross-Platform**: Works on macOS and Linux
- 🔒 **OS Keyring Integration**: Uses OS secure storage when available, with file-based fallback
- 🎨 **User-Friendly GUI**: Clean PyQt6 interface for easy password management

## Requirements

- Python 3.12 or higher
- PyQt6
- cryptography library
- keyring library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/obstreperous-ai/python-pyqt-password-saver.git
cd python-pyqt-password-saver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

On first launch, you'll be prompted to create a master password. This password will be used to encrypt and decrypt your password vault.

### Adding a Password

1. Click "Add Password" button
2. Enter the service name (e.g., "github.com")
3. Enter your username
4. Enter your password
5. Optionally add notes
6. Click "Save"

### Viewing a Password

1. Select a service from the list
2. Click "View Password" or double-click the service
3. Click "Show" to reveal the password
4. Password is copyable for easy use

### Deleting a Password

1. Select a service from the list
2. Click "Delete Password"
3. Confirm deletion

## Project Structure

```
python-pyqt-password-saver/
├── password_saver/          # Main package directory
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Application entry point and GUI logic
│   ├── storage.py          # Encrypted storage and cryptography logic
│   └── ui/
│       └── mainwindow.ui   # PyQt6 UI definition file
├── tests/                   # Test suite
│   ├── conftest.py         # Pytest fixtures and configuration
│   ├── test_main.py        # Tests for main module
│   └── test_storage.py     # Tests for storage module
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration and metadata
├── README.md               # This file
└── LICENSE                 # Apache 2.0 License
```

## Security

- Passwords are encrypted using AES-256-CBC with PBKDF2 key derivation
- 100,000 PBKDF2 iterations for key strengthening
- Random salt and IV for each encryption operation
- Master password never stored, only derived key
- Salt stored in OS keyring when available, otherwise in `.password_saver/.salt`
- Encrypted passwords stored in `~/.password_saver/passwords.enc`

## Development

### Configuration

Project uses `pyproject.toml` for configuration with support for:
- Black code formatter (line-length: 100)
- Ruff linter (Python 3.12 target)
- mypy type checker (strict settings)
- Pylint (comprehensive code quality checks)
- Bandit (security linter)

### Setting Up Development Environment

1. Install the package with development dependencies:
```bash
pip install -e ".[dev]"
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

This will automatically run code quality checks before each commit.

### Code Quality Tools

#### Pre-commit Hooks

Pre-commit hooks are configured in `.pre-commit-config.yaml` and automatically run on each commit:

- **black**: Code formatting
- **ruff**: Fast linting with auto-fix
- **pylint**: Comprehensive code quality checks
- **mypy**: Type checking
- **bandit**: Security scanning
- **detect-secrets**: Credential detection
- **Standard hooks**: Whitespace, YAML/TOML validation, large files

Run manually on all files:
```bash
pre-commit run --all-files
```

#### Manual Testing

Run individual tools:
```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Comprehensive linting with Pylint
pylint --rcfile=pyproject.toml .

# Type checking with MyPy
mypy --config-file=pyproject.toml .

# Security scanning
bandit -r . -c pyproject.toml

# Check for dependency vulnerabilities
pip-audit --desc -r requirements.txt
```

### Testing

Run tests with pytest:
```bash
# Run all tests (Linux with display server)
xvfb-run -a pytest -v --tb=short

# Run all tests (macOS)
pytest -v --tb=short

# Run tests with coverage report
xvfb-run -a pytest --cov=password_saver --cov-report=term --cov-report=html

# View coverage report
# Open htmlcov/index.html in a browser
```

Current test coverage: **97% for storage module**, **63% overall** (GUI testing is limited)

### Dependencies

Core dependencies:
- `PyQt6>=6.6.0` - GUI framework
- `cryptography>=41.0.0` - Encryption library
- `keyring>=24.0.0` - OS keyring integration

### CI/CD Workflows

This project uses GitHub Actions for continuous integration and deployment:

#### Build and Test (`build-test.yml`)
- Runs on: Push and Pull Requests to `main` and `develop`
- Platforms: Ubuntu and macOS
- Features:
  - Cross-platform PyQt6 compatibility testing
  - Platform-specific system dependencies
  - Headless GUI testing with Xvfb on Linux
  - Package build validation

#### Code Quality (`code-quality.yml`)
- Runs on: Push and Pull Requests
- Tools:
  - **Black**: Code formatting validation
  - **Ruff**: Fast Python linting
  - **Pylint**: Comprehensive code quality checks
  - **MyPy**: Type checking
  - **Bandit**: Security linting
  - **pre-commit**: Runs all configured hooks
- Ensures code formatting, quality, type safety, and basic security

#### Security Scanning (`security.yml`)
- Runs on: Push, Pull Requests, and weekly schedule
- Tools:
  - **pip-audit**: Scans dependencies for known vulnerabilities (CVEs)
  - **Bandit**: Static security analysis for Python code
  - **detect-secrets**: Prevents committing secrets/credentials
- Generates JSON reports uploaded as artifacts
- Checks for vulnerabilities and security issues in code and dependencies

#### Release (`release.yml`)
- Triggers on: Version tags (e.g., `v0.1.1`)
- Creates:
  - Python packages (wheel and source)
  - Platform-specific binaries (macOS, Linux)
  - GitHub Release with all artifacts

## License

Apache License 2.0 - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
