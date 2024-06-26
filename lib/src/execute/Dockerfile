FROM malevichai/app:python11_v0.1

RUN apt update && apt install -y git
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN malevich dev in-app-install
COPY apps/ apps/