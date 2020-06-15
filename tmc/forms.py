from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Reset, Row, Submit
from dateutil.relativedelta import relativedelta
from django import forms
from django.utils.translation import ugettext_lazy as _

__author__ = 'Yaisel Hurtado <hurta2yaisel@gmail.com>'
__date__ = '13-06-20'


class TMCQueryForm(forms.Form):
    credit_amount = forms.IntegerField(label=_('Credit Amount'), min_value=1, required=True)
    credit_term = forms.IntegerField(label=_('Credit Term'), min_value=1, required=True)
    overdue_days = forms.IntegerField(label=_('Overdue Days'), min_value=1, required=True)
    date = forms.DateField(label=_('Date'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date' in self.fields:
            today = datetime.today()
            max_date = today + relativedelta(months=1)
            max_date = max_date.replace(day=14)

            max_year = today.year + 1
            if today.month == 12 and today.day >= 15:
                max_year += 1
            years = range(1999, max_year)
            self.fields['date'].widget = forms.SelectDateWidget(years=years)
            self.fields['date'].widget = forms.TextInput(
                attrs={
                    'type': 'date',
                    'pattern': '\d{4}-\d{2}-\d{2}',
                    'min': '1999-05-07',
                    'max': max_date.strftime('%Y-%m-%d')
                }
            )
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('credit_amount', css_class='form-group col-6'),
                Column('credit_term', css_class='form-group col-6')
            ),
            Row(
                Column('overdue_days', css_class='form-group col-6'),
                Column('date', css_class='form-group col-6')
            ),
            Submit('submit', _('Query')),
            Reset('reset', _('Reset')),
        )

    def clean_date(self):
        today = datetime.today().date()
        date = self.cleaned_data['date']
        # min_date = datetime(2002, 1, 9).date()
        min_date = datetime(1999, 5, 7).date()
        max_date = today + relativedelta(months=1)
        max_date = max_date.replace(day=14)

        if date < min_date or date > max_date:
            raise forms.ValidationError(
                _('date must be between dates {min_date} and {max_date}'
                  .format(min_date=min_date.strftime('%Y-%m-%d'),
                          max_date=max_date.strftime('%Y-%m-%d'))))
        return date
