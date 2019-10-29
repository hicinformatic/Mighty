from django.db import models

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
SEMICIRCULARPROGRESSBA = "SEMICIRCULARPROGRESSBA"
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
    (SEMICIRCULARPROGRESSBA, _.c_semicircularprogressba),
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


    options = JSONField()
    responsive_options = JSONField()


    class Meta(ModelFull.Meta):
        abstract = True
        verbose_name = _.v_template
        verbose_name_plural = _.vp_template

    def __str__(self):
        return self.name

from django.utils.html import mark_safe
class Graph(ModelFull):
    title = models.CharField(_.f_title, max_length=255)
    is_responsive = models.BooleanField(_.f_is_responsive, default=False)
    values = JSONField()
    container = models.TextField(_.f_container, blank=True, null=True)

    width = models.PositiveSmallIntegerField(_.f_width, default=800)
    height = models.PositiveSmallIntegerField(_.f_height, default=400)
    max_width = models.PositiveSmallIntegerField(_.f_max_width, default=1200)
    title_size = models.PositiveSmallIntegerField(_.f_title_size, default=18)
    text_size = models.PositiveSmallIntegerField(_.f_text_size, default=14)
    margin_inner = models.PositiveSmallIntegerField(_.f_margin_inner, default=25)

    options = JSONField()
    responsive_options = JSONField()

    class Meta(ModelFull.Meta):
        abstract = True
        verbose_name = _.v_graph
        verbose_name_plural = _.vp_graph

    @property
    def labels(self):
        return [key for key, value in self.values.items()]

    @property
    def labels_str(self):
        return mark_safe(str(self.labels))

    @property
    def data(self):
        return [value for key, value in self.values.items()]

    @property
    def data_str(self):
        return mark_safe(str([value for key, value in self.values.items()]))

    @property
    def get_container(self):
        from django.template import Context, Template
        return Template(self.container).render(Context({'object': self,}))
