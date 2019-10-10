from django.urls import include, path

from mighty import fields
from mighty.admin.site import fset_default, fset_infos, OverAdmin, InErrorListFilter, InAlertListFilter
from mighty.apps.authenticate.views.authenticate import AdminCheckStatus
from mighty.apps.authenticate import models

class SmsAdmin(OverAdmin):
    fieldsets = (((None, {'fields': ('user', 'status', 'backend', 'response', 'sms')})),)
    list_filter = ('status',)
    readonly_fields = ('user', 'status', 'backend', 'response', 'sms')
    list_display = ('user', 'status')

    def has_add_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urlpatterns = super(SmsAdmin, self).get_urls()
        urlpatternsmore = []
        urlpatternsmore.append(
            path('<int:pk>/change/check/', self.admin_site.admin_view(AdminCheckStatus.as_view()), name='admin-authenticate-check-sms')
        )
        urlpatterns = urlpatternsmore + urlpatterns
        return urlpatterns

class EmailAdmin(OverAdmin):
    fieldsets = (((None, {'fields': ('user', 'status', 'backend', 'response', 'subject', 'html', 'txt')})),)
    list_filter = ('status',)
    readonly_fields = ('user', 'status', 'backend', 'response', 'subject', 'html', 'txt')
    list_display = ('user', 'status', 'date_create', 'date_update')
    
    def has_add_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urlpatterns = super(EmailAdmin, self).get_urls()
        urlpatternsmore = []
        urlpatternsmore.append(
            path('<int:pk>/change/check/', self.admin_site.admin_view(AdminCheckStatus.as_view()), name='admin-authenticate-check-email')
        )
        urlpatterns = urlpatternsmore + urlpatterns
        return urlpatterns