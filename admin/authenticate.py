from django.contrib import admin

from mighty.models.authenticate import Email, Sms
from mighty.apps.authenticate.admin import EmailAdmin, SmsAdmin

@admin.register(Email)
class EmailAdmin(EmailAdmin):
    pass

@admin.register(Sms)
class SmsAdmin(SmsAdmin):
    pass