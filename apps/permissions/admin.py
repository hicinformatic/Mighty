from django.contrib import admin

from mighty.apps.permissions.models import PermissionAsk

class PermissionAskAdmin(admin.ModelAdmin):
    pass
#    save_on_top = True
#    fieldsets = (((None, {'fields': ('user', 'permission', 'content_type', 'cid', 'cuid', 'status')})),
#                (_.a_infos, {'fields': ('date_create', 'date_update', 'update_by')}))
#    readonly_fields = ('user', 'permission', 'content_type', 'cid', 'cuid', 'date_create', 'date_update', 'update_by')
#    list_filter = ('permission', 'content_type')
#    list_display = ('user', 'content_type', 'permission')
#    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email',
#        'content_type__app_label', 'content_type__model',
#        'permission__codename', 'permission__name')
#
#    def has_add_permission(self, request):
#        return False
#
#    def has_disable_permission(self, request):
#        return False
#
#    def save_model(self, request, obj, form, change):
#        obj.update_by = request.user.username
#        super(PermissionAskAdmin, self).save_model(request, obj, form, change)