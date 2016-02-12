python2 makeconf.py > umunc/CONFIG.py
python2 manage.py migrate
python2 manage.py runserver 0.0.0.0:8080
