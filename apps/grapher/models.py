from django.db import models
from django.utils.html import mark_safe
from django.template import Context, Template

from mighty.models.abstracts import ModelFull
from mighty.models import JSONField
from mighty.apps.grapher import _

BAR = "BAR"
BIPOLAR = "BIPOLAR"
FUNNEL = "FUNNEL"
GAUGE = "GAUGE"
HORIZONTALBAR = "HORIZONTALBAR"
HORIZONTALPROGRESSBARS = "HORIZONTALPROGRESSBARS"
LINE = "LINE"
PIE = "PIE"
RADAR = "RADAR"
ROSE = "ROSE"
SCATTER = "SCATTER"
SEMICIRCULARPROGRESSBARS = "SEMICIRCULARPROGRESSBARS"
VERTICALPROGRESSBARS = "VERTICALPROGRESSBARS"
WATERFALL = "WATERFALL"
DONUT = "DONUT"
GANTT = "GANTT"
METER = "METER"
ODOMETER = "ODOMETER"
RADIALSCATTER = "RADIALSCATTER"
THERMOMETER = "THERMOMETER"
choices = (
    (BAR, _.c_bar),
    (BIPOLAR, _.c_bipolar),
    (FUNNEL, _.c_funnel),
    (GAUGE, _.c_gauge),
    (HORIZONTALBAR, _.c_horizontalbar),
    (HORIZONTALPROGRESSBARS, _.c_horizontalprogressbars),
    (LINE, _.c_line),
    (PIE, _.c_pie),
    (RADAR, _.c_radar),
    (ROSE, _.c_rose),
    (SCATTER, _.c_scatter),
    (SEMICIRCULARPROGRESSBARS, _.c_semicircularprogressbars),
    (VERTICALPROGRESSBARS, _.c_verticalprogressbars),
    (WATERFALL, _.c_waterfall),
    (DONUT, _.c_donut),
    (GANTT, _.c_gantt),
    (METER, _.c_meter),
    (ODOMETER, _.c_odometer),
    (RADIALSCATTER, _.c_radialscatter),
    (THERMOMETER, _.c_thermometer),
)

class Template(ModelFull):
    name = models.CharField(_.f_name, max_length=255, unique=True)
    graphtype = models.CharField(_.f_graphtype, choices=choices, max_length=100, default=BAR)

    lg_width = models.PositiveSmallIntegerField(_.f_lg_width, default=800)
    lg_height = models.PositiveSmallIntegerField(_.f_lg_height, default=400)
    lg_max_width = models.PositiveSmallIntegerField(_.f_lg_max_width, default=1200)
    lg_title_size = models.PositiveSmallIntegerField(_.f_lg_title_size, default=18)
    lg_text_size = models.PositiveSmallIntegerField(_.f_lg_text_size, default=14)
    lg_margin_inner = models.PositiveSmallIntegerField(_.f_lg_margin_inner, default=25)

    md_width = models.PositiveSmallIntegerField(_.f_md_width, default=600)
    md_height = models.PositiveSmallIntegerField(_.f_md_height, default=300)
    md_max_width = models.PositiveSmallIntegerField(_.f_md_max_width, default=992)
    md_title_size = models.PositiveSmallIntegerField(_.f_md_title_size, default=14)
    md_text_size = models.PositiveSmallIntegerField(_.f_md_text_size, default=12)
    md_margin_inner = models.PositiveSmallIntegerField(_.f_md_margin_inner, default=20)

    sm_width = models.PositiveSmallIntegerField(_.f_sm_width, default=400)
    sm_height = models.PositiveSmallIntegerField(_.f_sm_height, default=200)
    sm_max_width = models.PositiveSmallIntegerField(_.f_sm_max_width, default=768)
    sm_title_size = models.PositiveSmallIntegerField(_.f_sm_title_size, default=12)
    sm_text_size = models.PositiveSmallIntegerField(_.f_sm_text_size, default=10)
    sm_margin_inner = models.PositiveSmallIntegerField(_.f_sm_margin_inner, default=10)

    options = JSONField(blank=True, null=True)
    responsive_options = JSONField(blank=True, null=True)

    class Meta(ModelFull.Meta):
        abstract = True
        verbose_name = _.v_template
        verbose_name_plural = _.vp_template

    def __str__(self):
        return self.name

class Graph(ModelFull):
    title = models.CharField(_.f_title, max_length=255)
    is_responsive = models.BooleanField(_.f_is_responsive, default=False)

    svg_container = models.TextField(_.f_svg_container, blank=True, null=True)
    canvas_container = models.TextField(_.f_canvas_container, blank=True, null=True)

    width = models.PositiveSmallIntegerField(_.f_width, default=800)
    height = models.PositiveSmallIntegerField(_.f_height, default=400)
    max_width = models.PositiveSmallIntegerField(_.f_max_width, default=1200)
    title_size = models.PositiveSmallIntegerField(_.f_title_size, default=18)
    text_size = models.PositiveSmallIntegerField(_.f_text_size, default=14)
    margin_inner = models.PositiveSmallIntegerField(_.f_margin_inner, default=25)

    options = JSONField(blank=True, null=True)
    responsive_options = JSONField(blank=True, null=True)

    bar_values = JSONField(blank=True, null=True)
    bipolar_values = JSONField(blank=True, null=True)
    funnel_values = JSONField(blank=True, null=True)
    gauge_values = JSONField(blank=True, null=True)
    horizontalbar_values = JSONField(blank=True, null=True)
    horizontalprogressbars_values = JSONField(blank=True, null=True)
    line_values = JSONField(blank=True, null=True)
    pie_values = JSONField(blank=True, null=True)
    radar_values = JSONField(blank=True, null=True)
    rose_values = JSONField(blank=True, null=True)
    scatter_values = JSONField(blank=True, null=True)
    semicircularprogressbars_values = JSONField(blank=True, null=True)
    verticalprogressbars_values = JSONField(blank=True, null=True)
    waterfall_values = JSONField(blank=True, null=True)
    donut_values = JSONField(blank=True, null=True)
    gantt_values = JSONField(blank=True, null=True)
    meter_values = JSONField(blank=True, null=True)
    odometer_values = JSONField(blank=True, null=True)
    radialscatter_values = JSONField(blank=True, null=True)
    thermometer_values = JSONField(blank=True, null=True)

    class Meta(ModelFull.Meta):
        abstract = True
        verbose_name = _.v_graph
        verbose_name_plural = _.vp_graph

    @property
    def get_svg_container(self):
        return Template(self.svg_container).render(Context({'object': self,}))

    @property
    def get_svg_container(self):
        return Template(self.canvas_container).render(Context({'object': self,}))

    @property
    def svg_url(self):
        return self.get_url('svg', kwargs={'uid': str(self.uid)})

    @property
    def svg_url_html(self):
        return self.get_url_html('svg', self.title)

    @property
    def canvas_url(self):
        return self.get_url('canvas', kwargs={'uid': str(self.uid)})

    @property
    def canvas_url_html(self):
        return self.get_url_html('canvas', self.title)