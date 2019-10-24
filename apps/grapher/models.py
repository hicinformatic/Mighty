from django.db import models

from mighty.models.abstracts import ModelFull
from mighty.models import JSONField

from mighty.apps.grapher import _

can_graph = {
    "Bar": ["svg", "canvas"],
    "Bipolar ": ["svg", "canvas"],
    "Funnel ": ["svg", "canvas"],
    "Gauge ": ["svg", "canvas"],
    "Horizontal Bar ": ["svg", "canvas"],
    "Horizontal Progress bars": ["svg", "canvas"],
    "Line ": ["svg", "canvas"],
    "Pie ": ["svg", "canvas"],
    "Radar ": ["svg", "canvas"],
    "Rose ": ["svg", "canvas"],
    "Scatter ": ["svg", "canvas"],
    "Semi-circular Progress bars": ["svg", "canvas"],
    "Vertical Progress bars": ["svg", "canvas"],
    "Waterfall": ["svg", "canvas"],
    "Donut": ["canvas"],
    "Fuel": ["canvas"],
    "Funnel": ["canvas"],
    "Gantt": ["canvas"],
    "Meter": ["canvas"],
    "Odometer": ["canvas"],
    "Radial scatter": ["canvas"],
    "Thermometer": ["canvas"],
}

class Graph(ModelFull):
    title = models.CharField("Title", max_length=255)
    Bar = models.BooleanField(_.f_Bar, default=False)
    Bipolar = models.BooleanField(_.f_Bipolar, default=False)
    Funnel = models.BooleanField(_.f_Funnel, default=False)
    Gauge = models.BooleanField(_.f_Gauge, default=False)
    HorizontalBar = models.BooleanField(_.f_HorizontalBar, default=False)
    HorizontalProgressbars = models.BooleanField(_.f_HorizontalProgressbars, default=False)
    Line = models.BooleanField(_.f_Line, default=False)
    Pie = models.BooleanField(_.f_Pie, default=False)
    Radar = models.BooleanField(_.f_Radar, default=False)
    Rose = models.BooleanField(_.f_Rose, default=False)
    Scatter = models.BooleanField(_.f_Scatter, default=False)
    SemicircularProgressbars = models.BooleanField(_.f_SemicircularProgressbars, default=False)
    VerticalProgressbars = models.BooleanField(_.f_VerticalProgressbars, default=False)
    Waterfall = models.BooleanField(_.f_Waterfall, default=False)
    Donut = models.BooleanField(_.f_Donut, default=False)
    Fuel = models.BooleanField(_.f_Fuel, default=False)
    Gantt = models.BooleanField(_.f_Gantt, default=False)
    Meter = models.BooleanField(_.f_Meter, default=False)
    Odometer = models.BooleanField(_.f_Odometer, default=False)
    Radialscatter = models.BooleanField(_.f_Radialscatter, default=False)
    Thermometer = models.BooleanField(_.f_Thermometer, default=False)

    class Meta(ModelFull.Meta):
        abstract = True

