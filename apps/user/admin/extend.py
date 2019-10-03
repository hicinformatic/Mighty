from mighty.app.extend.admin import ExtendAdminInline, HistoryAdminInline

class UserExtendAdminInline(ExtendAdminInline):
    model = models.UserExtend

class UserHistoryAdminInline(HistoryAdminInline):
    model = models.UserHistory

class UserAdmin(UserAdmin):
    #inlines = [UserExtendAdminInline, UserHistoryAdminInline]
    fieldsets = (((None, {'fields': ('username', 'password', 'method')})),
            (_.a_personal_info, {'fields': ('email', 'phone', 'first_name', 'last_name', 'gender', 'nationalities', 'related_data')}),
            (_.a_permissions, {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            (_.a_api, {'fields': ('key', 'tokens', 'codes')}),
            (_.a_importante_dates, {'fields': ('last_login', 'date_joined')}),
            (_.a_ip, {'fields': ('ipv4', 'ipv6', 'sign')}),
            (fset_default),
            (fset_infos),)
    readonly_fields = fields.readonly_fields + ('key', 'tokens', 'codes', 'ipv4', 'ipv6', 'sign', 'related_data')