FROM daocloud.io/library/django:1.7-python2

MAINTAINER eastpiger

EXPOSE 8080

RUN apt-get update && apt-get install nginx -y
# RUN pip install simplejson mysql-python gunicorn tablib==0.11.2 django-classy-tags==0.7.0 django-import-export==0.7.0 django-suit==0.2.18

RUN mkdir /logs
RUN mkdir /UMUNC
RUN mkdir /cache
RUN mkdir /upload
RUN mkdir /upload/cheetah
RUN mkdir /upload/mpc
WORKDIR /UMUNC
COPY . /UMUNC
RUN pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
COPY umunc.conf /etc/nginx/nginx.conf
RUN chmod +x ./loader.sh

CMD ./loader.sh
