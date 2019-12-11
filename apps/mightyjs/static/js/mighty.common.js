function Mcommon(url, options) {
    //Mconfig.call(this, id, url, options);
    Mconfig.call(this, url, options);

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

    this.log = function(lvl, msg, array) {
        array = array === undefined ? null : array;
        if (!this.hasOwnProperty("logbg")) { this.logbg = this.randdarkcolor(); }
        if (this.debug) { 
            console.log("%c "+Date.now().toString()+": "+lvl+" | "+msg, "background: "+this.logbg+"; color: "+this.colors[lvl]); 
            if (array) { console[lvl](array); }
        }
    }

    this.delay = function(config, ms) {
        clearTimeout(this.timer[config]);
        var self = this;
        this.timer[config] = setTimeout(function() { self.xhr(config); }, ms || 0);
    }

    this.last = function(config, what, like) {
        if (like === undefined) {
            this.questions.lasts[config][what.key] = what.value;
        } else {
            return (this.questions.lasts[config].hasOwnProperty(what) && this.questions.lasts[config][what] === like) ? false : true;
        }
    }

    this.i = function(what, i) {
        i = i === undefined ? 0 : i;
        if (this.questions.i.hasOwnProperty(what)) {
            i = this.questions.i[what];
        } else {
            this.questions.i[what] = 0;
        }
        this.questions.i[what]++;
        return i;
    }

    this.is = function(what, status, is) {
        status = status === undefined ? false : status;
        is = is === undefined ? false : is;
        if (this.questions.is.hasOwnProperty(what) && this.questions.is[what]) {
            is = this.questions.is[what];
        } else {
            this.questions.is[what] = status;
        }
        return is;
    }

    this.add = function(config, key, value) {
        value = value === undefined ? {} : value;
        this.log("debug", "add - config: "+config+", key: "+key, config);
        if(!this.config.hasOwnProperty(config)) {
            this.questions.lasts[config] = {};
            //this.elements[config] = {};
            this.config[config] = {};
        } 
        this.config[config][key] = value;
    }

    this.serialize = function(datas) {
        var str = [];
        for (var p in datas)
          if (datas.hasOwnProperty(p) && datas[p]) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(datas[p]));
          }
        return str.join("&");
    }

    this.addEvent = function(evnt, elem, func) {
        if (elem.addEventListener)  // W3C DOM
           elem.addEventListener(evnt,func,false);
        else if (elem.attachEvent) { // IE DOM
           elem.attachEvent("on"+evnt, func);
        }
        else { // No much to do
           elem["on"+evnt] = func;
        }
     }

    this.xhr = function(config) {
        this.protect(config);
        var self = this;
        var url = this.config[config].hasOwnProperty("url") ? this.config[config]["url"] : this.url;
        var datas = this.config[config].hasOwnProperty("datas") ? this.serialize(this.config[config]["datas"]) : this.serialize(this.form);
        var method = this.config[config].hasOwnProperty("method") ? this.config[config]["method"] : this.method;
        var xhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
        xhttp.onloadstart = function(ev) {
            xhttp.timeout = this.config[config].hasOwnProperty("method") ? this.config[config]["timeout"] : this.timeout;
            xhttp.responseType = this.config[config].hasOwnProperty("datatype") ? this.config[config]["datatype"] : this.datatype;
        };
        xhttp.onprogress = function () {
            self.log("log", "onprogress - url: "+url+", method: "+method+", config: "+config);
        };
        xhttp.onload = function (e) {
            self.log("log", "onload - url: "+url+", method: "+method+", config: "+config, xhttp.response);
            self.template(config, xhttp.response);
            if (datas) {
                window.history.replaceState("", "", "?" + datas);
            }else{
                window.history.replaceState("", "", self.burl);
            }
        };
        xhttp.onabort = function (e) {
            self.log("error", "onabort - url: "+url+", method: "+method+", config: "+config, e);
            self.protect(config, false);
        };
        xhttp.onerror = function (e) {
            self.log("error", "onerror - url: "+url+", method: "+method+", config: "+config, e);
            self.protect(config, false);
        };
        if (method=="GET" && datas) {
            url = url + "?" + datas;
        }
        xhttp.open(method, url, true);
        xhttp.send(datas);
    }

    this.protect = function(config, status){
        status = status === undefined ? true : status;
        if (status) {
        }else{
        }
    }

    this.process = function(ms) {
        ms = ms === undefined ? 500 : ms;
        for (config in this.config) {
            this.delay(config, ms);
            //this.xhr(config);
        }
    }

    this.events = function() {
        this.searchable(this.is("searchable"));
    }

    this.searchable = function(searchable) {
        self = this;
        if (searchable) {
           this.addEvent('keyup', document.getElementById(searchable), function(e) {
                self.form.search = this.value;
                self.process(500);
            });
            this.form.search = document.getElementById(searchable).value;
        }
    }

    this.template = function(config, response) {
        var source = document.getElementById("template-"+config).innerHTML;
        source = source.replace(/\[\[/g, '{{');
        source = source.replace(/\]\]/g, '}}');
        var template = Handlebars.compile(source);
        var html = template({"datas": response[this.ajax.results]});
        document.getElementById(config).innerHTML = html;
        this.protect(config, false);

    }

}