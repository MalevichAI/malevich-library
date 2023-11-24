ARG mode=python
ARG branch

FROM pogrebnoijak/julius_export_python:0.1

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install gcc ffmpeg libsm6 libxext6 build-essential cmake libboost-dev libexpat1-dev zlib1g-dev libbz2-dev -y
RUN if test -e requirements.txt; then pip install --no-cache-dir -r requirements.txt; fi

COPY ./apps ./apps
