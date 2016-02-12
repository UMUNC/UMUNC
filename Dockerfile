FROM daocloud.io/library/django:1.8.6-python2

MAINTAINER eastpiger


RUN mkdir /UMUNC
WORKDIR /UMUNC
COPY . /UMUNC
RUN pip install simplejson mysql-python gunicorn
RUN python2 makeconf.py
RUN python2 manage.py migrate

EXPOSE 8080

CMD python2 manage.py runserver 0.0.0.0:8080
