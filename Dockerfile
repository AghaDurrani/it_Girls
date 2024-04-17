FROM artifactory.sofa.dev/docker-local/ubi8/python38-dev as build


ARG ARTIFACTORY_USER
ARG ARTIFACTORY_PASS
ARG PIP_INDEX_URL=https://artifactory.sofa.dev/artifactory/api/pypi/pypi-remote/simple
ARG PIP_EXTRA_INDEX_URL= https://artifactory.sofa.dev/artifactory/api/pypi/pypi-local/simple


WORKDIR /app


COPY . .

RUN pip install --user -i $PIP_INDEX_URL --extra-index-url $PIP_EXTRA_INDEX_URL -r requirements.txt --no-cache-dir
EXPOSE 8501

CMD [ "streamlit", "run", "app/Home.py" ]
