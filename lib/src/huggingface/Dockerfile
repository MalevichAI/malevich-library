ARG mode=python
ARG branch

FROM malevichai/app:python-torch_v0.1
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV GIT_BRANCH ${branch}
RUN apt-get update && apt-get install gcc ffmpeg libsm6 libxext6 build-essential cmake libboost-dev libexpat1-dev zlib1g-dev libbz2-dev wget -y

COPY requirements.txt requirements.txt
RUN if test -e requirements.txt; then pip install --no-cache-dir -r requirements.txt; fi

COPY ./apps ./apps