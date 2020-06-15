#!/bin/bash

export DJANGO_SETTINGS_MODULE=tmc_django_demo.settings
python manage.py migrate --noinput
python manage.py update-all-tmc
