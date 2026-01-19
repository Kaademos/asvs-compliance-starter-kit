# Troubleshooting

## Common Errors

### 1. `ModuleNotFoundError: No module named 'tools'`
**Cause:** You are running the script from outside the project root or the python path is incorrect.
**Fix:** Always run commands from the root of the repository using `python -m`:
```bash
# Correct
python -m tools.compliance_gate ...

# Incorrect
python tools/compliance_gate.py

```

### 2. `ValueError: Target URL is not allowed (SSRF Protection)`

**Cause:** You are trying to scan `localhost`, `127.0.0.1`, or a private IP address with the Verification Suite.
**Fix:** Add the `--allow-local` flag to your command.

```bash
python -m tools.verification_suite --target-url http://localhost:3000 --allow-local

```

### 3. Docker: "File not found" inside container

**Cause:** The volume mount is incorrect, or you are referencing a relative path that doesn't exist inside `/app` in the container.
**Fix:** Ensure you are mounting your current directory to `/app`.

```bash
# Linux/Mac
docker run -v $(pwd):/app asvs-engine ...

# Windows (PowerShell)
docker run -v ${PWD}:/app asvs-engine ...

```

### 4. `KeyError` in Report Generation

**Cause:** One of the input JSON files (`gate.json` or `verify.json`) is empty or malformed.
**Fix:** Check the output of the previous commands. Did `compliance_gate` actually produce JSON?

```bash
# Verify content
cat gate.json

```

## Getting Help

If you encounter an issue not listed here:

1. Run the command with `--help` to see available options.
2. Check the [Issues](https://github.com/kaademos/asvs-compliance-starter-kit/issues) tracker.
3. Open a **Bug Report** with the output of your command and the version of Python you are using.

```