import os

str=''

if os.getenv('CONFIG_DEBUG'):
	str+='''
DEBUG = '''+os.getenv('CONFIG_DEBUG')+'''
'''

if os.getenv('CONFIG_ALLOWED_HOSTS'):
	all_hosts = os.getenv('CONFIG_ALLOWED_HOSTS').split()
	all_hosts = ['\''+i+'\',' for i in all_hosts]
	str+='''
ALLOWED_HOSTS = ['''+' '.join(all_hosts)+''']
'''

if os.getenv('CONFIG_DB_NAME') and os.getenv('CONFIG_DB_USER') and os.getenv('CONFIG_DB_PASSWORD') and os.getenv('CONFIG_DB_HOST'):
	str+='''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': \''''+os.getenv('CONFIG_DB_NAME')+'''\',
        'USER': \''''+os.getenv('CONFIG_DB_USER')+'''\',
        'PASSWORD': \''''+os.getenv('CONFIG_DB_PASSWORD')+'''\',
        'HOST': \''''+os.getenv('CONFIG_DB_HOST')+'''\',
        'PORT': '3306',
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'default',
    }
}
'''

if os.getenv('CONFIG_UPLUAD_DIR'):
	str+='''
UPLUAD_DIR = \''''+os.getenv('CONFIG_UPLUAD_DIR')+'''\'
'''

if os.getenv('CONFIG_UPLUAD_URL'):
	str+='''
UPLUAD_URL = \''''+os.getenv('CONFIG_UPLUAD_URL')+'''\'
'''

if os.getenv('CONFIG_TIME_DIR'):
	str+='''
TIME_DIR = \''''+os.getenv('CONFIG_TIME_DIR')+'''\'
'''

if os.getenv('CONFIG_REFRESH_DIR'):
	str+='''
REFRESH_DIR = \''''+os.getenv('CONFIG_REFRESH_DIR')+'''\'
'''

if os.getenv('CONFIG_COMMITEE_DIR'):
	str+='''
COMMITEE_DIR = \''''+os.getenv('CONFIG_COMMITEE_DIR')+'''\'
'''

if os.getenv('CONFIG_COMMITEE_DIR2'):
	str+='''
COMMITEE_DIR2 = \''''+os.getenv('CONFIG_COMMITEE_DIR2')+'''\'
'''

if os.getenv('CONFIG_REVIEW_DIR'):
	str+='''
REVIEW_DIR = \''''+os.getenv('CONFIG_REVIEW_DIR')+'''\'
'''

if os.getenv('CONFIG_UMUNC_IRIS_REGISTER'):
	str+='''
UMUNC_IRIS_REGISTER = \''''+os.getenv('CONFIG_UMUNC_IRIS_REGISTER')+'''\'
'''

if os.getenv('CONFIG_UMUNC_CHEETAH_ENABLE'):
	str+='''
UMUNC_CHEETAH_ENABLE = \''''+os.getenv('CONFIG_UMUNC_CHEETAH_ENABLE')+'''\'
'''

if os.getenv('CONFIG_EMAIL_HOST') and os.getenv('CONFIG_EMAIL_PORT') and os.getenv('CONFIG_EMAIL_HOST_PASSWORD') and os.getenv('CONFIG_EMAIL_HOST_USER'):
    str+='''
EMAIL_HOST = \''''+os.getenv('CONFIG_EMAIL_HOST')+'''\'
EMAIL_PORT = \''''+os.getenv('CONFIG_EMAIL_PORT')+'''\'
EMAIL_HOST_PASSWORD = \''''+os.getenv('CONFIG_EMAIL_HOST_PASSWORD')+'''\'
EMAIL_HOST_USER = \''''+os.getenv('CONFIG_EMAIL_HOST_USER')+'''\'
DEFAULT_FROM_EMAIL = \''''+os.getenv('CONFIG_EMAIL_HOST_USER')+'''\'
'''

print(str)
