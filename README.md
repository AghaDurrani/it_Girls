# Streamlit Template

**A template to quickly build a Streamlit app and deploy it to AWS**

## 1. Description

🚀 **Streamlit demo app** — Quickly build upon Streamlit's boilerplate project<br>
🛠️ **Devcontainer config** — Instantly spin up a cloud-based dev env, including all deps and tools needed<br>
🐳 **Docker container** — Instantly run the project anywhere, in a well-defined container that includes all deps<br>
🏗️ **SOFA CI/CD pipelines** — Instantly deploy to AWS K8s, with all ECB-specific configs already in place

## 2. Usage

### 2.1. Run locally

Prerequisites:
- Recommended: Open this repository in [GitHub Codespaces](https://github.com/PRS-STD/codespace-sofa), where all deps and tools needed for development are provided out of the box.
- Alternative: Clone this repository and have `docker` (or `podman`) installed.

Build and run:
1. Navigate into the repository: `cd path/to/streamlit-template`
2. Set Streamlit's `config.toml` to local: `cd .streamlit && mv config.toml config-prod.toml && mv config-local.toml config.toml && cd ..`
3. Build an image from the Dockerfile: `docker build . --tag streamlit-template`
4. Pull the image and start the container: `docker run --detach --publish 8501:8501 streamlit-template`
5. Open your browser and go to [localhost:8501](localhost:8501).

### 2.2. Deploy to AWS K8s

To deploy the project to ECB's Shared K8s Cluster and obtain a `.tadnet.net` URL, trigger the stages/jobs described below via GitLab.<br>
Note that every job needs to be triggered manually, as it is not necessary or sensible to run each job for every commit.

Stage `build`:
- Job `build-docker-image` — bla bla bla

Stage `deploy`:
- Job `create-docker-credentials` — bla bla bla
- Job `install-application` — bla bla bla
- Job `uninstall-application` — bla bla bla

## 3. Demo

To view a sample deployment of this template, go to https://streamlit-template.k8s.aws.tadnet.net/ via TaDNet Chrome.

## 4. Contributors

* [Lucas Konstantin Bärenfänger](mailto:lucas_konstantin.barenfanger.external@ecb.europa.eu)
* [Tomas Hroch](mailto:tomas.hroch@ecb.europa.eu)
