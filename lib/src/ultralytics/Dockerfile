ARG mode=python
ARG branch

FROM pogrebnoijak/julius_export_python_torch:0.1
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV GIT_BRANCH ${branch}
RUN apt-get update && apt-get install gcc ffmpeg libsm6 libxext6 build-essential cmake libboost-dev libexpat1-dev zlib1g-dev libbz2-dev wget -y
RUN mkdir -p ./apps/weights
RUN wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
RUN mv yolov8n.pt ./apps/weights/yolo.pt

COPY requirements.txt requirements.txt
RUN if test -e requirements.txt; then pip install --no-cache-dir -r requirements.txt; fi

COPY ./apps ./apps