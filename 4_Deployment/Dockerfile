# Use a slim Python image for efficiency
FROM python:3.10-slim

# Upgrade pip and install uv
RUN pip install -U pip
COPY --from=ghcr.io/astral-sh/uv:0.5.30 /uv /uvx /bin/
# RUN pip install uv

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency files
COPY ["pyproject.toml", "uv.lock", "./"]

# ENV UV_PROJECT_ENVIRONMENT="/usr/local"
RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Copy the application files
COPY ["4_Deployment/predict.py", "./"]
COPY ["4_Deployment/models/lin_reg.bin", "./models/"]

# Expose port 9696 for incoming requests
EXPOSE 9696

# Define the entrypoint command to run the app using Gunicorn
ENTRYPOINT ["gunicorn", "--workers=4", "--bind=0.0.0.0:9696", "predict:app"]
