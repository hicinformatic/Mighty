function Mcommon(id, url, options={}) {
    Mconfig.call(this, id, url, options);

    this.randdarkcolor = function() {
        var lum = -0.25;
        var hex = String('#' + Math.random().toString(16).slice(2, 8).toUpperCase()).replace(/[^0-9a-f]/gi, '');
        if (hex.length < 6) { hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]; }
        var rgb = "#", c, i;
        for (i = 0; i < 3; i++) {
            c = parseInt(hex.substr(i * 2, 2), 16);
            c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
            rgb += ("00" + c).substr(c.length);
        }
        return rgb;
    }

    this.log = function(lvl, msg, array=null) {
        if (!this.hasOwnProperty("logbg")) { this.logbg = this.randdarkcolor(); }
        if (this.debug) { 
            console.log(`%c ${Date.now().toString()}: ${lvl} | ${msg}`, `background: ${this.logbg}; color: ${this.colors[lvl]}`); 
            if (array) { console[lvl](array); }
        }
    }

    this.add = function(config, key, value={}) {
        this.log("debug", `add - config: ${config}, key: ${key}`, config);
        if(!this.config.hasOwnProperty(config)) {
            this.questions.lasts[config] = {};
            this.elements[config] = {};
            this.config[config] = {};
        } 
        this.config[config][key] = value;
    }

    this.xhr = function(config) {
        var self = this;
        var url = this.config[config].hasOwnProperty("url") ? this.config[config]["url"] : this.url;
        var datas = this.config[config].hasOwnProperty("datas") ? this.config[config]["datas"] : '';
        var method = this.config[config].hasOwnProperty("method") ? this.config[config]["method"] : this.method;
        var xhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
        xhttp.timeout = this.config[config].hasOwnProperty("method") ? this.config[config]["timeout"] : this.timeout;
        xhttp.responseType = this.config[config].hasOwnProperty("datatype") ? this.config[config]["datatype"] : this.datatype;;
        xhttp.onprogress = function () {
            self.log("log", `onprogress - url: ${url}, method: ${method}, config: ${config}`);
        };
        xhttp.onload = function (e) {
            self.log("log", `onprogress - url: ${url}, method: ${method}, config: ${config}`, xhttp.response);
        };
        xhttp.onabort = function (e) {
            self.log("error", `onabort - url: ${url}, method: ${method}, config: ${config}`, e);
        };
        xhttp.onerror = function (e) {
            self.log("error", `onerror - url: ${url}, method: ${method}, config: ${config}`, e);
        };
        xhttp.open(method, url, true);
        xhttp.send(datas);
    }

    this.process = function() {
        for (config in this.config) {
            this.xhr(config);
        }
    }

}