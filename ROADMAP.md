# Product Roadmap

**Vision:** Build the industry-standard open-source compliance engine that transforms OWASP ASVS from static checklists into verifiable, automated code.

---

## Current Release: v2.2.0

### Highlights

- **Unified CLI:** Single `asvs` command for all compliance operations
- **Resource Manager:** Automatic download of templates from GitHub for pip-only installations
- **Dynamic Versioning:** Version info pulled from package metadata
- **195 Tests:** Comprehensive test coverage for all tools

### Full Feature Set

| Feature | Status | Description |
|---------|--------|-------------|
| Unified CLI (`asvs`) | Complete | Single entry point for all tools |
| Interactive Init | Complete | Wizard for project bootstrapping |
| Compliance Gate | Complete | Documentation and evidence verification |
| Evidence Verifier | Complete | `file_exists` and `content_match` checks |
| IaC Scanner | Complete | Terraform plan scanning for AWS S3 |
| Verification Suite | Complete | DAST for headers, cookies, CSRF |
| Export Tool | Complete | CSV and Jira JSON export |
| Drift Detector | Complete | ASVS standard version comparison |
| Resource Manager | Complete | Auto-download templates from GitHub |
| HTML Reports | Complete | Auditor dashboard generation |
| Docker Support | Complete | Container-ready deployment |

---

## Completed Milestones

### v2.0: The Compliance Engine
*Transformation from "Text Files" to "Active Verification"*

- [x] Automated evidence verification with `evidence.yml`
- [x] Infrastructure scanning for Terraform (ASVS V5.3)
- [x] Auditor-ready HTML dashboard generation
- [x] Interactive project initialization wizard
- [x] Docker container support

### v1.x: Foundation
- [x] Machine-readable ASVS 5.0 (JSON/CSV)
- [x] Decision templates for SOC2/ISO mapping
- [x] Lightweight DAST verification suite
- [x] Python package on PyPI

---

## In Progress: v2.3.0

**Theme:** Enterprise CI/CD Integration

| Feature | Status | Target |
|---------|--------|--------|
| GitHub Actions Summary | In Progress | Q1 2026 |
| GitLab Report Artifacts | Planned | Q1 2026 |
| Exit Codes Standardization | Planned | Q1 2026 |
| SARIF Output Format | Planned | Q1 2026 |

### Details

#### GitHub Actions Integration
Native step summaries for GitHub Actions workflows:
```yaml
- name: Verify Compliance
  run: asvs verify --level 2 --github-summary
```

#### SARIF Output
Security scanning results in SARIF format for code scanning alerts:
```bash
asvs verify --format sarif > results.sarif
asvs test https://example.com --format sarif >> results.sarif
```

---

## Planned: v2.4.0

**Theme:** Framework Auto-Detection

| Feature | Priority | Description |
|---------|----------|-------------|
| Framework Detector | High | Auto-detect Django, FastAPI, Express, etc. |
| Pre-built Evidence Packs | High | Ready-to-use patterns for common frameworks |
| Dependency Scanning | Medium | Check `requirements.txt`, `package.json` for security libs |

### Framework Evidence Packs

Auto-generated `evidence.yml` patterns for:

**Python:**
- Django (CSRF, sessions, password validation)
- FastAPI (Pydantic validation, CORS, security headers)
- Flask (Flask-Security, Flask-Login patterns)

**Node.js:**
- Express (Helmet, express-validator, csurf)
- Fastify (fastify-helmet, fastify-csrf)
- NestJS (built-in security modules)

**Java:**
- Spring Boot (Spring Security, validation)

```bash
# Future usage
asvs init --detect-framework
# Detected: FastAPI
# Generated evidence.yml with 12 pre-configured checks
```

---

## Planned: v3.0.0

**Theme:** Compliance Platform

### Policy Registry
Centralized repository of community-maintained evidence patterns:
```bash
asvs policy search "password hashing"
asvs policy install asvs-evidence-django
```

### IDE Integration
Real-time ASVS feedback in your editor:

<img src="https://placehold.co/800x400/1c1c1c/0066FF?text=IDE+Placeholder:+VS+Code+Extension+Preview&font=montserrat" alt="IDE Integration Preview" width="100%" />

- VS Code extension
- IntelliJ plugin
- Inline security suggestions
- Evidence gap highlighting

### Export Formats
One-click audit artifact generation:
```bash
asvs report --format pdf --output audit-2026.pdf
asvs report --format docx --template soc2
```

### Advanced Scanning

| Scanner | Target | Status |
|---------|--------|--------|
| AWS CDK | CloudFormation output | Planned |
| Azure Bicep | ARM templates | Planned |
| Pulumi | State inspection | Planned |
| Kubernetes | Security contexts | Planned |

---

## Future Vision: v4.0+

### Continuous Compliance
- Real-time monitoring of compliance drift
- Webhook integrations for compliance events
- Slack/Teams notifications for violations

### AI-Assisted Remediation
- Suggested fixes for failing checks
- Auto-generated evidence mappings
- Natural language requirement queries

### Multi-Standard Support
- PCI-DSS mapping
- NIST 800-53 controls
- CIS Benchmarks
- Custom control frameworks

---

## How to Contribute

We prioritize features that shift security **left** in the development lifecycle.

### High-Impact Areas

1. **Framework Adapters** - Add evidence patterns for your stack
2. **IaC Scanners** - Extend to new infrastructure tools
3. **DAST Checks** - New security verification checks
4. **Documentation** - Guides, tutorials, examples

### Getting Started

```bash
# Check open issues
gh issue list --label "help wanted"

# Good first issues
gh issue list --label "good first issue"
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.

---

## Feedback

Your input shapes this roadmap:

- **Feature Requests:** [Open an Issue](https://github.com/kaademos/asvs-compliance-starter-kit/issues/new)
- **Discussions:** [GitHub Discussions](https://github.com/kaademos/asvs-compliance-starter-kit/discussions)
- **Priority Voting:** React with on issues you want prioritized

---

*Roadmap last updated: January 2026*
