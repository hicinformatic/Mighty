from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mighty import fields
from mighty.admin.site import fset_default, fset_infos, OverAdmin, InErrorListFilter, InAlertListFilter
from mighty.apps.user import models, _
from mighty.apps.user.apps import UserConfig as conf
from mighty.apps.user.forms import UserCreationForm

class NationalityAdmin(OverAdmin):
    fieldsets = (((None, {'fields': ('country', 'alpha2', 'alpha3', 'numeric')})),
                (fset_default),
                (fset_infos),)
    list_filter = (InErrorListFilter, InAlertListFilter) + fields.list_filter

class UserAdmin(OverAdmin, UserAdmin):
    add_form = UserCreationForm
    add_fieldsets = ((None, {
            'classes': ('wide',),
            'fields': (conf.Field.username,) + conf.Field.required + ('password1', 'password2')}),)
    fieldsets = (((None, {'fields': ('username', 'password', 'method')})),
                (_.a_personal_info, {'fields': ('email', 'phone', 'first_name', 'last_name', 'gender', 'nationalities')}),
                (_.a_permissions, {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                (_.a_api, {'fields': ('key', 'tokens', 'codes')}),
                (_.a_importante_dates, {'fields': ('last_login', 'date_joined')}),
                (_.a_ip, {'fields': ('ipv4', 'ipv6', 'sign')}),
                (fset_default),
                (fset_infos),)
    filter_horizontal = ('groups', 'user_permissions', 'nationalities')
    readonly_fields = fields.readonly_fields + ('key', 'tokens', 'codes', 'ipv4', 'ipv6', 'sign') 
    list_display = fields.list_display + ('email', 'gender', 'ipv4', 'ipv6') 
    list_filter = (InErrorListFilter, InAlertListFilter) + fields.list_filter + ('is_active', 'gender', 'is_staff', 'is_superuser')
    search_fields = fields.search_fields + ('email', 'ipv4', 'ipv6')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.method = models.METHOD_BACKEND
        super().save_model(request, obj, form, change)