FROM pogrebnoijak/julius_export_python11:0.1

RUN apt install -y libgdiplus wget \
 && wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
 && dpkg -i ./libssl1.1_1.1.0g-2ubuntu4_amd64.deb \
 && rm -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb


RUN pip install aspose-words
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

COPY ./apps ./apps