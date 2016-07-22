FROM daocloud.io/library/django:1.7-python2

MAINTAINER eastpiger

EXPOSE 8080

RUN apt-get update && apt-get install nginx -y
RUN pip install simplejson mysql-python gunicorn django-classy-tags django-import-export django-suit==0.2.18

RUN mkdir /logs
RUN mkdir /UMUNC
RUN mkdir /cache
RUN mkdir /upload
WORKDIR /UMUNC
COPY . /UMUNC
COPY umunc.conf /etc/nginx/sites-enabled/umunc.conf
RUN chmod +x ./loader.sh

CMD ./loader.sh
