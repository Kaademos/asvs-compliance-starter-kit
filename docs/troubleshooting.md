# Troubleshooting Guide

Solutions for common issues with the ASVS Compliance Engine.

## Table of Contents

- [Installation Issues](#installation-issues)
- [CLI Errors](#cli-errors)
- [Verification Failures](#verification-failures)
- [Resource & Template Issues](#resource--template-issues)
- [DAST Scanner Issues](#dast-scanner-issues)
- [Docker Issues](#docker-issues)
- [CI/CD Issues](#cicd-issues)
- [Getting Help](#getting-help)

---

## Installation Issues

### `pip install` fails with version conflict

**Symptom:**
```
ERROR: Cannot install asvs-compliance-tools because these package versions have conflicting dependencies.
```

**Solution:**

Create a fresh virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install asvs-compliance-tools
```

### Command `asvs` not found after installation

**Symptom:**
```bash
$ asvs --version
command not found: asvs
```

**Solutions:**

1. **Check installation location:**
   ```bash
   pip show asvs-compliance-tools
   # Look for "Location:" to see where it's installed
   ```

2. **Ensure scripts directory is in PATH:**
   ```bash
   # Find where pip installs scripts
   python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
   
   # Add to PATH if needed
   export PATH="$PATH:$(python -c 'import sysconfig; print(sysconfig.get_path(\"scripts\"))')"
   ```

3. **Use module directly:**
   ```bash
   python -m tools.cli --version
   ```

### Version shows old number after upgrade

**Symptom:**
```bash
$ pip install --upgrade asvs-compliance-tools
$ asvs --version
asvs 2.1.0  # Expected 2.2.0
```

**Solution:**

The package metadata may be cached. Reinstall completely:

```bash
pip uninstall asvs-compliance-tools
pip cache purge
pip install asvs-compliance-tools
asvs --version
```

---

## CLI Errors

### `ModuleNotFoundError: No module named 'tools'`

**Symptom:**
```
ModuleNotFoundError: No module named 'tools'
```

**Cause:** Running scripts directly instead of using the CLI or module syntax.

**Solutions:**

1. **Use the CLI:**
   ```bash
   asvs verify --level 2
   ```

2. **Use module syntax:**
   ```bash
   python -m tools.compliance_gate --level 2
   ```

3. **Install in development mode (if working from repo):**
   ```bash
   pip install -e .
   ```

### `Error: {e}` with no details

**Symptom:** Generic error message without useful information.

**Solution:**

Run with Python's verbose flag:

```bash
python -v -m tools.cli verify --level 2 2>&1 | tail -50
```

Or check for import errors:

```bash
python -c "from tools import cli; cli.main(['--help'])"
```

---

## Verification Failures

### Documents not found (auto-detection fails)

**Symptom:**
```
ASVS Compliance Gate - Level 2
Documents checked: 0
Documents valid: 0
Status: FAILED

Errors:
  - Documents path not found: docs
```

**Solutions:**

1. **Specify docs path explicitly:**
   ```bash
   asvs verify --docs-path ./my-security-docs --level 2
   ```

2. **Check your directory structure:**
   ```bash
   ls -la docs/
   ls -la 03-Product-Specific-Files/
   ```

3. **Create docs with init:**
   ```bash
   asvs init
   ```

### Evidence checks failing

**Symptom:**
```
Automated Evidence Verification
==============================
  ✗ [V6.2.1] content_match: requirements.txt
      Pattern 'bcrypt' NOT found in requirements.txt
```

**Solutions:**

1. **Verify file exists:**
   ```bash
   ls -la requirements.txt
   cat requirements.txt | grep -i bcrypt
   ```

2. **Check pattern syntax:**
   ```yaml
   # Correct regex escaping
   pattern: "bcrypt|argon2"  # Good
   pattern: "bcrypt\|argon2"  # May fail depending on YAML parser
   ```

3. **Test pattern manually:**
   ```bash
   grep -E "bcrypt|argon2" requirements.txt
   ```

4. **Check file path is relative to project root:**
   ```yaml
   # Relative to where you run the command
   path: "requirements.txt"        # Root level
   path: "src/requirements.txt"    # Subdirectory
   ```

### Placeholder text detected

**Symptom:**
```
  ✗ V11-Cryptography-Strategy.md
      - Contains placeholders: ['[Project Name]', '[e.g.,']
```

**Solution:**

Edit the document and replace all placeholder text:

```bash
# Find placeholders
grep -n "\[Project Name\]" docs/V11-Cryptography-Strategy.md
grep -n "\[e.g.," docs/V11-Cryptography-Strategy.md

# Edit and replace with actual content
```

---

## Resource & Template Issues

### Templates unavailable

**Symptom:**
```
Initializing MyProject at docs (Level 2)...
  Warning: Templates unavailable. Documentation not created.
  Visit https://github.com/Kaademos/asvs-compliance-starter-kit for manual setup.
```

**Solutions:**

1. **Download resources:**
   ```bash
   asvs resources --download
   ```

2. **Check cache status:**
   ```bash
   asvs resources --status
   ```

3. **Clear and re-download:**
   ```bash
   asvs resources --clear
   asvs resources --download
   ```

### Download fails (network/proxy)

**Symptom:**
```
  [FAILED] V6-Authentication-Strategy.md
    Error: Failed to download: V6-Authentication-Strategy.md
```

**Solutions:**

1. **Check network connectivity:**
   ```bash
   curl -I https://raw.githubusercontent.com/Kaademos/asvs-compliance-starter-kit/main/README.md
   ```

2. **Use proxy if required:**
   ```bash
   export HTTPS_PROXY=http://proxy.example.com:8080
   asvs resources --download
   ```

3. **Clone repository instead:**
   ```bash
   git clone https://github.com/Kaademos/asvs-compliance-starter-kit.git
   cd asvs-compliance-starter-kit
   pip install -e .
   ```

### Source file not found for export

**Symptom:**
```
Error: Source file not found: ASVS-L2-Standard.json.
Run 'asvs resources --download' to fetch required files.
```

**Solution:**
```bash
asvs resources --download --yes
asvs export --level 2
```

---

## DAST Scanner Issues

### SSRF Protection blocking scan

**Symptom:**
```
Error: Invalid URL: http://localhost:3000
Security Warning: Target resolves to restricted IP 127.0.0.1
```

**Solution:**

Use the `--allow-local` flag for local development:

```bash
asvs test http://localhost:3000 --allow-local
```

### Connection timeout

**Symptom:**
```
Error: Connection timed out
```

**Solutions:**

1. **Increase timeout:**
   ```bash
   asvs test https://slow-server.example.com --timeout 120
   ```

2. **Check server is running:**
   ```bash
   curl -I https://slow-server.example.com
   ```

### Missing `requests` library

**Symptom:**
```
Warning: 'requests' library not installed. Install with: pip install requests
```

**Solution:**
```bash
pip install "asvs-compliance-tools[verification]"
# or
pip install requests
```

---

## Docker Issues

### Files not found inside container

**Symptom:**
```
Error: evidence.yml not found
# or
Error: Documents path not found: /app/docs
```

**Solution:**

Ensure proper volume mounting:

```bash
# Linux/Mac
docker run -v $(pwd):/app asvs-engine verify --level 2

# Windows PowerShell
docker run -v ${PWD}:/app asvs-engine verify --level 2

# Windows CMD
docker run -v %cd%:/app asvs-engine verify --level 2
```

### Interactive init fails in Docker

**Symptom:**
```
EOFError: EOF when reading a line
```

**Solution:**

Use `-it` flags for interactive sessions:

```bash
docker run -it -v $(pwd):/app asvs-engine init
```

### Permission denied errors

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: '/app/docs'
```

**Solution:**

Run with user mapping:

```bash
docker run -v $(pwd):/app -u $(id -u):$(id -g) asvs-engine verify
```

---

## CI/CD Issues

### Resources not available in CI

**Symptom:** Commands fail because templates/reference files are missing.

**Solution:**

Download resources as first step:

```yaml
# GitHub Actions
- name: Download ASVS Resources
  run: asvs resources --download --yes --quiet
```

### Exit code not reflecting failure

**Symptom:** CI pipeline shows success even when verification fails.

**Solution:**

Check that you're using `--strict` mode:

```bash
asvs verify --level 2 --evidence evidence.yml --strict
```

Exit codes:
- `0`: All checks passed
- `1`: Verification failed
- `2`: Error (missing files, invalid config)

### JSON output not valid

**Symptom:**
```
json.decoder.JSONDecodeError: Expecting value
```

**Cause:** Non-JSON output mixed with JSON (warnings, prompts).

**Solution:**

Use `--quiet` with `--json`:

```bash
asvs verify --level 2 --json 2>/dev/null > results.json
```

Or redirect stderr:

```bash
asvs verify --level 2 --json 2>&1 | grep -v "^Warning"
```

---

## Getting Help

### Before Opening an Issue

1. **Check version:**
   ```bash
   asvs --version
   python --version
   pip show asvs-compliance-tools
   ```

2. **Try verbose mode:**
   ```bash
   python -m tools.cli verify --level 2 2>&1
   ```

3. **Search existing issues:**
   [GitHub Issues](https://github.com/kaademos/asvs-compliance-starter-kit/issues)

### Opening an Issue

Include:

1. **Command you ran:**
   ```bash
   asvs verify --level 2 --evidence evidence.yml
   ```

2. **Full error output**

3. **Environment info:**
   ```bash
   asvs --version
   python --version
   pip list | grep asvs
   uname -a  # or systeminfo on Windows
   ```

4. **Relevant configuration** (evidence.yml, policy.json)

### Resources

- **Documentation:** [docs/](.)
- **Issues:** [GitHub Issues](https://github.com/kaademos/asvs-compliance-starter-kit/issues)
- **Discussions:** [GitHub Discussions](https://github.com/kaademos/asvs-compliance-starter-kit/discussions)

---

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Command not found | `pip install asvs-compliance-tools` |
| Templates missing | `asvs resources --download` |
| SSRF blocking local | `asvs test URL --allow-local` |
| Version mismatch | `pip install --upgrade asvs-compliance-tools` |
| Docker files missing | `-v $(pwd):/app` |
| CI resources missing | `asvs resources --download --yes --quiet` |
