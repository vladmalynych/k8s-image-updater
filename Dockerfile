ARG TAG=3.7.9-slim-buster
FROM python:${TAG}

ENV TZ=Europe/Prague

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /app

RUN apt-get update && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -e app

ENTRYPOINT k8s-pod-updater
