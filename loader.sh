python2 makeconf.py > umunc/CONFIG.py
python2 manage.py migrate

service nginx start
nohup gunicorn umunc.wsgi:application -b 127.0.0.1:8080
