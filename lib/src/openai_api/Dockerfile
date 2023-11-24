FROM pogrebnoijak/julius_export_python:0.1

COPY requirements.txt requirements.txt
RUN if test -e requirements.txt; then pip install --no-cache-dir -r requirements.txt; fi

COPY ./ ./apps
