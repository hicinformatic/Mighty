from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import Permission

from mighty.models import user as models
from mighty.apps.user.admin import NationalityAdmin, UserAdmin

nationality_inlines = []
user_inlines = []

if 'mighty.apps.extend' in settings.INSTALLED_APPS:
    from mighty.apps.extend.admin import ExtendAdminInline, HistoryAdminInline

    class NationalityExtendAdminInline(ExtendAdminInline):
        model = models.NationalityExtend
    class NationalityHistoryAdminInline(HistoryAdminInline):
        model = models.NationalityHistory
    nationality_inlines = [NationalityExtendAdminInline, NationalityHistoryAdminInline]

    class UserExtendAdminInline(ExtendAdminInline):
        model = models.UserExtend
    class UserHistoryAdminInline(HistoryAdminInline):
        model = models.UserHistory
    user_inlines = [UserExtendAdminInline, UserHistoryAdminInline]

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Nationality)
class NationalityAdmin(NationalityAdmin):
    inlines = nationality_inlines

@admin.register(models.User)
class UserAdmin(UserAdmin):
    inlines = user_inlines