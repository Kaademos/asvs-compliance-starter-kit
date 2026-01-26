# User Guide

Complete reference for the ASVS Compliance Engine CLI.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Command Reference](#command-reference)
  - [asvs init](#asvs-init)
  - [asvs verify](#asvs-verify)
  - [asvs scan](#asvs-scan)
  - [asvs test](#asvs-test)
  - [asvs export](#asvs-export)
  - [asvs drift](#asvs-drift)
  - [asvs resources](#asvs-resources)
- [Report Generation](#report-generation)
- [CI/CD Integration](#cicd-integration)

---

## Installation

### From PyPI (Recommended)

```bash
# Basic installation
pip install asvs-compliance-tools

# With all optional dependencies
pip install "asvs-compliance-tools[evidence,verification]"
```

### From Source

```bash
git clone https://github.com/Kaademos/asvs-compliance-starter-kit.git
cd asvs-compliance-starter-kit
pip install -e ".[dev,evidence,verification]"
```

### Verify Installation

```bash
asvs --version
# Output: asvs 2.2.0
```

---

## Getting Started

### 1. Initialize Your Project

```bash
asvs init
```

The interactive wizard will prompt you for:
- **Project Name:** Used in generated documentation
- **ASVS Level:** 1 (Basic), 2 (Standard), or 3 (Advanced)
- **Output Directory:** Where to create security documents

This creates:
- Security decision templates in your docs folder
- An `evidence.yml` file for mapping requirements to code

### 2. Configure Evidence Mapping

Edit `evidence.yml` to map ASVS requirements to your codebase:

```yaml
requirements:
  V6.2.1:  # Password Hashing
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "bcrypt|argon2"
        
  V14.4.1:  # Security Headers
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"helmet"'
```

### 3. Run Verification

```bash
# Basic check
asvs verify --level 2

# With evidence verification
asvs verify --level 2 --evidence evidence.yml

# Strict mode (fail on warnings)
asvs verify --level 2 --evidence evidence.yml --strict
```

---

## Command Reference

### asvs init

Bootstrap security documentation templates for your project.

```bash
asvs init [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--interactive`, `-i` | Run in interactive mode (default: True) |

**What Gets Created:**

- `V6-Authentication-Strategy.md` - Authentication decisions
- `V7-Session-Management.md` - Session handling approach
- `V8-Authorization-Rules.md` - Access control definitions
- `V11-Cryptography-Strategy.md` - Encryption standards
- `V14-Data-Classification.md` - Data handling policies
- `V16-Security-Logging-Strategy.md` - Logging requirements
- `evidence.yml` - Evidence mapping template

**First-Time Setup:**

If templates aren't available locally (pip-only install), you'll be prompted to download them from GitHub:

```
ASVS Compliance Starter Kit - Resource Download Required
============================================================

The ASVS CLI requires additional resources to function fully.
Resources will be downloaded from:
  https://github.com/Kaademos/asvs-compliance-starter-kit

Do you want to download these resources? [Y/n]:
```

If you decline, you can:
1. Run `asvs resources --download` later
2. Clone the full repository from GitHub

---

### asvs verify

Validate security documentation and code evidence.

```bash
asvs verify [OPTIONS]
```

**Options:**

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--docs-path` | `-d` | Documentation directory | Auto-detect |
| `--level` | `-l` | ASVS level (1, 2, 3) | 2 |
| `--evidence` | `-e` | Path to evidence.yml | None |
| `--config` | `-c` | Policy configuration JSON | None |
| `--json` | | Output in JSON format | False |
| `--strict` | | Fail on warnings | False |

**Auto-Detection:**

If `--docs-path` is not specified, the tool checks:
1. `./docs`
2. `./03-Product-Specific-Files`
3. Current directory

**Examples:**

```bash
# Basic verification
asvs verify --level 2

# Explicit paths
asvs verify --docs-path ./security-docs --evidence evidence.yml

# CI/CD mode
asvs verify --level 2 --evidence evidence.yml --json --strict

# Level 1 (no docs required)
asvs verify --level 1
```

**Output (Text):**

```
ASVS Compliance Gate - Level 2
==================================================
Documents checked: 1
Documents valid: 1
Status: PASSED

  ✓ V11-Cryptography-Strategy.md

Automated Evidence Verification
==============================
  ✓ [V6.2.1] content_match: requirements.txt
  ✓ [V14.4.1] file_exists: src/middleware/security.js
```

**Output (JSON):**

```json
{
  "passed": true,
  "level": 2,
  "documents": {
    "checked": 1,
    "valid": 1,
    "results": [...]
  },
  "evidence": {
    "checked": 2,
    "passed": 2,
    "results": [...]
  }
}
```

---

### asvs scan

Scan Terraform plans for ASVS V5.3 (Storage & Cryptography) violations.

```bash
asvs scan <plan-file> [OPTIONS]
```

**Prerequisites:**

Generate a Terraform plan in JSON format:

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--json` | Output in JSON format | False |

**Checks Performed:**

| Check | ASVS Requirement | Description |
|-------|------------------|-------------|
| SSE Encryption | V5.3.1 | Server-side encryption enabled |
| Public Access | V5.3.2 | Public access blocks configured |

**Examples:**

```bash
# Scan Terraform plan
asvs scan plan.json

# JSON output for CI
asvs scan plan.json --json
```

**Output:**

```
IaC Security Scanner - ASVS V5.3
================================
Scanning: plan.json

Findings:
  ✗ [HIGH] aws_s3_bucket.data: Missing server-side encryption
  ✓ [PASS] aws_s3_bucket.logs: Encryption enabled (AES256)
  
Summary: 1 violation, 1 passed
```

---

### asvs test

Dynamic Application Security Testing (DAST) for web applications.

```bash
asvs test <url> [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--allow-local` | Allow localhost/private IPs | False |
| `--json` | Output in JSON format | False |
| `--timeout` | Request timeout (seconds) | 30 |

**Security Checks:**

| Category | Checks |
|----------|--------|
| Headers | HSTS, X-Content-Type-Options, X-Frame-Options, CSP |
| Cookies | Secure, HttpOnly, SameSite attributes |
| CSRF | Token presence, meta tags, cookies |
| Passwords | Input field security attributes |

**SSRF Protection:**

By default, the scanner blocks:
- `localhost`, `127.0.0.1`, `::1`
- Private networks (10.x, 172.16.x, 192.168.x)
- Link-local addresses (169.254.x)

Use `--allow-local` to scan development servers.

**Examples:**

```bash
# Scan production site
asvs test https://example.com

# Scan local development
asvs test http://localhost:3000 --allow-local

# With timeout and JSON output
asvs test https://staging.example.com --timeout 60 --json
```

**Output:**

```
ASVS Verification Suite
=======================
Target: https://example.com

Security Headers (V14.4):
  ✓ Strict-Transport-Security: max-age=31536000
  ✓ X-Content-Type-Options: nosniff
  ✓ X-Frame-Options: DENY
  ✗ Content-Security-Policy: Missing

Cookie Security (V3.4):
  ✓ session: Secure, HttpOnly, SameSite=Strict

CSRF Protection (V4.2):
  ✓ CSRF token found in form

Summary: 4 passed, 1 failed
```

---

### asvs export

Export ASVS requirements to CSV or Jira-compatible JSON.

```bash
asvs export [OPTIONS]
```

**Options:**

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--level` | `-l` | ASVS level (1, 2, 3) | 2 |
| `--format` | `-f` | Output format (csv, jira-json) | csv |
| `--output` | `-o` | Output file path | stdout |
| `--source` | `-s` | Custom source JSON file | Auto |

**Examples:**

```bash
# Export L2 requirements to CSV
asvs export --level 2 --format csv > requirements.csv

# Export for Jira import
asvs export --level 2 --format jira-json --output jira-import.json

# Export L3 (comprehensive)
asvs export --level 3 --format csv --output asvs-l3.csv
```

**CSV Output Format:**

```csv
"Issue Key","Summary","Description","Labels","Chapter","Section"
"V1.2.1","[ASVS V1.2.1] Injection Prevention","Verify that...","asvs,security,L1,V1","Encoding","Injection Prevention"
```

**Jira JSON Format:**

```json
{
  "issues": [
    {
      "summary": "[ASVS V1.2.1] Injection Prevention",
      "description": "Verify that...",
      "labels": ["asvs", "security", "L1", "v1"],
      "customFields": {
        "asvsId": "V1.2.1",
        "asvsChapter": "Encoding and Sanitization",
        "asvsLevel": "1"
      }
    }
  ]
}
```

---

### asvs drift

Check for updates to the ASVS standard.

```bash
asvs drift [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--local` | Path to local ASVS JSON | Auto-detect |
| `--offline` | Skip upstream fetch | False |
| `--json` | Output in JSON format | False |

**Examples:**

```bash
# Check for drift against upstream OWASP
asvs drift

# Offline validation only
asvs drift --offline

# JSON output
asvs drift --json
```

**Output:**

```
ASVS Drift Detector
===================
Local Version: 5.0.0
Upstream Version: 5.0.0

Status: No drift detected

Requirements:
  Local: 286
  Upstream: 286
  Added: 0
  Removed: 0
  Modified: 0
```

---

### asvs resources

Manage CLI templates and reference files.

```bash
asvs resources [OPTIONS]
```

**Options:**

| Option | Short | Description |
|--------|-------|-------------|
| `--download` | | Download all resources from GitHub |
| `--status` | | Show cache status |
| `--clear` | | Clear cached resources |
| `--yes` | `-y` | Skip confirmation prompt |
| `--quiet` | `-q` | Suppress progress output |

**Examples:**

```bash
# Check what's cached
asvs resources --status

# Download everything
asvs resources --download

# Non-interactive download (for CI)
asvs resources --download --yes --quiet

# Clear cache
asvs resources --clear
```

**Cache Location:**

Resources are cached at `~/.asvs-compliance/resources/`

**Status Output:**

```
Cache directory: /home/user/.asvs-compliance/resources

  Decision templates for security documentation: Available
  ASVS core reference files (JSON/CSV): Available
  Functional requirements by level: Missing
  Implementation patterns: Missing
```

---

## Report Generation

Combine verification results into an HTML audit dashboard.

### Generate Reports

```bash
# 1. Run verification tools with JSON output
asvs verify --level 2 --evidence evidence.yml --json > compliance.json
asvs test https://your-app.com --json > security.json

# 2. Generate HTML report
python -m tools.generate_report \
  --compliance-json compliance.json \
  --verification-json security.json \
  --output audit_report.html

# 3. Open in browser
open audit_report.html  # macOS
xdg-open audit_report.html  # Linux
```

### Report Contents

- **Executive Summary:** Pass/fail status, coverage metrics
- **Documentation Status:** Required docs and their validation state
- **Evidence Verification:** Code-level checks and results
- **Security Scan Results:** DAST findings with recommendations
- **Timestamps:** When each check was performed

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Compliance

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  compliance:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install ASVS Tools
        run: pip install "asvs-compliance-tools[evidence,verification]"
      
      - name: Download Resources
        run: asvs resources --download --yes --quiet
      
      - name: Verify Documentation
        run: asvs verify --level 2 --strict
      
      - name: Verify Evidence
        run: asvs verify --level 2 --evidence evidence.yml --json > compliance.json
      
      - name: Security Scan (Staging)
        if: github.event_name == 'push'
        run: asvs test ${{ secrets.STAGING_URL }} --json > security.json
        continue-on-error: true
      
      - name: Generate Report
        run: |
          python -m tools.generate_report \
            --compliance-json compliance.json \
            --verification-json security.json \
            --output report.html
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: compliance-report
          path: |
            compliance.json
            security.json
            report.html
```

### GitLab CI

```yaml
stages:
  - compliance
  - security

compliance:
  stage: compliance
  image: python:3.12-slim
  script:
    - pip install "asvs-compliance-tools[evidence,verification]"
    - asvs resources --download --yes --quiet
    - asvs verify --level 2 --evidence evidence.yml --strict --json > compliance.json
  artifacts:
    paths:
      - compliance.json
    reports:
      dotenv: compliance.json

security_scan:
  stage: security
  image: python:3.12-slim
  script:
    - pip install "asvs-compliance-tools[verification]"
    - asvs test $STAGING_URL --json > security.json
  artifacts:
    paths:
      - security.json
  only:
    - main
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: asvs-verify
        name: ASVS Compliance Check
        entry: asvs verify --level 1
        language: system
        pass_filenames: false
```

---

## Next Steps

- [Configuration Guide](configuration.md) - Deep dive into `evidence.yml`
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Contributing](../CONTRIBUTING.md) - Help improve the tools
