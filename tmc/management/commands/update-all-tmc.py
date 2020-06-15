from __future__ import absolute_import, unicode_literals

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from tmc.utils import get_tmcs

__author__ = 'Yaisel Hurtado <hurta2yaisel@gmail.com>'
__date__ = '15-06-20'


class Command(BaseCommand):
    help = "This command gets all TMCs data"

    def show_info(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def show_error(self, msg):
        self.stderr.write(self.style.ERROR(msg))

    def show_warn(self, msg):
        self.stdout.write(self.style.WARNING(msg))

    def handle(self, *args, **options):
        try:
            get_tmcs(before=True)
            get_tmcs()
        except Exception as e:
            self.show_error(_('Error getting TMCs. %s' % e))
