from mighty import fields
from mighty.admin.site import fset_default, fset_infos, OverAdmin, InErrorListFilter, InAlertListFilter

from mighty import  _

fset_default = (_.f_default, {'fields': ('display', 'image')})
fset_infos = (_.f_infos, {'fields': (fields.readonly_fields)})

class NationalityAdmin(OverAdmin):
    fieldsets = (((None, {'fields': ('country', 'alpha2', 'alpha3', 'numeric', 'image')})),
                (_.f_infos, {'fields': fields.base + fields.signhash + fields.disable}),)
    list_display = ('country', 'alpha2', 'alpha3', 'numeric', 'image_html') + fields.disable
    list_filter = fields.disable
    readonly_fields = fields.base + fields.signhash + fields.disable