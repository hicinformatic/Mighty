from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from mighty import views
from mighty.models.authenticate import Email
from mighty.apps.authenticate.views import LoginView
from mighty.apps.authenticate.filters import EmailFilter

@method_decorator(permission_required('mighty.view_email'), name='dispatch')
class EmailList(views.ListView):
    model = Email
    fields = '__all__'

    def get_queryset(self):
        queryset, q = EmailFilter(self.request)
        return queryset.filter(q)

@method_decorator(permission_required('mighty.view_email'), name='dispatch')
class EmailDetail(views.DetailView):
    model = Email
    fields = '__all__'

@method_decorator(permission_required('mighty.add_email'), name='dispatch')
class EmailCreate(views.CreateView):
    model = Email
    fields = '__all__'

@method_decorator(permission_required('mighty.change_email'), name='dispatch')
class EmailUpdate(views.UpdateView):
    model = Email
    fields = '__all__'

@method_decorator(permission_required('mighty.delete_email'), name='dispatch')
class EmailDelete(views.DeleteView):
    model = Email
    fields = '__all__'

@method_decorator(permission_required('mighty.add_email'), name='dispatch')
class EmailEnable(views.EnableView):
    model = Email
    fields = '__all__'

@method_decorator(permission_required('mighty.delete_email'), name='dispatch')
class EmailDisable(views.DisableView):
    model = Email
    fields = '__all__'

@method_decorator(permission_required('mighty.change_email'), name='dispatch')
class EmailCheckStatus(views.DetailView):
    template_name = 'authenticate/check.html'
    model = Email
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(EmailCheckStatus, self).get_context_data(**kwargs)
        status = self.object.check_status()
        context.update({'status': status})
        return context

class AdminEmailCheckStatus(EmailCheckStatus, views.AdminView):
    template_name = 'authenticate/admin/check.html'

class LoginEmail(LoginView):
    template_name = 'authenticate/login/email.html'