function Mradar(id, url, options={}) {
    Mcommon.call(this, id, url, options);
    this.response = {};
    this.axes = [];
    this.max = {self: 1};
    this.min = {self: 1};
    this.times = {self: 1};
    this.add("init", "color", "transparent");

    this.axe = function(options={}) {
        this.axes.push(options);
    }

    this.start = function() {
        for (config in this.config) { this.call(config); }
    }

    this.step = function (config, step="ready") {  
        var test = "test";
    }

    this.datas = function(config) {
        return config == "init" ? [] : this.config[config].datas;
    }

    //this.initialize = function() {
    //    this.add("init", "nothing", "nothing");
    //    this.call("init");
    //}

    this.labels = function() {
        var labels = [];
        this.axes.forEach(function(axe){ 
            labels.push(axe.label);
        });
        return labels;
    }

    this.tablereal = function(config, axe) {
        if(!this.response[config][`avg_${axe.dataway}`]) { return 0; }
        return this.response[config][`avg_${axe.dataway}`];
    }

    this.tabledefault = function(config, axe) {
        var data = (axe.hasOwnProperty("table")) ? this[`table${axe.table}`](config, axe) : this.typedefault(config, axe);
        if (axe.hasOwnProperty("round")) { data = axe.round > 0 ? data.toFixed(axe.round) : Math.round(data, axe.round); }
        if (axe.hasOwnProperty("milliem")) { data = Math.round(data).toLocaleString('en').replace(new RegExp(',', 'g'), ' '); }
        return data;
    }

    this.table = function (config) {
        var id = this.mclsid("radar", {everywhere: true, instance: true, config: config, after: ["table"]});
        var tbody = $(`#${id}`).children("tbody");
        tbody.html("");
        var self = this;
        this.axes.forEach(function(axe){
            var tr = $("<tr></tr>");
            var tddata = $("<td></td>");
            tddata.append(self.tabledefault(config, axe));
            if (axe.hasOwnProperty("unit")) { tddata.append(axe.unit); } else { tddata.append(" %"); }
            var tddesc = $("<td></td>");
            tddesc.append(axe.desc);
            tr.append(tddata);
            tr.append(tddesc);
            tbody.append(tr);
        });
    }

    this.typedefault = function(config, axe) {
        if(!this.response[config][`avg_${axe.dataway}`]) { return 0; }
        if (axe.hasOwnProperty("type")) { return this[`type${axe.type}`](config, axe); }
        if (axe.hasOwnProperty("times")) { 
            if (axe.times === "self") {
                return this.times[axe.times]*this.response[config][`avg_${axe.dataway}`];
            } else {
                return (100/this.response[config][`avg_${axe.times}`])*this.response[config][`avg_${axe.dataway}`];
            }
        }
        return this.times[axe.dataway]*this.response[config][`avg_${axe.dataway}`];
    }

    this.stats = function (){
        var full = [];
        var self = this;
        for (config in this.config) {
            var stats = [];
            if (config === "init") {
                this.axes.forEach(function(axe){
                    stats.push(100);
                });
            } else {
                this.axes.forEach(function(axe){
                    stats.push(self.typedefault(config, axe));
                });
            }
            full.push(stats);
        }
        return full;
    }

    this.colors = function() {
        var colors = [];
        for (radar in this.config){ colors.push(this.config[radar].color); }
        return colors;
    }

    this.success = function (response, options) {
        this.response[options.config] = response;
        if (options.config === "init") {
            var self = this;
            this.axes.forEach(function(axe){
                if (response.hasOwnProperty(`max_${axe.dataway}`)) {
                    self.max[axe.dataway] = response[`max_${axe.dataway}`];
                    self.times[axe.dataway] = 100/response[`max_${axe.dataway}`];
                }else {
                    self.times[axe.dataway] = 0;
                }
                if (response.hasOwnProperty(`min_${axe.dataway}`)) {
                    self.min[axe.dataway] = response[`min_${axe.dataway}`];
                }
            });
        }
        if (this.is("table")) { this.table(options.config); }
        var self = this;
        setTimeout(function(){
            self.draw();
        }, 500);
    }


    this.draw = function() {
        var self = this;
        var display = "inline-block";
        var id = this.mclsid("radar", {everywhere: true, instance: true});
        if (this.radar != null) { 
            display = $(`#${id}`).css("display");
            RGraph.SVG.clear(this.radar.svg); 
        }
        this.radar = new RGraph.SVG.Radar({
            id: id,
            data: self.stats(),
            options: {
                scaleVisible: false,
                scaleMax: 100,
                filled: true,
                filledAccumulative: false,
                backgroundGridColor: 'gray',
                colors: self.colors(),
                linewidth: 2,
                labels: self.labels(),
                tickmarksStyle: 'filledcircle',
                tickmarksSize: 0
            }
        }).trace();
        $(`#${id}`).css("display", display);
    }


}