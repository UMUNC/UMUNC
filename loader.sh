python2 makeconf.py > umunc/CONFIG.py
python2 manage.py migrate

nohup gunicorn umunc.wsgi:application -b 127.0.0.1:8080&
service nginx start

while true
do
    sleep 1
done
