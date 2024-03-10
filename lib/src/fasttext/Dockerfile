FROM malevichai/app:python11_v0.1

COPY requirements.txt requirements.txt
RUN apt-get install build-essential -y
RUN apt-get install wget -y
RUN mkdir /model && cd /model && wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz 
RUN if test -e requirements.txt; then pip install --no-cache-dir -r requirements.txt; fi

COPY ./ ./apps
