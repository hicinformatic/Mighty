from django.urls import include, path

from mighty import fields
from mighty.admin.site import fset_default, fset_infos, OverAdmin, InErrorListFilter, InAlertListFilter
from mighty.apps.grapher import fields
from mighty.apps.grapher import _

class TemplateAdmin(OverAdmin):
    fieldsets = (((None, {'fields': fields.template})),
        ("Options", {'classes': ('collapse',), 'fields': fields.template_options}),
        ("Large", {'classes': ('collapse',), 'fields': fields.template_lg}),
        ("Medium", {'classes': ('collapse',), 'fields': fields.template_md}),
        ("Small", {'classes': ('collapse',), 'fields': fields.template_sm}),
        (fset_default),
        (fset_infos),)
    list_filter = (InErrorListFilter, InAlertListFilter)
    list_display = ('name', 'uid')

class GraphAdmin(OverAdmin):
    fieldsets = (((None, {'fields': fields.graph})),
        ("Options", {'classes': ('collapse',), 'fields': fields.graph_options}),
        ("Size", {'classes': ('collapse',), 'fields': fields.graph_size}),
        (_.c_bar, {'classes': ('collapse',), 'fields': ('bar_values',) }),
        (_.c_bipolar, {'classes': ('collapse',), 'fields': ('bipolar_values',) }),
        (_.c_funnel, {'classes': ('collapse',), 'fields': ('funnel_values',) }),
        (_.c_gauge, {'classes': ('collapse',), 'fields': ('gauge_values',) }),
        (_.c_horizontalbar, {'classes': ('collapse',), 'fields': ('horizontalbar_values',) }),
        (_.c_horizontalprogressbars, {'classes': ('collapse',), 'fields': ('horizontalprogressbars_values',) }),
        (_.c_line, {'classes': ('collapse',), 'fields': ('line_values',) }),
        (_.c_pie, {'classes': ('collapse',), 'fields': ('pie_values',) }),
        (_.c_radar, {'classes': ('collapse',), 'fields': ('radar_values',) }),
        (_.c_rose, {'classes': ('collapse',), 'fields': ('rose_values',) }),
        (_.c_scatter, {'classes': ('collapse',), 'fields': ('scatter_values',) }),
        (_.c_semicircularprogressbars, {'classes': ('collapse',), 'fields': ('semicircularprogressbars_values',) }),
        (_.c_verticalprogressbars, {'classes': ('collapse',), 'fields': ('verticalprogressbars_values',) }),
        (_.c_waterfall, {'classes': ('collapse',), 'fields': ('waterfall_values',) }),
        (_.c_donut, {'classes': ('collapse',), 'fields': ('donut_values',) }),
        (_.c_gantt, {'classes': ('collapse',), 'fields': ('gantt_values',) }),
        (_.c_meter, {'classes': ('collapse',), 'fields': ('meter_values',) }),
        (_.c_odometer, {'classes': ('collapse',), 'fields': ('odometer_values',) }),
        (_.c_radialscatter, {'classes': ('collapse',), 'fields': ('radialscatter_values',) }),
        (_.c_thermometer, {'classes': ('collapse',), 'fields': ('thermometer_values',) }),
        (fset_default),
        (fset_infos),)
    list_filter = (InErrorListFilter, InAlertListFilter)
    list_display = ('title', 'svg_url_html', 'canvas_url_html')
    filter_horizontal = ('templates',)