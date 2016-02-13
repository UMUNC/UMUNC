FROM daocloud.io/library/django:1.7-python2

MAINTAINER eastpiger

EXPOSE 8080

RUN apt-get update && apt-get install nginx -y
RUN pip install simplejson mysql-python gunicorn

RUN mkdir /UMUNC
RUN mkdir /upload/logs
WORKDIR /UMUNC
COPY . /UMUNC
COPY umunc.conf /etc/nginx/sites-enabled/umunc.conf
RUN chmod +x ./loader.sh

CMD ./loader.sh
