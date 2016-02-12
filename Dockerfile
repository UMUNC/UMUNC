FROM daocloud.io/library/django:1.7-python2

MAINTAINER eastpiger

EXPOSE 8080

RUN apt-get install nginx
RUN pip install simplejson mysql-python gunicorn

RUN mkdir /UMUNC
WORKDIR /UMUNC
COPY . /UMUNC
COPY umunc.conf /etc/nginx/sites-available/umunc.conf
RUN chmod +x ./loader.sh

CMD ./loader.sh
