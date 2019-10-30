from mighty.apps.grapher.backends    import GraphBackend


class RGraph(GraphBackend):

    @property
    def css(self):
        return {
            'canvas': 'rgraph/canvas/canvas.css',
            'svg': 'rgraph/svg/svg.css',
        }

    @property
    def html(self):
        return {
            'canvas': 'rgraph/canvas/canvas.html',
            'svg': 'rgraph/svg/svg.html',
        }

    @property
    def directory(self):
        return {
            'canvas': 'rgraph/canvas/',
            'svg': 'rgraph/svg/',
        }

    @property
    def common_lib(self):
        return {
            'canvas': 'RGraph/libraries/RGraph.common.core.js',
            'svg': 'RGraph/libraries/RGraph.svg.common.core.js',
        }

    @property
    def ajax_bib(self):
        return {
            'canvas': 'RGraph/libraries/RGraph.common.ajax.js',
            'svg': 'RGraph/libraries/RGraph.svg.common.ajax.js',
        }

    @property
    def svg_lib(self):
        return {
            self.bar: 'RGraph/libraries/RGraph.svg.bar.js',
            self.bipolar: 'RGraph/libraries/RGraph.svg.bipolar.js',
            self.funnel: 'RGraph/libraries/RGraph.svg.funnel.js',
            self.gauge: 'RGraph/libraries/RGraph.svg.gauge.js',
            self.horizontalbar: 'RGraph/libraries/RGraph.svg.horizontalbar.js',
            self.horizontalprogressbars: 'RGraph/libraries/RGraph.svg.horizontalprogressbars.js',
            self.line: 'RGraph/libraries/RGraph.svg.line.js',
            self.pie: 'RGraph/libraries/RGraph.svg.pie.js',
            self.radar: 'RGraph/libraries/RGraph.svg.radar.js',
            self.rose: 'RGraph/libraries/RGraph.svg.rose.js',
            self.scatter: 'RGraph/libraries/RGraph.svg.scatter.js',
            self.semicircularprogressbars: 'RGraph/libraries/RGraph.svg.semicircularprogressbars.js',
            self.verticalprogressbars: 'RGraph/libraries/RGraph.svg.verticalprogressbars.js',
            self.waterfall: 'RGraph/libraries/RGraph.svg.waterfall.js',
            self.donut: 'RGraph/libraries/RGraph.svg.donut.js',
            self.gantt: 'RGraph/libraries/RGraph.svg.gantt.js',
            self.meter: 'RGraph/libraries/RGraph.svg.meter.js',
            self.odometer: 'RGraph/libraries/RGraph.svg.odometer.js',
            self.radialscatter: 'RGraph/libraries/RGraph.svg.radialscatter.js',
            self.thermometer: 'RGraph/libraries/RGraph.svg.thermometer.js',
        }

    @property
    def canvas_lib(self):
        return {
            self.bar: 'RGraph/libraries/RGraph.bar.js',
            self.bipolar: 'RGraph/libraries/RGraph.bipolar.js',
            self.funnel: 'RGraph/libraries/RGraph.funnel.js',
            self.gauge: 'RGraph/libraries/RGraph.gauge.js',
            self.horizontalbar: 'RGraph/libraries/RGraph.horizontalbar.js',
            self.horizontalprogressbars: 'RGraph/libraries/RGraph.horizontalprogressbars.js',
            self.line: 'RGraph/libraries/RGraph.line.js',
            self.pie: 'RGraph/libraries/RGraph.pie.js',
            self.radar: 'RGraph/libraries/RGraph.radar.js',
            self.rose: 'RGraph/libraries/RGraph.rose.js',
            self.scatter: 'RGraph/libraries/RGraph.scatter.js',
            self.semicircularprogressbars: 'RGraph/libraries/RGraph.semicircularprogressba.js',
            self.verticalprogressbars: 'RGraph/libraries/RGraph.verticalprogressbars.js',
            self.waterfall: 'RGraph/libraries/RGraph.waterfall.js',
            self.donut: 'RGraph/libraries/RGraph.donut.js',
            self.gantt: 'RGraph/libraries/RGraph.gantt.js',
            self.meter: 'RGraph/libraries/RGraph.meter.js',
            self.odometer: 'RGraph/libraries/RGraph.odometer.js',
            self.radialscatter: 'RGraph/libraries/RGraph.radialscatter.js',
            self.thermometer: 'RGraph/libraries/RGraph.thermometer.js',
        }