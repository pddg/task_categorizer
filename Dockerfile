FROM python:3.7-alpine

RUN apk update && \
    apk add --no-cache \
        postgresql-dev &&\
    pip install --no-cache-dir \
        pipenv=="2018.11.26"

WORKDIR /opt/task_categorizer

COPY . /opt/task_categorizer

RUN apk update && \
    apk add --virtual deps --no-cache \
        musl-dev \
        gcc && \
    pipenv install --system --deploy && \
    apk del deps

CMD ["python3", "manage.py", "runserver"]
