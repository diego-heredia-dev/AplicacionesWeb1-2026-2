FROM ubuntu:22.04

RUN apt-get update && apt-get install -y nano
RUN apt-get install -y python3

COPY config/ /site_config/

VOLUME /config

CMD ["python3", "/site_config/main.py"]
