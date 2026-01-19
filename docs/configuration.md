
# Configuration Guide

## Evidence Manifest (`evidence.yml`)

The Evidence Manifest is the heart of the "Active Verification" system. It allows you to map high-level ASVS requirements to specific files or patterns in your codebase.

### File Structure

The file is a YAML dictionary where keys are ASVS Requirement IDs (e.g., `V14.4.1`) and values are lists of checks.

```yaml
requirements:
  <ASVS_ID>:
    checks:
      - type: <check_type>
        path: <relative_file_path>
        pattern: <regex_pattern> (optional)

```

### Supported Check Types

#### 1. `file_exists`

Verifies that a specific security configuration file exists.

**Use Case:** verifying `SECURITY.md` or a specific config file.

```yaml
V1.1.1:
  checks:
    - type: file_exists
      path: ".github/SECURITY.md"

```

#### 2. `content_match`

Searches a file for a specific Regular Expression.

**Use Case:** Verifying a library is installed in `package.json` or `requirements.txt`.

```yaml
V6.2.1: # Password Hashing
  checks:
    - type: content_match
      path: "requirements.txt"
      pattern: "bcrypt|argon2"  # Regex allowing either library
      description: "Must use strong hashing library"

```

### Best Practices

1. **Be Specific:** Don't just check `package.json`. Check for the *specific version* if necessary using regex: `"helmet": "\^4\."`.
2. **Comment Your Rules:** Add comments in the YAML to explain *why* this check satisfies the requirement.
3. **Use OR Logic:** Use regex pipes `|` to allow for multiple acceptable libraries (e.g., `fastapi|flask`).