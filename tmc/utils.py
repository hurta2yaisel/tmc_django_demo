from __future__ import absolute_import, division, generators, nested_scopes, \
    print_function, unicode_literals, with_statement

import logging
import os
import sys
import time
from datetime import datetime

import django
import requests
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)
APP_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tmc_django_demo.settings'
    django.setup()

from tmc.models import TMCType, TMC

# API_KEY = 'f38af6ad37a9f672722eddb3add57c6941df8681'
API_KEY = '9c84db4d447c80c74961a72245371245cb7ac15f'
API_FORMAT = 'json'
API_PARAMS = "?apikey={api_key}&formato={api_format}".format(api_key=API_KEY, api_format=API_FORMAT)
API_URL = 'https://api.sbif.cl/api-sbifv3/recursos_api/'
# API_URL = 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/2020/06?'

# API_INDICATORS = ('dolar', 'uf', 'utm', 'euro','tmc')
API_INDICATORS = ('tmc',)

USER_AGENT = 'TMC Django Demo https://secure.cumplo.cl'
SESSION = requests.session()


def print_r(string):
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(stamp, string)


def update_headers():
    global SESSION

    SESSION.headers.update({
        'User-Agent': USER_AGENT,
        'Referer': 'https://secure.cumplo.cl',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    })
    return SESSION.headers


def log_error(e):
    try:
        print(e)
        os.makedirs('logs', exist_ok=True)
        log_file_name = "logs/"
        if os.name == 'nt':
            log_file_name = "logs\\"

        logger = logging.getLogger(__name__)

        log_format = ";%(levelname)s %(process)d %(message)s"
        log_file_name = '{path}log-{date}.txt'.format(path=log_file_name, date=datetime.now().strftime('%Y-%m-%d'))

        file_handler = logging.FileHandler(log_file_name, encoding='UTF-8')

        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)

        logger.addHandler(logging.FileHandler(log_file_name))
        logger.error("{message}".format(
            message='{error} {date}'.format(date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), error=str(e))
        ))
    except Exception as e2:
        pass


def get_tmcs(query_date=datetime.today().date(), before=False):
    try:
        print("1. Obteniendo indicadores desde: " + API_URL)
        tries = 3
        msg_slug = None
        while tries > 0:
            try:
                year = query_date.year
                month = query_date.month
                day = query_date.day
                if day <= 14:
                    if month > 1:
                        month -= 1
                    else:
                        month = 12
                        year -= 1

                url_request = '{api}tmc/{before}{year}/{month}{params}'.format(
                    api=API_URL,
                    year=year,
                    month=month,
                    params=API_PARAMS,
                    before='anteriores/' if before else ''
                )
                response = SESSION.get(url_request)

                if response.status_code < 400:
                    # OK
                    try:
                        tmcs = response.json()['TMCs']
                        tmc_codes = []
                        for tmc in tmcs:
                            title = tmc['Titulo']
                            subtitle = tmc['SubTitulo']
                            value = tmc['Valor']
                            start_date = tmc['Fecha']
                            end_date = tmc.get('Hasta', None)
                            if not end_date:
                                end_date = datetime.strptime(
                                    start_date,
                                    '%Y-%m-%d'
                                ).date() + relativedelta(months=1)
                                end_date = end_date.replace(day=14)

                            code = int(tmc['Tipo'])
                            if title and 'Operaciones no reajustables' in title:
                                tmc_codes.append(code)
                                try:
                                    tmc_type = TMCType.objects.get(code=code)
                                except TMCType.DoesNotExist:
                                    tmc_type = TMCType()
                                tmc_type.code = code
                                tmc_type.title = title
                                tmc_type.subtitle = subtitle
                                tmc_type.save()
                                try:
                                    TMC.objects.get(tmc_type=tmc_type, start_date=start_date)
                                except TMC.DoesNotExist:
                                    print(tmc)
                                    tmc_obj = TMC()
                                    tmc_obj.tmc_type = tmc_type
                                    tmc_obj.value = value
                                    tmc_obj.start_date = start_date
                                    tmc_obj.end_date = end_date
                                    tmc_obj.save()

                        print(sorted(set(tmc_codes)))
                        msg_slug = None
                        print(min(tmc_codes), '-', max(tmc_codes))
                    except Exception as e:
                        print_r("Ups: {error}".format(error=e))
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        exc_type = str(exc_type).split("'")[1]
                        msg_slug = '%s: %s: %s. %s' % (exc_type, fname, exc_tb.tb_lineno, e)
                        log_error(msg_slug)
                    break
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                exc_type = str(exc_type).split("'")[1]
                msg_slug = '%s: %s: %s. %s' % (exc_type, fname, exc_tb.tb_lineno, e)
                time.sleep(1)
            tries -= 1
        if tries == 0 and msg_slug:
            log_error(msg_slug)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        exc_type = str(exc_type).split("'")[1]
        msg_slug = '%s: %s: %s. %s' % (exc_type, fname, exc_tb.tb_lineno, e)
        log_error(msg_slug)


def main():
    get_tmcs(before=True)


if __name__ == '__main__':
    main()
