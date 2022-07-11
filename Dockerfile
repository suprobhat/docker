FROM python:3.7-buster

LABEL maintainer="support@inadev.com"

ARG DEBIAN_FRONTEND=noninteractive

COPY ./requirements.txt /opt/

RUN apt-get update && \
    python3 -m pip install --no-cache-dir  -r /opt/requirements.txt && \
    mkdir -p /opt/application/

COPY . /opt/application
EXPOSE 8501
WORKDIR /opt/application

CMD streamlit run streamlit_density.py



