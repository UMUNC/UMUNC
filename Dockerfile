FROM daocloud.io/library/django:1.7-python2

MAINTAINER eastpiger

EXPOSE 8080

RUN mkdir /UMUNC
WORKDIR /UMUNC
COPY . /UMUNC
RUN pip install simplejson mysql-python gunicorn
RUN chmod +x ./loader.sh

CMD ./loader.sh
