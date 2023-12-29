ARG mode=python
ARG branch

FROM pogrebnoijak/julius_export_python:0.1
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV GIT_BRANCH ${branch}

COPY requirements.txt requirements.txt
RUN if test -e requirements.txt; then pip install --no-cache-dir -r requirements.txt; fi
COPY ./apps ./apps
