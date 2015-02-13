UMUNC v2
===================================  
Online system for UMUNC

Apps
-----------------------------------  
/umunc:[UMUNC-CORE] Basic core of system, including settings, common modules and main url config;
/umunc_static:[UMUNC-STATIC] Static files;
/umunc_iris:[UMUNC-IRIS] User center apps;
/umunc_cheetah:[UMUNC_CHEETAH] Live chat apps;


Installation  
-----------------------------------  
Sync databases by using:
		python manage.py syncdb
install via Apache, mod_wsgi and python2. Seeing Django documents.

Tips:
	cache files path: /www/cache/
	Upload files path: /www/upload/
