release: sh release-tasks.sh
web: gunicorn tmc_django_demo.asgi --log-file -
worker: celery -A tmc_django_demo.celery_run worker -l info -B
