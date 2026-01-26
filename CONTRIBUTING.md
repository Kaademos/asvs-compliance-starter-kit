# Contributing to the ASVS Compliance Engine

Thank you for your interest in contributing! This project thrives on community involvement, and every contribution helps make application security more accessible. Whether you're fixing a typo, adding a secure coding pattern, or building new features, your input is valuable.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.

## Ways to Contribute

### Good First Issues

New to the project? Look for issues labeled:
- `good first issue` - Well-defined, beginner-friendly tasks
- `help wanted` - Tasks where we need community help
- `documentation` - Improve guides, examples, and comments

### High-Impact Contributions

- **Framework Adapters:** Add evidence patterns for Django, FastAPI, Express, Spring Boot
- **Language Guides:** Create secure coding guides in `02-Implementation-Guidance/Languages/`
- **IaC Scanners:** Extend scanning to AWS CDK, Azure Bicep, Pulumi
- **DAST Checks:** Add new security verification checks to the verification suite

### Bug Reports

Found a bug? [Open an issue](https://github.com/kaademos/asvs-compliance-starter-kit/issues/new) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Relevant error messages or logs

### Feature Requests

Have an idea? [Open an issue](https://github.com/kaademos/asvs-compliance-starter-kit/issues/new) describing:
- The problem you're trying to solve
- Your proposed solution
- Alternative approaches considered
- How it benefits other users

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- (Optional) Docker for container testing

### Local Installation

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/asvs-compliance-starter-kit.git
cd asvs-compliance-starter-kit

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install in development mode with all dependencies
pip install -e ".[dev,evidence,verification]"

# 4. Verify installation
asvs --version
python -m pytest tests/ -v
```

### Running the CLI Locally

```bash
# All commands work immediately after installation
asvs --help
asvs verify --level 1
asvs resources --status
```

### Docker Development

```bash
# Build the development image
docker build -t asvs-engine:dev .

# Run tests in container
docker run -v $(pwd):/app asvs-engine:dev pytest tests/ -v
```

## Project Structure

```
asvs-compliance-starter-kit/
├── tools/                          # CLI source code (main development area)
│   ├── cli.py                      # Unified CLI entry point
│   ├── compliance_gate.py          # Documentation & evidence verification
│   ├── verification_suite.py       # DAST scanner
│   ├── iac_scanner.py              # Terraform scanner
│   ├── export_requirements.py      # CSV/Jira export
│   ├── drift_detector.py           # ASVS standard drift detection
│   ├── resource_manager.py         # Template download manager
│   ├── init_project.py             # Project initialization
│   └── generate_report.py          # HTML report generator
├── tests/                          # Test suite (pytest)
│   ├── test_cli.py
│   ├── test_compliance_gate.py
│   └── ...
├── 00-Documentation-Standards/     # Decision templates
├── 01-ASVS-Core-Reference/         # ASVS 5.0 JSON/CSV data
├── 02-Implementation-Guidance/     # Secure coding patterns
├── policies/                       # OPA/Rego policies
├── docs/                           # User documentation
├── pyproject.toml                  # Package configuration
└── Makefile                        # Common development commands
```

### Key Files for Contributors

| File | Purpose |
|------|---------|
| `tools/cli.py` | Add new commands here |
| `tools/compliance_gate.py` | Evidence verification logic |
| `tools/verification_suite.py` | DAST checks (headers, cookies, CSRF) |
| `tools/resource_manager.py` | Template download and caching |
| `evidence.example.yml` | Example evidence patterns |
| `pyproject.toml` | Dependencies and package metadata |

## Pull Request Process

### 1. Create a Branch

```bash
# Sync with upstream
git checkout main
git pull origin main

# Create a feature branch
git checkout -b feat/your-feature-name
# or: git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clear, focused commits
- Follow the coding standards below
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: <type>(<scope>): <description>

# Examples:
git commit -m "feat(cli): add resources command for template management"
git commit -m "fix(verify): handle missing evidence.yml gracefully"
git commit -m "docs: update CLI reference in README"
git commit -m "test(export): add tests for Jira JSON export"
```

**Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`

### 4. Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=tools --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_cli.py -v
```

### 5. Submit PR

- Push your branch: `git push origin feat/your-feature-name`
- Open a Pull Request against `main`
- Fill out the PR template completely
- Link related issues using `Fixes #123` or `Closes #456`

### 6. Code Review

- Address reviewer feedback promptly
- Keep discussions constructive
- Squash commits if requested

## Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use descriptive variable and function names

```python
# Good
def verify_evidence_manifest(
    manifest_path: Path,
    base_path: Path,
    strict: bool = False
) -> tuple[bool, list[str]]:
    """
    Verify all evidence checks in a manifest file.
    
    Args:
        manifest_path: Path to evidence.yml
        base_path: Root directory for relative paths
        strict: If True, fail on warnings
        
    Returns:
        Tuple of (success, list of error messages)
    """
    ...

# Avoid
def verify(p, b, s=False):
    ...
```

### CLI Design Principles

- Use consistent option names across commands
- Provide sensible defaults
- Support both `--json` and human-readable output
- Include helpful error messages with remediation steps

```python
# Good error message
raise FileNotFoundError(
    f"Evidence manifest not found: {path}. "
    "Create one with 'asvs init' or see evidence.example.yml"
)

# Avoid
raise FileNotFoundError("File not found")
```

### Security Considerations

- Never log sensitive information (paths, credentials, tokens)
- Sanitize error messages that could expose internal details
- Validate all user inputs
- Use `--allow-local` pattern for features that bypass security controls

## Testing

### Test Structure

```python
# tests/test_your_feature.py

import pytest
from tools.your_module import YourClass

class TestYourFeature:
    """Tests for YourClass functionality."""
    
    def test_basic_functionality(self):
        """Test the happy path."""
        result = YourClass().do_thing()
        assert result.success is True
    
    def test_handles_missing_input(self):
        """Test error handling for missing input."""
        with pytest.raises(ValueError, match="Input required"):
            YourClass().do_thing(None)
    
    def test_edge_case(self, tmp_path):
        """Test edge case with temporary directory."""
        test_file = tmp_path / "test.yml"
        test_file.write_text("key: value")
        # ...
```

### Test Requirements

- All new features must have tests
- Bug fixes should include regression tests
- Maintain >80% code coverage for `tools/`
- Use `pytest` fixtures for common setup

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test class
pytest tests/test_cli.py::TestVerifyCommand -v

# With coverage report
pytest tests/ --cov=tools --cov-report=html
open htmlcov/index.html
```

## Documentation

### Where to Document

| Change Type | Documentation Location |
|-------------|----------------------|
| New CLI command | `README.md` CLI Reference section |
| New option | `docs/user-guide.md` |
| Configuration changes | `docs/configuration.md` |
| Common errors | `docs/troubleshooting.md` |
| API changes | Docstrings in source code |

### Documentation Style

- Use clear, concise language
- Include code examples for all features
- Show expected output where helpful
- Link to related documentation

### Docstring Format

```python
def function_name(arg1: str, arg2: int = 10) -> bool:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the purpose,
    algorithm, or important details.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2 (default: 10)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When arg1 is empty
        FileNotFoundError: When referenced file doesn't exist
        
    Example:
        >>> function_name("hello", 5)
        True
    """
```

## Recognition

Contributors are recognized in:
- Git commit history
- Release notes for significant contributions
- [ADOPTERS.md](ADOPTERS.md) Ambassador program

## Getting Help

- **Questions:** Open a [Discussion](https://github.com/kaademos/asvs-compliance-starter-kit/discussions)
- **Bugs:** Open an [Issue](https://github.com/kaademos/asvs-compliance-starter-kit/issues)
- **Security Issues:** See [SECURITY.md](SECURITY.md) for responsible disclosure

---

Thank you for contributing to the ASVS Compliance Engine!
