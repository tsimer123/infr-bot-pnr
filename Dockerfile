# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.11-slim
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /app
# Копирует все файлы из нашего локального проекта в контейнер
COPY ./src /app/infr-bot-pnr
COPY requirements.txt .

# устанавливаем локаль
RUN apt-get update && \
apt-get install -y locales && \
sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8


RUN groupadd --gid 2000 appgrp && \
    useradd --uid 2000 --gid appgrp --shell /bin/bash --create-home appuser && \
    chown -R appuser:appgrp infr-bot-pnr && \
    echo Europe/Moscow > /etc/timezone && \
    ln -f -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

USER appuser
#ENV LANG ru_RU.UTF-8

RUN pip install --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

WORKDIR /app/infr-bot-pnr
