# Configuration Guide

Complete reference for configuring the ASVS Compliance Engine.

## Table of Contents

- [Evidence Manifest (evidence.yml)](#evidence-manifest-evidenceyml)
- [Policy Configuration](#policy-configuration)
- [Environment Variables](#environment-variables)
- [Resource Management](#resource-management)

---

## Evidence Manifest (evidence.yml)

The evidence manifest is the heart of automated compliance verification. It maps ASVS requirements to verifiable evidence in your codebase.

### File Location

The `evidence.yml` file should be placed in your project root:

```
your-project/
├── evidence.yml          # Evidence manifest
├── src/
├── requirements.txt
└── ...
```

### Basic Structure

```yaml
# evidence.yml
requirements:
  <ASVS_REQUIREMENT_ID>:
    checks:
      - type: <check_type>
        path: <relative_file_path>
        pattern: <regex_pattern>  # For content_match only
```

### Check Types

#### file_exists

Verifies that a specific file exists in your repository.

**Use Cases:**
- Security documentation files
- Configuration files
- Required module presence

**Syntax:**

```yaml
requirements:
  V1.1.1:  # Security Documentation
    checks:
      - type: file_exists
        path: "SECURITY.md"
        
  V1.1.2:  # Threat Model
    checks:
      - type: file_exists
        path: "docs/threat-model.md"
```

#### content_match

Searches a file for a regular expression pattern.

**Use Cases:**
- Verify library dependencies
- Check configuration values
- Validate code patterns

**Syntax:**

```yaml
requirements:
  V6.2.1:  # Password Hashing
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "bcrypt|argon2|scrypt"
        
  V14.4.1:  # Security Headers
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"helmet"'
```

### Complete Examples

#### Python/Django Project

```yaml
# evidence.yml for Django
requirements:
  # V1: Architecture & Design
  V1.1.1:
    checks:
      - type: file_exists
        path: "SECURITY.md"
      - type: file_exists
        path: "docs/architecture.md"

  # V2: Authentication
  V2.1.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "django-allauth|django-auth"
        
  # V3: Session Management
  V3.2.1:
    checks:
      - type: content_match
        path: "settings.py"
        pattern: "SESSION_COOKIE_SECURE\\s*=\\s*True"

  # V6: Password Security
  V6.2.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "bcrypt|argon2-cffi"
      - type: content_match
        path: "settings.py"
        pattern: "PASSWORD_HASHERS.*Argon2|BCrypt"

  # V13: API Security
  V13.1.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "djangorestframework"
      - type: file_exists
        path: "api/authentication.py"

  # V14: HTTP Security
  V14.4.1:
    checks:
      - type: content_match
        path: "settings.py"
        pattern: "SECURE_HSTS_SECONDS"
      - type: content_match
        path: "settings.py"
        pattern: "X_FRAME_OPTIONS"
```

#### Node.js/Express Project

```yaml
# evidence.yml for Express
requirements:
  # V1: Documentation
  V1.1.1:
    checks:
      - type: file_exists
        path: "SECURITY.md"
      - type: file_exists
        path: "docs/api-security.md"

  # V4: Access Control
  V4.1.1:
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"passport"|"express-jwt"'
      - type: file_exists
        path: "src/middleware/auth.js"

  # V5: Input Validation
  V5.1.1:
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"express-validator"|"joi"|"yup"'

  # V6: Password Hashing
  V6.2.1:
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"bcrypt"|"argon2"'

  # V14: Security Headers
  V14.4.1:
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"helmet"'
      - type: content_match
        path: "src/app.js"
        pattern: "helmet\\(\\)"

  # V14: CORS
  V14.5.1:
    checks:
      - type: content_match
        path: "package.json"
        pattern: '"cors"'
      - type: content_match
        path: "src/app.js"
        pattern: "cors\\("
```

#### FastAPI Project

```yaml
# evidence.yml for FastAPI
requirements:
  # V2: Authentication
  V2.1.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "python-jose|pyjwt"
      - type: file_exists
        path: "app/auth/jwt.py"

  # V5: Input Validation
  V5.1.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "pydantic"
      - type: content_match
        path: "app/schemas/"
        pattern: "class.*BaseModel"

  # V6: Password Security
  V6.2.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "passlib|bcrypt|argon2"

  # V13: API Security
  V13.1.1:
    checks:
      - type: file_exists
        path: "app/middleware/rate_limit.py"
      - type: content_match
        path: "requirements.txt"
        pattern: "slowapi|fastapi-limiter"

  # V14: Security Headers
  V14.4.1:
    checks:
      - type: content_match
        path: "requirements.txt"
        pattern: "secure|starlette-secure-cookies"
      - type: file_exists
        path: "app/middleware/security_headers.py"
```

### Pattern Writing Tips

#### Basic Patterns

```yaml
# Exact string match
pattern: "bcrypt"

# Multiple alternatives (OR)
pattern: "bcrypt|argon2|scrypt"

# Version range
pattern: 'helmet.*"\\^[4-9]\\.'

# Configuration value
pattern: "DEBUG\\s*=\\s*False"
```

#### Advanced Patterns

```yaml
# Function call
pattern: "helmet\\(\\)"

# Import statement
pattern: "from\\s+passlib|import\\s+passlib"

# Class definition
pattern: "class\\s+\\w+.*BaseModel"

# Environment variable usage
pattern: "os\\.environ\\.get\\(['\"]SECRET_KEY['\"]\\)"
```

#### Escaping Special Characters

```yaml
# Dot (.)
pattern: "flask\\.security"  # Matches "flask.security"

# Parentheses
pattern: "helmet\\(\\)"      # Matches "helmet()"

# Quotes
pattern: '"helmet"'          # Matches "helmet" in JSON
pattern: "'helmet'"          # Matches 'helmet' in Python
```

### Best Practices

1. **Be Specific:** Target exact files rather than broad patterns
   ```yaml
   # Good
   path: "src/auth/password_hasher.py"
   
   # Too broad
   path: "**/*.py"
   ```

2. **Use OR Patterns:** Accept multiple valid implementations
   ```yaml
   pattern: "bcrypt|argon2|scrypt"  # Any approved hasher
   ```

3. **Comment Your Rules:** Explain why each check matters
   ```yaml
   V6.2.1:  # Password must use memory-hard algorithm
     checks:
       - type: content_match
         path: "requirements.txt"
         pattern: "argon2-cffi"  # Preferred over bcrypt
   ```

4. **Layer Checks:** Combine file existence with content verification
   ```yaml
   V14.4.1:
     checks:
       - type: file_exists
         path: "src/middleware/security.py"
       - type: content_match
         path: "src/middleware/security.py"
         pattern: "X-Content-Type-Options"
   ```

---

## Policy Configuration

Advanced policy configuration via JSON for custom validation rules.

### Policy File Structure

```json
{
  "placeholder_patterns": [
    "[Project Name]",
    "[e.g.,",
    "YYYY-MM-DD",
    "TODO:",
    "FIXME:"
  ],
  "required_documents": {
    "1": [],
    "2": ["V11-Cryptography-Strategy.md"],
    "3": [
      "V11-Cryptography-Strategy.md",
      "V6-Authentication-Strategy.md",
      "V8-Authorization-Rules.md"
    ]
  },
  "min_content_length": 200
}
```

### Options

| Field | Description | Default |
|-------|-------------|---------|
| `placeholder_patterns` | Regex patterns indicating incomplete docs | See below |
| `required_documents` | Docs required per ASVS level | See below |
| `min_content_length` | Minimum bytes for valid content | 100 |

### Default Placeholder Patterns

```json
[
  "[Project Name]",
  "[e.g.,",
  "YYYY-MM-DD",
  "`[.*?]`"
]
```

### Default Required Documents

| Level | Required Documents |
|-------|-------------------|
| 1 | None |
| 2 | V11-Cryptography-Strategy.md |
| 3 | V11-Cryptography-Strategy.md |

### Usage

```bash
asvs verify --level 2 --config policy.json
```

---

## Environment Variables

The CLI respects these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `ASVS_CACHE_DIR` | Resource cache location | `~/.asvs-compliance/resources` |
| `ASVS_GITHUB_TOKEN` | GitHub token for API requests | None |
| `NO_COLOR` | Disable colored output | Not set |

### Example

```bash
# Custom cache location
export ASVS_CACHE_DIR=/opt/asvs-cache
asvs resources --download

# CI environment (no prompts, no color)
export NO_COLOR=1
asvs verify --level 2
```

---

## Resource Management

### Cache Structure

```
~/.asvs-compliance/resources/
├── 00-Documentation-Standards/
│   └── Decision-Templates/
│       ├── V6-Authentication-Strategy.md
│       ├── V7-Session-Management.md
│       └── ...
├── 01-ASVS-Core-Reference/
│   ├── ASVS-5.0-en.json
│   ├── ASVS-L1-Baseline.json
│   └── ...
└── 02-Implementation-Guidance/
    └── Patterns/
        └── ...
```

### Resource Types

| Type | Description | Files |
|------|-------------|-------|
| `templates` | Decision templates | 6 Markdown files |
| `core_reference` | ASVS JSON/CSV | 5 data files |
| `functional_requirements` | Requirements by level | 3 JSON files |
| `patterns` | Implementation guides | 5 Markdown files |

### Checking Status

```bash
asvs resources --status
```

### Downloading

```bash
# Interactive (prompts for confirmation)
asvs resources --download

# Non-interactive (for CI/CD)
asvs resources --download --yes --quiet
```

### Clearing Cache

```bash
asvs resources --clear
```

### Custom Cache Location

```bash
# Use environment variable
export ASVS_CACHE_DIR=/path/to/custom/cache
asvs resources --download
```

---

## Next Steps

- [User Guide](user-guide.md) - Complete CLI reference
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
