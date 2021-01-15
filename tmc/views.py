# from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, resolve_url
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from .forms import TMCQueryForm
from .models import TMC
from .utils import get_tmcs


# Create your views here.
class TMCQueryView(generic.FormView):
    form_class = TMCQueryForm
    template_name = 'tmc/tmc_query.html'

    def get_success_url(self):
        return resolve_url('tmc-query')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            data = form.cleaned_data
            credit_amount = data['credit_amount']
            credit_term = data['credit_term']
            overdue_days = data['overdue_days']
            date = data['date']
            credit_total_days = credit_term + overdue_days
            if credit_total_days < 90:
                if credit_amount <= 5000:
                    tmc_type_code = 26
                    pass
                else:
                    tmc_type_code = 25
                    pass
            else:
                if credit_amount <= 50:
                    tmc_type_code = 45
                    pass
                elif credit_amount <= 200:
                    tmc_type_code = 44
                    pass
                elif credit_amount <= 5000:
                    tmc_type_code = 35
                    pass
                else:
                    tmc_type_code = 34
                    pass
            tmc = TMC.objects.filter(tmc_type__code=tmc_type_code, start_date__lte=date, end_date__gte=date).first()
            if not tmc:
                get_tmcs(date)
                tmc = TMC.objects.filter(tmc_type__code=tmc_type_code, start_date__lte=date, end_date__gte=date).first()
            if tmc:
                tmc_value = tmc.value
                credit_tmc = round(credit_amount * (tmc_value / 100), 2)
                credit_with_tmc = credit_amount + credit_tmc
                tmc_type_desc = str(tmc)
                print(tmc_type_code, credit_amount, credit_tmc, credit_with_tmc)
                kwargs.update({
                    'query_result': _('OK'),
                    'tmc_type_code': tmc_type_code,
                    'tmc_type_value': tmc_value,
                    'credit_amount': credit_amount,
                    'credit_tmc': credit_tmc,
                    'credit_with_tmc': credit_with_tmc,
                    'tmc_type_desc': tmc_type_desc,
                })
                print(args)
            else:
                messages.error(request, _('TMC Not Found'))
                kwargs.update({
                    'query_result': _('TMC Not Found')
                })
                print(tmc_type_code, _('TMC Not Found'), )
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context=context)
        return super().post(request, *args, **kwargs)
