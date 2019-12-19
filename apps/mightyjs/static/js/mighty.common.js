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

    this.delay = function(config, ms, action) {
        if (action == "bottom") {
            if (!this.is("blocked", true)) {
                this.xhr(config, action);
            }
        } else {
            delete this.questions.is["blocked"];
            clearTimeout(this.timer[config]);
            var self = this;
            this.timer[config] = setTimeout(function() { self.xhr(config, action); }, ms || 0);
        }
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

    this.xhr = function(config, action) {
        this.protect(config);
        var self = this;
        var url = this.config[config].hasOwnProperty("url") ? this.config[config]["url"] : this.url;
        if (action == "next" && this.config[config]["response"]["next"]) { url = this.config[config]["response"]["next"]; }
        var datas = this.config[config].hasOwnProperty("datas") ? this.serialize(this.config[config]["datas"]) : this.serialize(this.form);
        var method = this.config[config].hasOwnProperty("method") ? this.config[config]["method"] : this.method;
        var datatype = this.config[config].hasOwnProperty("datatype") ? this.config[config]["datatype"] : this.datatype;
        var xhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
        if (method=="GET") {
            if (datas) {
                self.log("log", "datas", datas);
                url = url + "?" + datas;
            }
        }
        if(this.last(config, "url", url) || this.last(config, "datas", datas)){
            this.last(config, {key: "url", value: url});
            this.last(config, {key: "datas", value: datas});
            xhttp.open(method, url, true);
            xhttp.timeout = this.config[config].hasOwnProperty("method") ? this.config[config]["timeout"] : this.timeout;
            xhttp.onprogress = function () {
                self.log("log", "onprogress - url: "+url+", method: "+method+", config: "+config);
            };
            xhttp.onload = function (e) {
                self.log("log", "onload - url: "+url+", datatype: "+datatype, xhttp.response);
                self.config[config]["response"] = JSON.parse(xhttp.response);
                if (datatype == "json") self.template(config, self.config[config]["response"], action);
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
            xhttp.send(datas);
        }
    }

    this.protect = function(config, status){
        status = status === undefined ? true : status;
        if (status) {
        }else{
        }
    }

    this.processconfig = function(config, ms, action) {
        action = action === undefined ? false : action;
        ms = ms === undefined ? 500 : ms;
        this.delay(config, ms, action);

    }

    this.process = function(ms, action) {
        action = action === undefined ? false : action;
        ms = ms === undefined ? 500 : ms;
        for (config in this.config) {
            this.processconfig(config, ms, action);
            if (this.is("bottom")){ this.bottom(config); }
        }
    }

    this.events = function() {
        this.searchable(this.is("searchable"));
    }

    this.searchable = function(searchable) {
        self = this;
        if (searchable) {
           this.addEvent('keyup', document.getElementById(searchable), function(e) {
                document.getElementById(config + "-top").scrollIntoView();
                self.form.search = this.value;
                self.process(500);
            });
            this.form.search = document.getElementById(searchable).value;
        }
    }

    this.template = function(config, response, action) {
        action = action === undefined ? false : action;
        var source = document.getElementById("template-"+config).innerHTML;
        source = source.replace(/\[\[/g, '{{');
        source = source.replace(/\]\]/g, '}}');
        var template = Handlebars.compile(source);
        if (response.hasOwnProperty(this.ajax.results)) {
            var results = response[this.ajax.results];
            delete response[this.ajax.results];
            console.log(results);
            var html = template({"datas": results, "options": response});
        } else {
            var html = template({"datas": response});
        }
        if (this.is('init', true)) {
            if (action == "bottom") {
                document.getElementById(config).innerHTML = document.getElementById(config).innerHTML + html;
            } else {
                document.getElementById(config).innerHTML = html;
            }
        } else {
            document.getElementById(config).innerHTML = html;
            
        }
        if (this.is("next")){ this.next(config); }
        if (this.is("previous")){ this.previous(config); }
        this.protect(config, false);
        this.after(config, response);
        delete this.questions.is["blocked"];
    }

    this.after = function (config, response) { }

    //this.bottom = function(config) {
    //    var self = this;
    //    this.addEvent("scroll", window, function(){
    //        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
    //            self.processconfig(config, 0, "bottom");
    //        }
    //    });
    //}

    this.previous = function(config) {
        var self = this;
        this.addEvent("click", document.getElementById(config + this.actions.previous), function(e) {
            self.processconfig(config, 0, "previous");
            document.getElementById(config + self.actions.top).scrollIntoView();
        });
    }

    this.next = function(config) {
        var self = this;
        this.addEvent("click", document.getElementById(config + this.actions.next), function(e) {
            self.processconfig(config, 0, "next");
            document.getElementById(config + self.actions.top).scrollIntoView();
        });
    }

}