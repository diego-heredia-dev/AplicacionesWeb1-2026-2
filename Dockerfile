FROM python:3.12

RUN pip install flask

COPY config/ /site_config/
COPY . ./site/

EXPOSE 5000

VOLUME /config

CMD ["python3", "/site/app.py"]

