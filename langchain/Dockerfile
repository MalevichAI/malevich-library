FROM pogrebnoijak/julius_export_python11:0.1

ENV GIT_BRANCH ${branch}

COPY requirements.txt requirements.txt
RUN if test -e requirements.txt; then pip install --no-cache-dir -r requirements.txt; fi

COPY ./ ./apps
