FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for build)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Install dependencies
COPY pyproject.toml .
# Install basic + evidence + verification deps
RUN pip install .[evidence,verification]

# Copy source code
COPY tools/ ./tools/
COPY policies/ ./policies/
COPY 01-ASVS-Core-Reference/ ./01-ASVS-Core-Reference/
# Copy templates for init wizard
COPY 00-Documentation-Standards/ ./00-Documentation-Standards/

# Set up entrypoint
ENTRYPOINT ["python", "-m"]
CMD ["tools.compliance_gate", "--help"]