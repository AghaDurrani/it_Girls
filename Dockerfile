# Build stage using Debian slim image from a remote Artifactory repository
# FROM artifactory.sofa.dev/docker-remote/debian:12-slim as build

FROM python:3.10

# Arguments for connecting to Artifactory
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASS



# Setting the working directory
WORKDIR /app

# Copying all files from the context to the working directory in the container
COPY . .

RUN pip install -r requirements.txt


# Exposing the port that the app will run on
EXPOSE 8501

# Command to run the application using Streamlit
CMD ["streamlit", "run", "app.py"]
