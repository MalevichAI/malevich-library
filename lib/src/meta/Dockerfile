FROM malevichai/app:python11_v0.1

RUN apt-get install git -y
RUN pip install -U pydantic
RUN pip install -U https://github.com/MalevichAI/malevich/archive/feature/iso-installer.zip
RUN malevich dev in-app-install

COPY  ./apps ./apps