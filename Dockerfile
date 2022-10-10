FROM python:3.9


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create false

COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# RUN poetry install --no-root --no-dev

# see https://python-poetry.org/docs/cli/ for poetry options used
# the --no-root means Do not install the root package (your project).
# this means we include only the packages under [tool.poetry.dependencies] in  metcap-api/app/pyproject.toml
RUN poetry install --no-root --only main


COPY ./app /app
RUN chmod +x run.sh

ENV PYTHONPATH=/app

# This is CRITICAL. Your container will not run without this

RUN mkdir -p /opt/metcap/etc

# COPY /opt/metcap/etc/config.yml /opt/metcap/etc/config.yml
# COPY ./local-dev/database/config/config.yml /opt/metcap/etc/config.yml

CMD ["./run.sh"]