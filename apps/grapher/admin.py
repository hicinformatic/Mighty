from django.urls import include, path

from mighty import fields
from mighty.admin.site import fset_default, fset_infos, OverAdmin, InErrorListFilter, InAlertListFilter
from mighty.apps.authenticate.views.authenticate import AdminEmailCheckStatus, AdminSmsCheckStatus
from mighty.apps.authenticate import models

class GraphAdmin(OverAdmin):
    fieldsets = (((None, {'fields': (
        "title",
        "Bar",
        "Bipolar",
        "Funnel",
        "Gauge",
        "HorizontalBar",
        "HorizontalProgressbars",
        "Line",
        "Pie",
        "Radar",
        "Rose",
        "Scatter",
        "SemicircularProgressbars",
        "VerticalProgressbars",
        "Waterfall",
        "Donut",
        "Fuel",
        "Gantt",
        "Meter",
        "Odometer",
        "Radialscatter",
        "Thermometer",
    )})),)
    list_filter = (
        "title",
        "Bar",
        "Bipolar",
        "Funnel",
        "Gauge",
        "HorizontalBar",
        "HorizontalProgressbars",
        "Line",
        "Pie",
        "Radar",
        "Rose",
        "Scatter",
        "SemicircularProgressbars",
        "VerticalProgressbars",
        "Waterfall",
        "Donut",
        "Fuel",
        "Funnel",
        "Gantt",
        "Meter",
        "Odometer",
        "Radialscatter",
        "Thermometer",
    )
    list_display = ('title',)