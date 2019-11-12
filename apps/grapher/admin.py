from django.urls import include, path

from mighty import fields
from mighty.admin.site import fset_default, fset_infos, OverAdmin, InErrorListFilter, InAlertListFilter
from mighty.apps.authenticate.views.authenticate import AdminEmailCheckStatus, AdminSmsCheckStatus
from mighty.apps.grapher import fields

class TemplateAdmin(OverAdmin):
    fieldsets = (((None, {'fields': fields.template})),
        (fset_default),
        (fset_infos),)
    list_filter = (InErrorListFilter, InAlertListFilter)
    list_display = ('name', 'uid')

class GraphAdmin(OverAdmin):
    fieldsets = (((None, {'fields': fields.graph})),
        (fset_default),
        (fset_infos),)
    list_filter = (InErrorListFilter, InAlertListFilter)
    list_display = ('title', 'svg_url_html', 'canvas_url_html')
    filter_horizontal = ('templates',)