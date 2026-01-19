# User Guide

This guide details the usage of every tool in the ASVS Compliance Engine.

## 1. Compliance Gate (`compliance_gate`)

The primary enforcement tool for CI/CD. It verifies that your security documentation exists and that your code meets defined evidence standards.

### Usage
```bash
python -m tools.compliance_gate [OPTIONS]

```

### Options

* `--docs-path PATH`: Directory containing your security decision records (default: `./docs`).
* `--level {1,2,3}`: ASVS assurance level to enforce (default: 2).
* `--evidence-manifest PATH`: Path to your `evidence.yml` configuration.
* `--format {text,json}`: Output format. Use `json` for pipeline parsing.
* `--strict`: Fail on warnings (e.g., placeholder text found).

### Example: CI Pipeline

```bash
# Fail build if level 2 requirements aren't met
python -m tools.compliance_gate \
  --docs-path ./security-docs \
  --level 2 \
  --evidence-manifest evidence.yml \
  --strict

```

---

## 2. Infrastructure Scanner (`iac_scanner`)

Scans Terraform plan files for ASVS V5.3 (Cloud Storage) violations. Currently supports AWS S3.

### Prerequisites

You must generate a Terraform plan in JSON format first:

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json

```

### Usage

```bash
python -m tools.iac_scanner --plan-file plan.json

```

### Checks Performed

* **Encryption:** Verifies Server-Side Encryption (SSE) is enabled.
* **Public Access:** Checks for `aws_s3_bucket_public_access_block`.

---

## 3. Verification Suite (`verification_suite`)

A lightweight DAST (Dynamic Application Security Testing) tool that checks running applications for visible security controls.

### Usage

```bash
python -m tools.verification_suite --target-url [https://staging.example.com](https://staging.example.com)

```

### Security Note (SSRF Protection)

By default, the tool blocks connections to `localhost`, `127.0.0.1`, and private network ranges to prevent Server-Side Request Forgery. To scan a local development server, use the override flag:

```bash
python -m tools.verification_suite --target-url http://localhost:8000 --allow-local

```

---

## 4. Report Generator (`generate_report`)

Combines outputs from other tools into a single HTML dashboard for auditors.

### Usage

```bash
# 1. Run tools and save output
python -m tools.compliance_gate ... --format json > gate.json
python -m tools.verification_suite ... --format json > verify.json

# 2. Generate HTML
python -m tools.generate_report \
  --compliance-json gate.json \
  --verification-json verify.json \
  --output audit_report.html

```