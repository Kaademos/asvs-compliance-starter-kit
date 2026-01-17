<p align="center">
  <h1 align="center">ASVS Compliance Engine</h1>
  <p align="center">
    <strong>Turn Security Requirements into Verifiable Code.</strong>
  </p>
  <p align="center">
    Automate OWASP ASVS 5.0 compliance with Evidence Verification, Infrastructure Scanning, and Auditor-Ready Reporting.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.0-blue.svg" alt="Version 2.1.0">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-green.svg" alt="License"></a>
</p>

---

## Why Use This?

Most compliance efforts fail because they rely on static Word documents that rot. This toolset treats **Compliance as Code**:

1.  **Init:** Generate a tailored security architecture based on your risk profile.
2.  **Code:** Map your actual code files (`package.json`, `main.tf`) as evidence.
3.  **Verify:** CI/CD pipelines automatically fail if evidence is missing or insecure.
4.  **Report:** Generate HTML dashboards for your auditors (SOC2, ISO 27001).

---

## ⚡ Quick Start

### 1. Initialize Your Project
Don't start from a blank page. Run the wizard to generate your security architecture docs.

```bash
# Generate docs/ folder and evidence.yml
python -m tools.init_project --interactive

```

### 2. Map Your Evidence

Tell the engine where to find proof of security controls in your code.

```yaml
# evidence.yml
requirements:
  V14.4: # HTTP Security Headers
    checks:
      - type: content_match
        path: "package.json"
        pattern: "helmet"

```

### 3. Verify in CI/CD

Run the Compliance Gate to verify both documentation and code evidence.

```bash
python -m tools.compliance_gate --level 2 --evidence-manifest evidence.yml

```

### 4. Scan Infrastructure

Ensure your S3 buckets and cloud storage meet ASVS V5.3 requirements.

```bash
# Generate Terraform plan JSON
terraform show -json tfplan > plan.json

# Scan for misconfigurations
python -m tools.iac_scanner --plan-file plan.json

```

### 5. Generate Auditor Report

Create a single-page HTML dashboard combining all findings.

```bash
python -m tools.generate_report \
  --compliance-json gate_output.json \
  --verification-json verify_output.json \
  --output audit-report.html

```

---

## Docker Usage

No Python? No problem. Run the full suite via Docker.

```bash
# Build
docker build -t asvs-engine .

# Run Compliance Gate
docker run -v $(pwd):/app asvs-engine tools.compliance_gate --docs-path docs --level 2

# Run Infrastructure Scan
docker run -v $(pwd):/app asvs-engine tools.iac_scanner --plan-file plan.json

```

---

## Features

| Feature | Description | Enterprise Value |
| --- | --- | --- |
| **Evidence Verifier** | Scans code for regex patterns/file existence. | Auto-validates controls (e.g., "Is `bcrypt` installed?") |
| **IaC Scanner** | Checks Terraform plans for unencrypted storage. | Prevents cloud misconfigurations before deploy. |
| **Drift Detector** | Compares local ASVS JSON vs Upstream. | Keeps you aligned with the latest OWASP standard. |
| **Verification Suite** | Light DAST for Headers, Cookies, CSRF. | Verifies running application posture. |
| **Report Generator** | HTML Dashboard. | Replaces manual evidence collection spreadsheets. |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to build, test, and submit PRs.

## Funding

If this tool saves you hours of audit prep, please consider [Sponsoring](.github/FUNDING.yml) to support the development of:

* **Jira Two-Way Sync:** Auto-close tickets based on passing tests.
* **Pre-built Evidence Packs:** Drop-in rules for Node.js, Django, Spring Boot.

---

<p align="center">
  <sub>Built with ❤️ for the community</sub>
</p>

<p align="center">
  <a href="https://owasp.org/www-project-application-security-verification-standard/">OWASP ASVS</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Report Bug</a> •
  <a href="https://github.com/kaademos/asvs-compliance-starter-kit/issues">Request Feature</a>
</p>
