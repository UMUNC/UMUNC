FROM daocloud.io/library/django:1.8.6-python2

MAINTAINER eastpiger


RUN pip install simplejson mysql-python gunicorn
RUN mkdir /UMUNC
WORKDIR /UMUNC
COPY . /UMUNC
EXPOSE 8000

CMD python2 manage.py runserver 0.0.0.0:8080
