from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class TMC(models.Model):
    value = models.FloatField(verbose_name=_("Value"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    tmc_type = models.ForeignKey(
    "tmc.TMCType", on_delete=models.CASCADE, verbose_name=_("TMC Type")
)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return "{tmc_type}. {start_date} a {end_date}".format(
            tmc_type=self.tmc_type,
            start_date=self.start_date,
            end_date=self.end_date,
        )

    class Meta:
        unique_together = ('tmc_type', 'start_date')
        verbose_name = _('TMC')
        verbose_name_plural = _('TMCs')


class TMCType(models.Model):
    code = models.IntegerField(verbose_name=_("Code"), unique=True, db_index=True)
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    subtitle = models.CharField(verbose_name=_("Subtitle"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return "{code}. {title}. {subtitle}".format(
            code=self.code,
            title=self.title,
            subtitle=self.subtitle
        )

    class Meta:
        verbose_name = _('TMC Type')
        verbose_name_plural = _('TMC Types')
