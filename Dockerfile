# Build stage using Debian slim image from a remote Artifactory repository

FROM artifactory.sofa.dev/docker-remote/debian:12-slim as build


# Arguments for connecting to Artifactory
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASS

FROM python:3.10 as final


# Setting the working directory
WORKDIR /app

# Copying all files from the context to the working directory in the container
COPY . .
RUN pip install --upgrade pip && \
    pip install -i https://artifactory.sofa.dev/artifactory/api/pypi/pypi-remote/simple --extra-index-url https://artifactory.sofa.dev/artifactory/api/pypi/pypi-local/simple -r requirements.txt --no-cache-dir
RUN pip install -r requirements.txt


# Exposing the port that the app will run on
EXPOSE 8501

# Command to run the application using Streamlit
CMD ["streamlit", "run", "app.py"]
