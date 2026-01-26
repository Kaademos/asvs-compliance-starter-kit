<div align="center">

# ASVS Compliance Engine

### Transform Security Requirements into Verified, Audit-Ready Code

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Kaademos/asvs-compliance-starter-kit/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/Kaademos/asvs-compliance-starter-kit/tree/main)
[![PyPI - Version](https://img.shields.io/pypi/v/asvs-compliance-tools?style=flat-square&color=0066FF&labelColor=1c1c1c)](https://pypi.org/project/asvs-compliance-tools/)
[![Python Version](https://img.shields.io/pypi/pyversions/asvs-compliance-tools?style=flat-square&color=0066FF&labelColor=1c1c1c)](https://pypi.org/project/asvs-compliance-tools/)
[![License](https://img.shields.io/badge/license-MIT-0066FF?style=flat-square&labelColor=1c1c1c)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-0066FF?style=flat-square&labelColor=1c1c1c&logo=docker)](Dockerfile)
[![Downloads](https://img.shields.io/pypi/dm/asvs-compliance-tools?style=flat-square&color=0066FF&labelColor=1c1c1c)](https://pypi.org/project/asvs-compliance-tools/)

<br/>

<img src="https://placehold.co/1200x600/1c1c1c/0066FF?text=Video+Placeholder:+10s+Terminal+Workflow+Demo&font=montserrat" alt="ASVS Compliance Engine Demo" width="100%" />

<br/>
<br/>

**Security compliance shouldn't live in spreadsheets.**

The ASVS Compliance Engine is a production-ready DevSecOps toolkit that operationalizes the **OWASP Application Security Verification Standard (ASVS) 5.0**. It treats compliance as code—scanning your infrastructure, verifying application security controls, and enforcing evidence requirements directly in your CI/CD pipeline.

[**Quick Start**](#-quick-start) · [**Documentation**](docs/) · [**CLI Reference**](#-cli-reference) · [**Report Bug**](https://github.com/kaademos/asvs-compliance-starter-kit/issues)

</div>

---

## Why ASVS Compliance Engine?

Most security compliance efforts fail because they rely on static documents that become obsolete immediately after creation. Teams scramble before audits, screenshots get lost, and "we use bcrypt" becomes impossible to verify.

**This engine bridges the gap between Requirements and Reality.**

| The Old Way | With ASVS Compliance Engine |
| :--- | :--- |
| "Trust me, we use bcrypt" | Automated scans verify `bcrypt` in your `requirements.txt` |
| Architecture diagrams from 2021 | Living documentation mapped to actual code files |
| Manual cloud config reviews | IaC scanning catches misconfigurations before deploy |
| Audit panic and screenshot hunting | One-command HTML reports for SOC2/ISO auditors |
| Security requirements in Confluence | Machine-readable ASVS 5.0 in your CI/CD pipeline |

---

## Key Features

### Unified CLI

One command to rule them all. The `asvs` CLI provides a consistent interface for all compliance operations:

```bash
asvs init        # Bootstrap security documentation
asvs verify      # Validate compliance evidence
asvs scan        # Check Terraform for misconfigurations
asvs test        # DAST scanning for headers/cookies/CSRF
asvs export      # Generate CSV/Jira-ready requirements
asvs drift       # Detect ASVS standard changes
asvs resources   # Manage templates and reference files
```

### Automated Evidence Verification

Don't just claim compliance—prove it. Map ASVS requirements directly to files in your repository using `evidence.yml`. The engine verifies their existence and content during every build.

<img src="https://placehold.co/1000x400/1c1c1c/0066FF?text=Image+Placeholder:+Evidence.yml+Configuration+vs+Terminal+Success&font=montserrat" alt="Evidence Verification" width="100%" />

```yaml
# evidence.yml - Map requirements to proof
requirements:
  V6.2.1:  # Password Storage
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "bcrypt|argon2"
      - type: file_exists
        path: "src/auth/password_hasher.py"
  
  V14.4.1:  # Security Headers
    checks:
      - type: content_match
        path: "package.json"
        pattern: "helmet"
```

### Infrastructure-as-Code Scanning

Shift security left by catching cloud misconfigurations before they deploy. The native scanner checks Terraform plans against ASVS V5.3 (Storage & Cryptography).

<img src="https://placehold.co/1000x300/1c1c1c/0066FF?text=Image+Placeholder:+Terminal+showing+S3+Encryption+Failure&font=montserrat" alt="IaC Scanner" width="100%" />

```bash
# Generate Terraform plan and scan
terraform plan -out=tfplan && terraform show -json tfplan > plan.json
asvs scan plan.json
```

### Dynamic Application Security Testing (DAST)

Lightweight security scanner for running applications. Validates security headers, cookie attributes, CSRF protections, and password policies.

```bash
# Scan your staging environment
asvs test https://staging.example.com

# Scan local dev with SSRF protection disabled
asvs test http://localhost:8000 --allow-local
```

### Auditor-Ready Reports

Generate comprehensive HTML dashboards combining documentation status, code evidence, and DAST results. Perfect for SOC2, ISO 27001, and PCI-DSS audits.

<img src="https://placehold.co/1000x500/1c1c1c/0066FF?text=Image+Placeholder:+Auditor+Dashboard+Screenshot&font=montserrat" alt="Compliance Dashboard" width="100%" />

---

## Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install asvs-compliance-tools

# With optional dependencies for full functionality
pip install "asvs-compliance-tools[evidence,verification]"
```

The CLI automatically downloads required templates and reference files on first use. You'll be prompted to confirm the download from GitHub.

### Initialize Your Project

```bash
# Interactive wizard creates security docs and evidence.yml
asvs init

# Follow the prompts:
# - Project name
# - ASVS assurance level (1, 2, or 3)
# - Output directory for documentation
```

### Verify Compliance

```bash
# Basic verification (auto-detects docs folder)
asvs verify --level 2

# With evidence manifest for code verification
asvs verify --level 2 --evidence evidence.yml

# JSON output for CI/CD pipelines
asvs verify --level 2 --evidence evidence.yml --json --strict
```

### Generate Audit Report

```bash
# Collect verification results
asvs verify --json > compliance.json
asvs test https://your-app.com --json > security.json

# Generate HTML report
python -m tools.generate_report \
  --compliance-json compliance.json \
  --verification-json security.json \
  --output audit_report.html
```

---

## CLI Reference

### Global Options

```bash
asvs --version    # Show version (currently 2.2.0)
asvs --help       # Show help
asvs <cmd> --help # Command-specific help
```

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Bootstrap security documentation templates | `asvs init` |
| `verify` | Validate documentation and code evidence | `asvs verify --level 2 --evidence evidence.yml` |
| `scan` | Scan Terraform plans for ASVS violations | `asvs scan plan.json` |
| `test` | DAST scanning for web applications | `asvs test https://example.com` |
| `export` | Export ASVS requirements to CSV/Jira | `asvs export --level 2 --format csv` |
| `drift` | Check for ASVS standard updates | `asvs drift` |
| `resources` | Manage CLI templates and reference files | `asvs resources --status` |

### Verify Command Options

```bash
asvs verify [OPTIONS]

Options:
  -d, --docs-path PATH      Documentation directory (auto-detects ./docs)
  -l, --level {1,2,3}       ASVS assurance level (default: 2)
  -e, --evidence PATH       Path to evidence.yml manifest
  -c, --config PATH         Policy configuration JSON
  --json                    Output in JSON format
  --strict                  Fail on warnings
```

### Test Command Options

```bash
asvs test <URL> [OPTIONS]

Options:
  --allow-local    Allow scanning localhost/private IPs
  --json           Output in JSON format
  --timeout INT    Request timeout in seconds
```

### Export Command Options

```bash
asvs export [OPTIONS]

Options:
  -l, --level {1,2,3}         ASVS level (default: 2)
  -f, --format {csv,jira-json} Output format (default: csv)
  -o, --output PATH           Output file (default: stdout)
  -s, --source PATH           Custom source JSON file
```

### Resources Command Options

```bash
asvs resources [OPTIONS]

Options:
  --download      Download all resources from GitHub
  --status        Show cache status
  --clear         Clear cached resources
  -y, --yes       Skip confirmation prompt
  -q, --quiet     Suppress progress output
```

---

## Docker Usage

Run the compliance engine without installing Python:

```bash
# Build the image
docker build -t asvs-engine .

# Run verification
docker run -v $(pwd):/app asvs-engine verify --level 2

# Run DAST scanner
docker run asvs-engine test https://example.com

# Interactive init (requires TTY)
docker run -it -v $(pwd):/app asvs-engine init
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Compliance
on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install ASVS Compliance Tools
        run: pip install "asvs-compliance-tools[evidence,verification]"
      
      - name: Download Resources
        run: asvs resources --download --yes --quiet
      
      - name: Verify Compliance
        run: asvs verify --level 2 --evidence evidence.yml --strict --json
      
      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: compliance-report
          path: compliance.json
```

### GitLab CI

```yaml
compliance:
  image: python:3.12-slim
  script:
    - pip install "asvs-compliance-tools[evidence,verification]"
    - asvs resources --download --yes --quiet
    - asvs verify --level 2 --evidence evidence.yml --json > compliance.json
  artifacts:
    reports:
      dotenv: compliance.json
    paths:
      - compliance.json
```

### CircleCI

```yaml
version: 2.1
jobs:
  compliance:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Install and Verify
          command: |
            pip install "asvs-compliance-tools[evidence,verification]"
            asvs resources --download --yes --quiet
            asvs verify --level 2 --evidence evidence.yml --strict
```

---

## Project Structure

```
asvs-compliance-starter-kit/
├── tools/                          # CLI source code
│   ├── cli.py                      # Unified CLI entry point
│   ├── compliance_gate.py          # Documentation & evidence verification
│   ├── verification_suite.py       # DAST scanner
│   ├── iac_scanner.py              # Terraform scanner
│   ├── export_requirements.py      # CSV/Jira export
│   ├── drift_detector.py           # ASVS standard drift detection
│   ├── resource_manager.py         # Template/resource download manager
│   └── init_project.py             # Project initialization wizard
├── 00-Documentation-Standards/     # Decision templates
│   └── Decision-Templates/         # Security strategy templates
├── 01-ASVS-Core-Reference/         # Machine-readable ASVS 5.0
│   ├── ASVS-5.0-en.json           # Full ASVS specification
│   ├── ASVS-L1-Baseline.json      # Level 1 requirements
│   ├── ASVS-L2-Standard.json      # Level 2 requirements
│   └── Functional-Requirements/    # Requirements by level
├── 02-Implementation-Guidance/     # Secure coding patterns
│   ├── Languages/                  # Language-specific guides
│   │   ├── NodeJS/
│   │   ├── Python/
│   │   └── Terraform/
│   └── Patterns/                   # Security implementation patterns
├── policies/                       # OPA/Rego policy files
├── docs/                           # User documentation
├── tests/                          # Test suite (195 tests)
├── evidence.example.yml            # Example evidence manifest
└── pyproject.toml                  # Package configuration
```

---

## ASVS Levels Explained

| Level | Name | Use Case | Required Documents |
|-------|------|----------|-------------------|
| **L1** | Opportunistic | All applications | None (baseline) |
| **L2** | Standard | Apps handling sensitive data | Cryptography Strategy |
| **L3** | Advanced | Critical infrastructure, healthcare, finance | All L2 + additional |

The engine enforces documentation requirements based on your selected level. Higher levels require more comprehensive security decision records.

---

## Evidence Manifest Reference

The `evidence.yml` file maps ASVS requirements to verifiable evidence in your codebase:

```yaml
# evidence.yml
requirements:
  # V6.2.1: Password Storage
  V6.2.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "bcrypt|argon2|scrypt"
      - type: file_exists
        path: "src/auth/password_service.py"

  # V14.4.1: HTTP Security Headers
  V14.4.1:
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"helmet"'
      - type: content_match
        path: "src/middleware/security.js"
        pattern: "helmet\\(\\)"

  # V1.1.1: Security Documentation
  V1.1.1:
    checks:
      - type: file_exists
        path: "SECURITY.md"
      - type: file_exists
        path: "docs/threat-model.md"
```

### Check Types

| Type | Description | Required Fields |
|------|-------------|-----------------|
| `file_exists` | Verify a file exists | `path` |
| `content_match` | Search file for regex pattern | `path`, `pattern` |

---

## Troubleshooting

### Templates Not Found

If you see "Templates unavailable" when running `asvs init`:

```bash
# Download resources from GitHub
asvs resources --download

# Or clone the full repository
git clone https://github.com/Kaademos/asvs-compliance-starter-kit.git
cd asvs-compliance-starter-kit
pip install -e .
```

### Version Mismatch

Ensure you have the latest version:

```bash
pip install --upgrade asvs-compliance-tools
asvs --version  # Should show 2.2.0
```

### SSRF Protection Blocking Local Scans

The DAST scanner blocks localhost by default:

```bash
# Enable local scanning explicitly
asvs test http://localhost:3000 --allow-local
```

### Docker Volume Mounting

Ensure proper volume mounting for file access:

```bash
# Linux/Mac
docker run -v $(pwd):/app asvs-engine verify

# Windows PowerShell
docker run -v ${PWD}:/app asvs-engine verify

# Windows CMD
docker run -v %cd%:/app asvs-engine verify
```

See [docs/troubleshooting.md](docs/troubleshooting.md) for more solutions.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick ways to contribute:**
- Add secure coding patterns for your favorite framework
- Improve documentation and examples
- Report bugs and suggest features
- Add language-specific implementation guides

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features including:
- Two-way Jira/GitHub issue sync
- Framework auto-detection (Django, FastAPI, Express, Spring Boot)
- IDE plugins for VS Code and IntelliJ
- PDF/DOCX export for auditors

## Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/kaademos/asvs-compliance-starter-kit/issues)
- **Discussions:** [GitHub Discussions](https://github.com/kaademos/asvs-compliance-starter-kit/discussions)

---

<div align="center">

**Built for the Security Community**

[OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) · [Report Bug](https://github.com/kaademos/asvs-compliance-starter-kit/issues) · [Request Feature](https://github.com/kaademos/asvs-compliance-starter-kit/issues)

</div>
