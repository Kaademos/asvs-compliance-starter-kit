# Product Roadmap

**Vision:** To build the industry-standard open-source Compliance Engine that transforms OWASP ASVS from a static checklist into verifiable, automated code.

---

## ✅ Completed Milestones

### v2.0: The Compliance Engine (Current)
*Transformation from "Text Files" to "Active Verification"*
- [x] **Automated Evidence Verification:** `compliance_gate` now verifies file existence and content patterns (e.g., checking for `helmet` or `bcrypt`).
- [x] **Infrastructure Scanning:** Native `iac_scanner` for Terraform plans to catch unencrypted storage (ASVS V5.3).
- [x] **Auditor Dashboard:** HTML report generation combining documentation, code evidence, and DAST results.
- [x] **Developer Experience:** Interactive `init` wizard and Docker container support.

### v1.0 - v1.2: Foundation & Policy
- [x] **Core Reference:** Machine-readable ASVS 5.0 (JSON/CSV).
- [x] **Decision Templates:** Markdown templates for SOC2/ISO mapping.
- [x] **Verification Suite:** Lightweight DAST for headers and cookies.

---

## 🚧 Current Focus: v2.x (Enterprise Ready)

**Goal:** Remove friction for enterprise adoption and enable "set and forget" compliance.

### v2.1: Integrations & Trust
- [ ] **Two-Way Issue Sync:** Automatically close Jira/GitHub issues when Evidence Verification passes.
- [ ] **CI/CD Visibility:** Native GitHub Actions Step Summaries and GitLab Report artifacts.
- [ ] **Supply Chain Security:** SLSA Level 3 compliance for CLI binaries (Signed releases).

### v2.2: The "Evidence Pack" Ecosystem
- [ ] **Framework Detectors:** Auto-configure evidence rules for:
  - **Node.js:** Express, Fastify, NestJS
  - **Python:** Django, FastAPI, Flask
  - **Java:** Spring Boot
- [ ] **Cloud Scanners:** Expand IaC scanning to include AWS CDK and Azure Bicep.

---

## 🔭 Future Vision: v3.0 (Compliance Platform)

**Goal:** A unified interface for Security, Engineering, and Auditors.

- [ ] **PDF/Docx Export:** One-click generation of audit artifacts for external auditors.
- [ ] **Policy Registry:** Centralized repository of community-maintained `evidence.yml` rules.
- [ ] **IDE Plugin:** Real-time ASVS feedback in VS Code / IntelliJ (e.g., "This route lacks auth checks").

---

## 💡 How to Contribute

We prioritize features that move security **left**. Check our [Issues](https://github.com/kaademos/asvs-compliance-starter-kit/issues) board:
- `good first issue`: Documentation and simple pattern matchers.
- `help wanted`: New framework adapters for the Evidence Verifier.

*Roadmap last updated: Q1 2026*