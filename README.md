<div align="center">

# Suptech Analytics App Template

### A template to quickly build and deploy an analytics app for banking supervision

<br>

🚀 **Streamlit demo app**<br>
Quickly build upon Streamlit's boilerplate project<br>

🛠️ **Devcontainer config**<br>
Instantly spin up a cloud-based dev env, including all deps and tools needed<br>

🐳 **Docker container**<br>
Instantly run the project anywhere, in a well-defined container that includes all deps<br>

🏗️ **SOFA CI/CD pipeline**<br>
Instantly deploy to AWS K8s, with all ECB-specific configs already in place

</div>

## 1. Usage

### 1.1. Run locally

Prerequisites:
- Recommended: Open this repository in [GitHub Codespaces](https://github.com/PRS-STD/codespace-sofa), where all deps and tools needed for development are provided out of the box.
- Alternative: Clone this repository and have `docker` (or `podman`) installed.

Build and run:
- Navigate into the repository
  - `cd path/to/streamlit-template`
- Switch to the local Streamlit configuration
  - `cd .streamlit && mv config.toml config-prod.toml && mv config-local.toml config.toml && cd ..`
  - This needs to be undone before deploying to the Shared K8s Cluster on AWS!
- Build an image from the Dockerfile
  - `docker build . --tag streamlit-template`
- Pull the image and start the container
  - `docker run --detach --publish 8501:8501 streamlit-template`
- Open your browser and go to [localhost:8501](localhost:8501).

### 1.2. Deploy to the Shared K8s Cluster on AWS

To deploy the project to ECB's Shared K8s Cluster and obtain a `.tadnet.net` URL, trigger the jobs described below via GitLab.<br>
Note that every job needs to be triggered manually, as it is not necessary or sensible to run every job for every commit.

- Job `create-docker-credentials`
  - Creates a secret on the K8s cluser containing the Artifactory registry credentials
  - Trigger once to store credentials
- Job `build-docker-image`
  - Builds a new Docker image and pushes it to the Artifactory registry
  - Trigger to deploy source code changes
- Job `uninstall-application`
  - Uninstalls the application on the K8s cluster using Helm
  - Trigger before installing an updated version of the application
- Job `install-application`
  - Installs the application on the K8s cluster using Helm
  - Trigger to install an updated version of the application

## 2. Demo

To view a sample deployment of this template, go to https://streamlit-template.k8s.aws.tadnet.net via TaDNet Chrome.

## 3. Contributors

* [Lucas Konstantin Bärenfänger](mailto:lucas_konstantin.barenfanger.external@ecb.europa.eu)
* [Tomas Hroch](mailto:tomas.hroch@ecb.europa.eu)
