FROM python:2.7.12

MAINTAINER tecnologia@scielo.org

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r /app/requirements.txt

ADD docker/entrypoint.sh /app/docker/entrypoint.sh
RUN chmod +x /app/docker/entrypoint.sh