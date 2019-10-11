from django.contrib import admin
from django.conf import settings

from mighty.models import nationality as models
from mighty.apps.nationality.admin import NationalityAdmin

nationality_inlines = []
if 'mighty.apps.extend' in settings.INSTALLED_APPS:
    from mighty.apps.extend.admin import ExtendAdminInline, HistoryAdminInline

    class NationalityExtendAdminInline(ExtendAdminInline):
        model = models.NationalityExtend

    class NationalityHistoryAdminInline(HistoryAdminInline):
        model = models.NationalityHistory
    nationality_inlines = [NationalityExtendAdminInline, NationalityHistoryAdminInline]

@admin.register(models.Nationality)
class NationalityAdmin(NationalityAdmin):
    inlines = nationality_inlines