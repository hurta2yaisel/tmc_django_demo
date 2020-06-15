# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

__author__ = 'Yaisel Hurtado <hurta2yaisel@gmail.com>'
__date__ = '15-06-20'

logger = get_task_logger(__name__)


@shared_task
def update_all_tmc():
    try:
        call_command('update-all-tmc')
    except Exception as ex:
        logger.exception("Error on task tmc.update_all_tmc: %s" % ex)
