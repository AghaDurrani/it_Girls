# Build stage using Debian slim image from a remote Artifactory repository
FROM artifactory.sofa.dev/docker-remote/debian:12-slim as build

# Arguments for connecting to Artifactory
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASS

# Setting up environment variables for pip to use Artifactory as index
ENV PIP_INDEX_URL=https://artifactory.sofa.dev/artifactory/api/pypi/pypi-remote/simple
ENV PIP_EXTRA_INDEX_URL=https://artifactory.sofa.dev/artifactory/api/pypi/pypi-local/simple

# Final stage using Python 3.10
FROM python:3.10 as final

# Setting the working directory
WORKDIR /app

# Copying all files from the context to the working directory in the container
COPY . .

# Upgrading pip to the latest version
RUN pip install --upgrade pip

# Installing Python dependencies using pip with Artifactory as the index
RUN pip install -i $PIP_INDEX_URL --extra-index-url $PIP_EXTRA_INDEX_URL -r requirements.txt --no-cache-dir

# Exposing the port that the app will run on
EXPOSE 8501

# Command to run the application using Streamlit
CMD ["streamlit", "run", "app.py"]
