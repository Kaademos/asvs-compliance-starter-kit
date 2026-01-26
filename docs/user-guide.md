# User Guide

This guide details the usage of every tool in the ASVS Compliance Engine.

## Unified CLI (`asvs`)

The toolkit provides a single `asvs` command to manage all compliance tasks. Install the package and use the unified CLI:

```bash
pip install -e .
asvs --help
```

---

## 1. Verify Compliance (`asvs verify`)

The primary enforcement tool for CI/CD. It verifies that your security documentation exists and that your code meets defined evidence standards.

### Usage

```bash
asvs verify [OPTIONS]
```

### Options

* `--docs-path, -d PATH`: Directory containing your security decision records (auto-detects `./docs` or `./03-Product-Specific-Files`).
* `--level, -l {1,2,3}`: ASVS assurance level to enforce (default: 2).
* `--evidence, -e PATH`: Path to your `evidence.yml` configuration.
* `--config, -c PATH`: Path to policy configuration JSON.
* `--json`: Output in JSON format (good for CI).
* `--strict`: Fail on warnings (e.g., placeholder text found).

### Examples

```bash
# Basic verification (auto-detects docs folder)
asvs verify --level 2

# With explicit docs path and evidence
asvs verify --docs-path ./security-docs --evidence evidence.yml

# JSON output for CI pipelines
asvs verify --level 2 --json --strict
```

### Legacy Usage

The original CLI is still supported:

```bash
python -m tools.compliance_gate --docs-path ./docs --level 2
```

---

## 2. Infrastructure Scanner (`asvs scan`)

Scans Terraform plan files for ASVS V5.3 (Cloud Storage) violations. Currently supports AWS S3.

### Prerequisites

You must generate a Terraform plan in JSON format first:

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

### Usage

```bash
asvs scan <plan-file> [OPTIONS]
```

### Examples

```bash
# Scan a Terraform plan
asvs scan plan.json

# JSON output for CI
asvs scan plan.json --json
```

### Checks Performed

* **Encryption:** Verifies Server-Side Encryption (SSE) is enabled.
* **Public Access:** Checks for `aws_s3_bucket_public_access_block`.

---

## 3. Verification Suite (`asvs test`)

A lightweight DAST (Dynamic Application Security Testing) tool that checks running applications for visible security controls.

### Usage

```bash
asvs test <url> [OPTIONS]
```

### Options

* `--allow-local`: Allow scanning localhost/private IPs (disable SSRF protection).
* `--json`: Output in JSON format.
* `--timeout`: Request timeout in seconds.

### Examples

```bash
# Scan a staging server
asvs test https://staging.example.com

# Scan local development server
asvs test http://localhost:8000 --allow-local

# JSON output
asvs test https://example.com --json
```

### Security Note (SSRF Protection)

By default, the tool blocks connections to `localhost`, `127.0.0.1`, and private network ranges to prevent Server-Side Request Forgery.

---

## 4. Export Requirements (`asvs export`)

Export ASVS requirements to CSV or Jira-compatible JSON format.

### Usage

```bash
asvs export [OPTIONS]
```

### Options

* `--level, -l {1,2,3}`: ASVS level to export (default: 2).
* `--format, -f {csv,jira-json}`: Output format (default: csv).
* `--output, -o PATH`: Output file (default: stdout).

### Examples

```bash
# Export L2 requirements to CSV
asvs export --level 2 --format csv > requirements.csv

# Export to Jira JSON
asvs export --format jira-json --output jira-import.json
```

---

## 5. Drift Detector (`asvs drift`)

Compare local ASVS implementation against the upstream OWASP standard.

### Usage

```bash
asvs drift [OPTIONS]
```

### Options

* `--local PATH`: Path to local ASVS JSON file.
* `--offline`: Skip upstream fetch (offline mode).
* `--json`: Output in JSON format.

### Examples

```bash
# Check for drift against upstream
asvs drift

# Offline mode (only validate local file)
asvs drift --offline
```

---

## 6. Initialize Project (`asvs init`)

Bootstrap security documentation templates for your project.

### Usage

```bash
asvs init [OPTIONS]
```

### Options

* `--interactive, -i`: Run in interactive mode (default: True).

### Example

```bash
asvs init
```

---

## 7. Report Generator (`generate_report`)

Combines outputs from other tools into a single HTML dashboard for auditors.

### Usage

```bash
# 1. Run tools and save output
asvs verify --json > gate.json
asvs test https://example.com --json > verify.json

# 2. Generate HTML
python -m tools.generate_report \
  --compliance-json gate.json \
  --verification-json verify.json \
  --output audit_report.html
```