FROM python:3.10

ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASS
ARG PIP_INDEX_URL=https://artifactory.sofa.dev/artifactory/api/pypi/pypi-remote/simple
ARG PIP_EXTRA_INDEX_URL=https://${ARTIFACTORY_USER}:${ARTIFACTORY_PASS}@artifactory.sofa.dev/artifactory/api/pypi/dgis-prs-std-pypi-local/simple


WORKDIR /app

COPY . .

RUN pip install --user -i $PIP_INDEX_URL --extra-index-url $PIP_EXTRA_INDEX_URL -r requirements.txt --no-cache-dir


EXPOSE 8501

CMD [ "streamlit", "run", "app.py" ]
