from django.conf import settings
from mighty.views import ModelViewSet, ListView, DetailView
from mighty.models.grapher import Graph
from mighty.apps.grapher import filters

fields = (
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
    )

from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.module_loading import import_string

@method_decorator(xframe_options_exempt, name='dispatch')
class GraphView(DetailView):
    no_permission = True
    fields = fields
    template_name = 'mighty/graph.html'
    backend = None

    def get_header(self):
        return {'title': self.object.title, }

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data(**kwargs)
        backend = import_string(settings.GRAPHER_BACKEND)
        self.backend = backend(self.object)
        context.update({
            'css': self.backend.css,
            'html': self.backend.html,
            'directory': self.backend.directory,
            'templates': self.object.templates.all(),
        })
        return context

class SvgView(GraphView):
    def get_context_data(self, **kwargs):
        context = super(SvgView, self).get_context_data(**kwargs)
        context.update({
            'js': self.backend.libraries('svg'),
        })
        return context

class CanvasView(GraphView):
    def get_context_data(self, **kwargs):
        context = super(CanvasView, self).get_context_data(**kwargs)
        context.update({'js': self.backend.libraries('canvas')})
        return context


#import matplotlib
#import matplotlib.pyplot as plt
#import numpy as np
#
#from matplotlib.figure import Figure
#from django.http import HttpResponse
#import io
#
#@method_decorator(xframe_options_exempt, name='dispatch')
#class ImageGraph(DetailView):
#    no_permission = True
#    fields = fields
#
#    def get_header(self):
#        return {'title': self.object.title, }
#
#    def render_to_response(self, context, **response_kwargs):
#        def autolabel(rects):
#            """Attach a text label above each bar in *rects*, displaying its height."""
#            for rect in rects:
#                height = rect.get_height()
#                ax.annotate('{}'.format(height),
#                            xy=(rect.get_x() + rect.get_width() / 2, height),
#                            xytext=(0, 3),  # 3 points vertical offset
#                            textcoords="offset points",
#                            ha='center', va='bottom')
#
#        labels = self.object.labels
#        data = self.object.data
#        x = np.arange(len(labels))  # the label locations
#        width = 0.35  # the width of the bars
#        fig, ax = plt.subplots()
#        for d in data:
#            rects1 = ax.bar(x - width/2, d, width, label='Men')
#            autolabel(rects1)
#        ax.set_ylabel('Scores')
#        ax.set_title('Scores by group and gender')
#        ax.set_xticks(x)
#        ax.set_xticklabels(labels)
#        ax.legend()
#
#        fig.tight_layout()
#        buf = io.BytesIO()
#        plt.savefig(buf, format='png')
#        plt.close(fig)
#        response = HttpResponse(buf.getvalue(), content_type='image/png')
#        return response

class GraphViewSet(ModelViewSet):
    filter_model = filters.GraphFilter
    model = Graph
    list_display = ('__str__', 'image_html',)
    fields = fields

    def __init__(self, model=None):
        super().__init__()
        self.addView('svg', SvgView, '%s/svg/')
        self.addView('canvas', CanvasView, '%s/canvas/')
        #self.addView('image', ImageGraph, '%s/image/')


if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.views.api import ApiModelViewSet
    from mighty.apps.grapher.serializers import GraphSerializer

    class GraphApiViewSet(ApiModelViewSet):
        filter_model = filters.GraphFilter
        model = Graph
        list_display = ('__str__', 'image_html',)
        fields = fields
        queryset = Graph.objects.all()
        serializer_class = GraphSerializer

