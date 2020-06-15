# Instalar dependencias con pipenv o con pip
# Instalar Reddis Server

# Database (borrar previamiente la base de datos, para probar el proceso
python manage.py makemigrations
python manage.py migrate

# Static files and i18n
python manage.py makemessages -l es -l en --no-location --no-obsolete
python manage.py compilemessages

# Obtener las TMCs
python manage.py update-all-tmc

# Ejecutar Celery. La tarea esta configurada para que se ejecute los dias 15
# de cada mes.

cd /path/to/tmc_django_demo

celery -A tmc_django_demo.celery_run worker -l info -B

# Ejecutar la demo
python manage.py runserver

Cualquier duda contactarme en hurta2yaisel@gmail.com.
