FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
# Install basic + evidence deps
RUN pip install .[evidence,verification]

# Copy tools
COPY tools/ ./tools/
COPY policies/ ./policies/
COPY 01-ASVS-Core-Reference/ ./01-ASVS-Core-Reference/

# Default entrypoint
ENTRYPOINT ["python", "-m", "tools.compliance_gate"]
CMD ["--help"]