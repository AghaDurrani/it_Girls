# streamlit-template

**A template to quickly build a Streamlit app and deploy it to AWS**

## Description

This repository contains:
* the [Streamlit demo app](https://docs.streamlit.io/library/get-started/create-an-app), exploring a public Uber dataset for pickups and drop-offs in New York City
* a Dockerfile, containerizing the app to make it instantly runnable and easily deployable
* a Terraform configuration, leveraging IaC to automate deloyment to AWS **(in progress)**
* a Devcontainer/VS Code configuration, allowing for development in [GitHub Codespaces](https://github.com/PRS-STD/codespace-sofa)

## Usage

### Run locally

The following steps assume that you have cloned this repository and have `docker` (or `podman`) installed.

**➡️ Simply open this repository in [GitHub Codespaces](https://github.com/PRS-STD/codespace-sofa), where `docker` will be provided out of the box.**

1. Navigate into the repository: `cd path/to/streamlit-template`
2. Set Streamlit's `config.toml` to local: `cd .streamlit && mv config.toml config-prod.toml && mv config-local.toml config.toml && cd ..`
3. Build an image from the Dockerfile: `docker build . --tag streamlit-template`
4. Pull the image and start the container: `docker run --detach --publish 8501:8501 streamlit-template`
5. Open your browser and go to [localhost:8501](localhost:8501).

### Deploy to AWS

Trigger the execution of the PCS-configured pipeline, which will provision and manage the AWS infrastructure based on the Terraform configuration files.

## Contributors

* [Lucas Konstantin Bärenfänger](mailto:lucas_konstantin.barenfanger.external@ecb.europa.eu)
