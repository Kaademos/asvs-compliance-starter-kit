# Security Decision: Data Classification & Protection

| | |
| :--- | :--- |
| **Project Name:** | `[Project Name]` |
| **Document Owner:** | `[e.g., Data Protection Officer, Architect]` |
| **Date:** | `YYYY-MM-DD` |
| **Status:** | `Draft | In Review | Approved` |

---

## 1. Applicable ASVS Requirements

This document addresses the high-level design decisions for the following ASVS 5.0 requirements:

* **V14.1.1:** Identify and classify all sensitive data into protection levels.
* **V14.1.2:** Document the protection requirements for each classification level.

---

## 2. Data Classification Levels

This organization defines the following levels of data sensitivity:

* **Public:** Information intended for public consumption. Its disclosure would cause no harm.
* **Internal:** Information for internal employees and authorized contractors. Unauthorized disclosure would have a minimal negative impact.
* **Confidential:** Sensitive business or personal data. Unauthorized disclosure could have a significant negative impact on the company, its partners, or its users.
* **Restricted:** The most sensitive data, including trade secrets, authentication secrets, and highly regulated data. Unauthorized disclosure could have a critical or catastrophic impact.

---

## 3. Data Inventory & Classification (V14.1.1)

This table serves as the inventory of all sensitive data elements handled by the application.

| Data Element | Description / Context | Storage Location(s) | Classification Level |
| :--- | :--- | :--- | :--- |
| `e.g., User Password` | User's authentication credential. | `Database (users table)` | **Restricted** |
| `e.g., Session Token` | Token used to maintain user session. | `Browser Cookie, Cache` | **Restricted** |
| `e.g., User Email` | User's contact and login identifier. | `Database, Logs, Cache` | **Confidential** |
| `e.g., Credit Card PAN` | Primary Account Number for payments. | `[N/A - Sent to processor]` | **Restricted** |
| `e.g., User Profile Bio` | Publicly viewable user biography. | `Database` | **Public** |
| `e.g., Internal Feature Flag`| Configuration for a new feature. | `Config File, Database` | **Internal** |
| `e.g., API Keys (Internal)`| Keys for backend service communication.| `Secrets Manager` | **Restricted** |

---

## 4. Protection Requirements per Level (V14.1.2)

This matrix defines the minimum security controls required for each data classification level.

| Control | Public | Internal | Confidential | Restricted |
| :--- | :--- | :--- | :--- | :--- |
| **Encryption in Transit** | Recommended | **Required** (TLS 1.2+) | **Required** (TLS 1.2+) | **Required** (TLS 1.3 preferred) |
| **Encryption at Rest** | N/A | Recommended | **Required** (e.g., AES-256) | **Required** (e.g., AES-256) |
| **Logging Policy** | Log access events. | Log access events. | Log access; mask/redact data.| **Do not log** value. Log access events only. |
| **Data Retention** | Indefinite | Indefinite | `[e.g., 7 years]` | `[e.g., 30 days]` or as needed. |
| **Access Control** | Anonymous | Authenticated | Authorized | Strictly Authorized (Least Privilege) |
| **Other** | - | - | e.g., Data Masking in UI | e.g., Stored in HSM / Vault |