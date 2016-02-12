FROM daocloud.io/library/django:1.8.6-python2

MAINTAINER eastpiger

EXPOSE 8080

RUN mkdir /UMUNC
WORKDIR /UMUNC
COPY . /UMUNC
RUN pip install simplejson mysql-python gunicorn


CMD ./loader.sh
