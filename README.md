Welcome to UMUNC!
===================

This is the online system for UMUNC.

----------


Apps
-------------

Now this project contains 4 mainly apps/modules:

####**UMUNC-CORE** (/umunc)
Basic core of system, including settings, common modules and main url config;

####**UMUNC-STATIC** (/umunc_static)
Static files; 

####**UMUNC-IRIS** (/umunc_iris)
User center apps; 

####**UMUNC_CHEETAH** (/umunc_cheetah)
Live chat apps;

----------


Installation
-------------------

Sync databases by using: **python manage.py syncdb** and install it via Apache, mod_wsgi and python2. 
Seeing [Django Documentations](https://docs.djangoproject.com/en/1.7/).

> **Tips:**
> - cache files path: /www/cache/
> - Upload files path: /www/upload/


----------


Environment
-------------

#####**Python2** 
#####**Python2 modules**

 - simplejson
 - mod-wsgi
 - mysqldb
#####**Database** (Mysql/MariaDB)
#####**Django 1.5+**
> **Tips:**
>  Not sure if Django1.7 will support this project currectly.

### Support

[eastpiger](www.eastpiger.com) ~ 2015
![enter image description here](https://raw.githubusercontent.com/UMUNC/UMUNC/master/umunc_static/common/image/UMUNC-logo-white.png)
