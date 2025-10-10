# Security Decision: Authorization Strategy

| | |
| :--- | :--- |
| **Project Name:** | `[Project Name]` |
| **Document Owner:** | `[e.g., Lead Engineer, Architect]` |
| **Date:** | `YYYY-MM-DD` |
| **Status:** | `Draft | In Review | Approved` |

---

## 1. Applicable ASVS Requirements

This document addresses the high-level design decisions for the following ASVS 5.0 requirements:

* **V8.1.1:** Define rules for function-level and data-specific access.
* **V8.1.2:** Define rules for field-level access restrictions.
* **V8.1.3:** Define environmental and contextual attributes used for security decisions.
* **V8.1.4:** Define how environmental and contextual factors are used in decision-making.

---

## 2. Authorization Model

Describe the primary authorization model used by the application.

* [ ] **Role-Based Access Control (RBAC):** Access is granted based on user roles (e.g., Admin, User, Viewer).
* [ ] **Attribute-Based Access Control (ABAC):** Access is granted based on policies combining user attributes, resource attributes, and environmental conditions.
* [ ] **Other (Please Specify):** `[e.g., Relationship-Based, Custom]`

---

## 3. Function-Level and Data-Level Access Rules (V8.1.1)

This table defines which roles/attributes can perform actions on specific application functions or data resources. This is the primary defense against Insecure Direct Object Reference (IDOR) and Broken Function Level Authorization.

| Role / Attribute | Function / Resource | Allowed Actions | Justification |
| :--- | :--- | :--- | :--- |
| `e.g., Admin` | `/api/v1/users/{userId}` | `GET`, `PUT`, `DELETE` | Admins can manage all users. |
| `e.g., User (Owner)` | `/api/v1/users/{userId}` | `GET`, `PUT` | A user can view and edit their own profile. |
| `e.g., User (Non-Owner)`| `/api/v1/users/{userId}` | `GET` | A user can view another user's public profile. |
| `e.g., User` | `/api/v1/billing` | `GET`, `POST` | Users can manage their own billing info. |
| `e.g., Anonymous` | `/api/v1/products` | `GET` | Anyone can browse products. |

---

## 4. Field-Level Access Rules (V8.1.2)

This table defines read/write permissions for specific fields within a data object to prevent Broken Object Property Level Authorization (BOPLA).

| Role / Attribute | Data Object / Model | Field Name | Permissions | Conditions / Notes |
| :--- | :--- | :--- | :--- | :--- |
| `e.g., Admin` | `User` | `is_admin` | `Read`, `Write` | |
| `e.g., User` | `User` | `is_admin` | `Read-Only` | Users can see their admin status but not change it. |
| `e.g., User` | `User` | `password_hash` | `None` | The password hash should never be exposed via an API. |
| `e.g., User` | `User` | `email` | `Read`, `Write` | |
| `e.g., Support Staff` | `User` | `email` | `Read-Only` | Support can view user emails for verification. |

---

## 5. Contextual Attributes & Adaptive Access (V8.1.3 & V8.1.4)

This section documents environmental factors used for adaptive authorization decisions (primarily for ASVS L3).

**Attributes Considered:**
* [ ] **IP Address / Geolocation:** (e.g., Is it from a corporate network? Is it from a new country?)
* [ ] **Time of Day:** (e.g., Is the request happening outside of normal business hours?)
* [ ] **Device Fingerprint:** (e.g., Is this a recognized user device?)
* [ ] **User Behavior:** (e.g., Has the user's velocity of requests changed abnormally?)
* [ ] **Other:** `[Specify]`

**Decision Logic:**
* **Example 1:** If a user with the `Admin` role attempts to log in from an unrecognized IP address, require **step-up authentication** (e.g., re-enter password + MFA).
* **Example 2:** If a user attempts to perform a sensitive transaction (e.g., change billing details) outside of their typical country of access, **block the request** and notify the user.
* **Example 3:** `[Your Logic Here]`