from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from mighty import views
from mighty.models.authenticate import Sms
from mighty.apps.authenticate.views import LoginView
from mighty.apps.authenticate.filters import SmsFilter

@method_decorator(permission_required('mighty.view_sms'), name='dispatch')
class SmsList(views.ListView):
    model = Sms
    fields = '__all__'

    def get_queryset(self):
        queryset, q = SmsFilter(self.request)
        return queryset.filter(q)

@method_decorator(permission_required('mighty.view_sms'), name='dispatch')
class SmsDetail(views.DetailView):
    model = Sms
    fields = '__all__'

@method_decorator(permission_required('mighty.add_sms'), name='dispatch')
class SmsCreate(views.CreateView):
    model = Sms
    fields = '__all__'

@method_decorator(permission_required('mighty.change_sms'), name='dispatch')
class SmsUpdate(views.UpdateView):
    model = Sms
    fields = '__all__'

@method_decorator(permission_required('mighty.delete_sms'), name='dispatch')
class SmsDelete(views.DeleteView):
    model = Sms
    fields = '__all__'

@method_decorator(permission_required('mighty.add_sms'), name='dispatch')
class SmsEnable(views.EnableView):
    model = Sms
    fields = '__all__'

@method_decorator(permission_required('mighty.delete_sms'), name='dispatch')
class SmsDisable(views.DisableView):
    model = Sms
    fields = '__all__'

@method_decorator(permission_required('mighty.delete_sms'), name='dispatch')
class SmsCheckStatus(views.DetailView):
    template_name = 'authenticate/check.html'
    model = Sms
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(SmsCheckStatus, self).get_context_data(**kwargs)
        status = self.object.check_status()
        context.update({'status': status})
        return context

@method_decorator(permission_required('mighty.delete_sms'), name='dispatch')
class AdminSmsCheckStatus(SmsCheckStatus):
    template_name = 'authenticate/admin/check.html'

class LoginSms(LoginView):
    template_name = 'authenticate/login/sms.html'