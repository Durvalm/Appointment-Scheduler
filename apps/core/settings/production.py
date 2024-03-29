from .base import *
import dj_database_url

# DATATABASE
prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

DEBUG = True
ALLOWED_HOSTS = ['*']