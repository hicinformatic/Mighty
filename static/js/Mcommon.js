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

    this.delay = function(config) {
        clearTimeout(this.timer[config]);
        var self = this;
        this.timer[config] = setTimeout(function() { self.call(config); }, this.msdelay || 0);
    }

    this.last = function(config, what, like=null) {
        if (like === null) {
            this.questions.lasts[config][what.key] = what.value;
        } else {
            return (this.questions.lasts[config].hasOwnProperty(what) && this.questions.lasts[config][what] === like) ? false : true;
        }
    }

    this.getname = function(search, id) {
        return id.replace(search, "");
    }

    this.i = function(what) {
        var i = 0;
        if (this.questions.i.hasOwnProperty(what)) {
            i = this.questions.i[what];
        } else {
            this.questions.i[what] = 0;
        }
        this.questions.i[what]++;
        return i;
    }

    this.is = function(what, status=false) {
        var is = false;
        if (this.questions.is.hasOwnProperty(what) && this.questions.is[what]) {
            is = this.questions.is[what];
        } else {
            this.questions.is[what] = status;
        }
        return is;
    }

    this.exist = function(id, selector="#") {
        var elem = $(`${selector}${id}`);
        this.log("debug", `exist: ${selector}${id} - exist: ${elem.length}`);
        return elem.length === 0 ? false : true;
    }

    this.gettristate = function(inputid){
        return this.lists.tristates[inputid];
    }

    this.checkboxstate = function(input) {
        if (input.is(':checked')) {
            return 1;
        } if (input.is(':indeterminate')) {
            return 2;
        }
        return 0;
    }

    this.tag = function (input) {
        var state = this.checkboxstate(input);
        var value = input.attr("value");
        var tags = $(`#${this.mclsid("tags", {everywhere: true, instance: true})}`);
        var button = $(`button[value="${value}"].${this.mclsid("tag", {everywhere: true, instance: true})}`);
        if (button.length > 0) { button.remove(); }
        if (state !== 0) {
            var button = $("<button></button>");
            button.attr({
                value: value,
                class: this.mclsid("tag", {everywhere: true, instance: true}),
            });
            if (state == 1) {
                button.append(`&equiv;${input.attr("title")}`);
            }else {
                button.append(`&ne;${input.attr("title")}`);
            }
            tags.append(button);
            var self = this;
            button.click(function(){
                self.forcecheckbox(this.value, 1);
                var input = $(`input[value="${this.value}"].${self.mclsid("filterscbx", {everywhere: true, instance: true})}`);
                input.click();
            })
        }
    }

    this.forcecheckbox = function(value, tristate=0) {
        var input = $(`input[value="${value}"].${this.mclsid("filterscbx", {everywhere: true, instance: true})}`);
        if (tristate == 1) {
            input.prop('indeterminate', true);
            input.prop('checked', false);
        } else if (tristate == 2) {
            input.prop('indeterminate', false);
            input.prop('checked', false);
        } else{
            input.prop('indeterminate', false);
            input.prop('checked', true);
        }
        this.lists.tristates[value] = this.checkboxstate(input);
        if (this.is("tags")) { this.tag(input); }
        return this.lists.tristates[value];
    }

    this.mclsid = function(fonction, options={}) {
        var cls = this.bid;
        if (options.hasOwnProperty("everywhere")) { var cls = `${this.bid}-${fonction}` }
        else { var cls = fonction; }
        if (options.hasOwnProperty("instance")) { cls += `-${this.id}`; }
        if (options.hasOwnProperty("config")) { cls += `-${options.config}` }
        if (options.hasOwnProperty("after")) { cls += `-${options.after}`; }
        return cls;
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

    this.template = function(options={}) {
        var tag = options.hasOwnProperty("tag") ? options.tag : "div";
        var el = tag === "input" ? $("<input>") : $(`<${tag}></${tag}>`);
        var tag = options.hasOwnProperty("tag") ? options.tag : "div";
        delete options.tag;
        el.attr(options);
        return el;
    }

    this.datas = function(config) {
        this.step(config, "prepare");
        var self = this, datas = {};
        this.elements.form.serializeArray().forEach(function(d) {
            var key = d.name;
            var value = d.value;
            if (value) {
                value = self.forces[key] !== null ? [value, self.forces[key]].join(" ") : value;
                datas[key] = value;
            } else if (self.forces[key] !== null) {
                datas[key] = self.forces[key];
            }
            self.options[key] = value;
        });
        this.elements[config].form.serializeArray().forEach(function(d) {
            var key = d.name;
            var value = d.value;
            if (value && key !== "config") { datas[key] = value; }
            self.config[config][key] = value;
        });
        return datas;
    }

    this.call = function(config) {
        var self = this;
        var url = this.config[config].hasOwnProperty("url") ? this.config[config]["url"] : this.url;
        var datas = this.config[config].hasOwnProperty("datas") ? this.config[config]["datas"] : $.param(this.datas(config));
        var method = this.config[config].hasOwnProperty("method") ? this.config[config]["method"] : this.method;
        var datatype = this.config[config].hasOwnProperty("datatype") ? this.config[config]["datatype"] : this.datatype;
        var timeout = this.config[config].hasOwnProperty("method") ? this.config[config]["timeout"] : this.timeout;
        if(this.last(config, "url", url) || this.last(config, "datas", datas)){
            this.last(config, {key: "url", value: url});
            this.last(config, {key: "datas", value: datas});
            $.ajax({ 
                url: url,
                method: method,
                data: datas,
                dataType: datatype,
                timeout: timeout,
                beforeSend: function() { self.before({id: self.id, url: url, datas: datas, method: method, config: config}); },
                error: function (xhr, status, error) { self.error(xhr, status, error, {id: self.id, url: url, datas: datas, method: method, config: config}) },
                complete: function() { self.after({id: self.id, url: url, datas: datas, method: method, config: config}); },
                success: function(response) { self.success(response, {id: self.id, url: url, datas: datas, method: method, config: config}); },
            });
        } else {
            this.nochange({url: url, datas: datas, method: method, config: config});
        }
    }

    this.nochange = function(options) { this.step(options.config, "complete");  }
    this.before = function (options) { this.step(options.config, "send"); }
    this.success = function (response, options) { 
        this.step(options.config, "success"); 
        if (this.is("paginate")) { this.paginate(options.config, response[this.ajax.count]); }
        if (this.is("counter")) { this.counter(options.config, response[this.ajax.count]); }
        this.when(response, options);
    }
    this.after = function (options) { 
        this.step(options.config, "complete"); 
        if (this.is("oneshow")) { this.oneshow(); }
    }
    
    this.code100 = function() { var msg = "Continue, informational"; this.log("debug", msg); return msg; }
    this.code101 = function() { var msg = "Switching Protocols, informational"; this.log("debug", msg); return msg; }
    this.code200 = function() { var msg = "OK, Successful"; this.log("debug", msg); return msg; }
    this.code201 = function() { var msg = "Created, Successful"; this.log("debug", msg); return msg; }
    this.code202 = function() { var msg = "Accepted, Successful"; this.log("debug", msg); return msg; }
    this.code203 = function() { var msg = "Non-Authoritative information, Successful"; this.log("debug", msg); return msg; }
    this.code204 = function() { var msg = "No Content, Successful"; this.log("debug", msg); return msg; }
    this.code205 = function() { var msg = "Reset Content, Successful"; this.log("debug", msg); return msg; }
    this.code206 = function() { var msg = "Partial Content, Successful"; this.log("debug", msg); return msg; }
    this.code300 = function() { var msg = "Multiple Choices, Redirection"; this.log("debug", msg); return msg; }
    this.code301 = function() { var msg = "Moved Permanently, Redirection"; this.log("debug", msg); return msg; }
    this.code302 = function() { var msg = "Found, Redirection"; this.log("debug", msg); return msg; }
    this.code303 = function() { var msg = "See Other, Redirection"; this.log("debug", msg); return msg; }
    this.code304 = function() { var msg = "Not Modified, Redirection"; this.log("debug", msg); return msg; }
    this.code305 = function() { var msg = "Use Proxy, Redirection"; this.log("debug", msg); return msg; }
    this.code307 = function() { var msg = "Temporary Redirect, Redirection"; this.log("debug", msg); return msg; }
    this.code400 = function() { var msg = "Bad Request, Client Error"; this.log("warning", msg); return msg; }
    this.code401 = function() { var msg = "Unauthorized, Client Error"; this.log("warning", msg); return msg; }
    this.code402 = function() { var msg = "Payment Required, Client Error"; this.log("warning", msg); return msg; }
    this.code403 = function() { var msg = "Forbidden, Client Error"; this.log("warning", msg); return msg; }
    this.code404 = function() { var msg = "Not Found, Client Error"; this.log("warning", msg); return msg; }
    this.code405 = function() { var msg = "Method Not Allowed, Client Error"; this.log("warning", msg); return msg; }
    this.code406 = function() { var msg = "Not Acceptable, Client Error"; this.log("warning", msg); return msg; }
    this.code407 = function() { var msg = "Proxy Authentication Required, Client Error"; this.log("warning", msg); return msg; }
    this.code408 = function() { var msg = "Request Timeout, Client Error"; this.log("warning", msg); return msg; }
    this.code409 = function() { var msg = "Conflict, Client Error"; this.log("warning", msg); return msg; }
    this.code410 = function() { var msg = "Gone, Client Error"; this.log("warning", msg); return msg; }
    this.code411 = function() { var msg = "Length Required, Client Error"; this.log("warning", msg); return msg; }
    this.code412 = function() { var msg = "Precondition Failed, Client Error"; this.log("warning", msg); return msg; }
    this.code413 = function() { var msg = "Request Entity Too Large, Client Error"; this.log("warning", msg); return msg; }
    this.code414 = function() { var msg = "Request-URI Too Long, Client Error"; this.log("warning", msg); return msg; }
    this.code415 = function() { var msg = "Unsupported Media Type, Client Error"; this.log("warning", msg); return msg; }
    this.code416 = function() { var msg = "Requested Range Not Satisfiable, Client Error"; this.log("warning", msg); return msg; }
    this.code417 = function() { var msg = "Expectation Failed, Client Error"; this.log("warning", msg); return msg; }
    this.code500 = function() { var msg = "Internal Server Error, Server Error"; this.log("error", msg); return msg; }
    this.code501 = function() { var msg = "Not Implemented, Server Error"; this.log("error", msg); return msg; }
    this.code502 = function() { var msg = "Bad Gateway, Server Error"; this.log("error", msg); return msg; }
    this.code503 = function() { var msg = "Service Unavailable, Server Error"; this.log("error", msg); return msg; }
    this.code504 = function() { var msg = "Gateway Timeout, Server Error"; this.log("error", msg); return msg; }
    this.code505 = function() { var msg = "HTTP Version Not Supported, Server Error"; this.log("error", msg); return msg; }

    this.error= function (xhr, status, error, options) {
        this.step(options.config, "error");
        var container = this.mclsid("error", {everywhere: true, instance: true, config: options.config});
        if (this.exist(container)) {
            container = $(`#${container}`);
            container.html(`${xhr.status} - ${this[`code${xhr.status}`]()}`);
        }
    }

    this.step = function (config, step="ready") {
        if (this.steps[step] < 5) {
            this.elements[config].step.html(` - ${this.steps[step]}/4`);
        } else  {
            this.elements[config].step.html("Error");
        }
    }

    this.form = function() {
        var form = this.template({tag: "form", class: this.mclsid("form", {everywhere: true}), id: this.mclsid("form", {everywhere: true, instance: true})});
        this.elements.mighty.append(form);
        this.elements.form = form;
        var self = this;
        this.canshared.forEach(function(ipt){
            var input = self.template({tag: "input", name: ipt, placeholder: ipt, id: self.mclsid(ipt, {everywhere: true, instance: true})});
            if (self.options.hasOwnProperty(ipt)) { input.val(self.options[ipt]); }
            form.append(input);
            self.elements[ipt] = input;
        });
        form.change(function(){ for (config in self.config) { self.delay(config); } });
        for (config in this.config) {
            form = this.template({
                tag: "form",
                id: this.mclsid("form", {everywhere: true, instance: true, config: config})
            });
            var p = this.template({tag: "p", id: this.mclsid("config", {everywhere: true, instance: true, config: config})});
            p.append(config);
            var step = this.template({tag: "span", id: this.mclsid("step", {everywhere: true, instance: true, config: config})});
            this.elements[config].step = step;
            p.append(step);
            this.elements.mighty.append(p);
            this.step(config, "ready");
            this.elements.mighty.append(form);
            this.elements[config].form = form;
            input = self.template({tag: "input", name: "config", value: config});
            form.append(input);
            this.cantshared.forEach(function(ipt){
                input = self.template({tag: "input", name: ipt, placeholder: ipt, id: self.mclsid(ipt, {everywhere: true, instance: true, config: config})});
                if (self.config[config].hasOwnProperty(ipt)) { input.val(self.config[config][ipt]); }
                form.append(input);
                self.elements[config][ipt] = input;
            });
            form.change(function(){ self.delay($(`#${this.id}`).find('input[name="config"]').val()); });
        }
    }

    this.search = function () {
        var container = this.mclsid("cmd-search", {everywhere: true, instance: true});
        if (this.exist(container)) {
            container = $(`#${container}`);
            var label = this.template({
                tag: "label",
                class: this.mclsid("cmd-search", {everywhere: true}),
            });
            var search = this.template({
                tag: "input",
                class: this.mclsid("cmd-search", {everywhere: true}),
                id: this.mclsid("cmd-search", {everywhere: true, instance: true}),
            });
            label.append(search);
            label.append(`<span>${this.translation.search}</span>`);
            container.append(label);
            this.elements.commands.search = search;
            var self = this;
            search.on("keyup", function(e){
                if( this.value.length >= 2 ) {
                    if (self.is("searchex") && self.checkboxstate(self.elements.commands.searchex)) {
                        self.elements.searchex.val(this.value);
                    } else {
                        self.elements.search.val(this.value);
                    }
                    for (config in self.config) { self.elements[config].page.val(1); }
                    self.elements.form.trigger("change");
                }else{
                    self.elements.searchex.val("");
                    self.elements.search.val("");
                    for (config in self.config) { self.elements[config].page.val(1); }
                    self.elements.form.trigger("change");
                }
            });
        }
    }

    this.searchex = function() {
        var container = this.mclsid("cmd-searchex", {everywhere: true, instance: true});
        if (this.exist(container)) {
            container = $(`#${container}`);
            var label = this.template({
                tag: "label",
                class: this.mclsid("cmd-searchex", {everywhere: true}),
            });
            var searchex = this.template({
                tag: "input",
                class: this.mclsid("cmd-searchex", {everywhere: true}),
                id: this.mclsid("cmd-searchex", {everywhere: true, instance: true}),
                type: "checkbox",
            });
            label.append(searchex);
            label.append(`<span>${this.translation.searchex}</span>`);
            container.append(label);
            this.elements.commands.searchex = searchex;
            var self = this;
            searchex.change(function(){
                if (self.checkboxstate(searchex)) {
                    self.elements.searchex.val(self.elements.search.val());
                    self.elements.search.val("");
                }else{
                    self.elements.search.val(self.elements.searchex.val());
                    self.elements.searchex.val("");
                }
                self.elements.form.trigger("change");
            });
        }
    }

    this.paginate = function(config, count) {
        var nbr = count > 50 ? Math.ceil(count/this.by)+1 : 1;
        var container = this.mclsid("cmd-paginate", {everywhere: true, instance: true});
        var page = this.elements[config].page.val();
        if (this.exist(container)) {
            container = $(`#${container}`);
            var id = this.mclsid("cmd-paginate", {everywhere: true, instance: true, config: config});
            if (this.exist(id)) { $(`#${id}`).remove(); }
            if (nbr > 1) {
                var paginate = this.template({
                    tag: "select",
                    class: `${this.mclsid("cmd-paginate", {everywhere: true})} ${this.mclsid("show", {everywhere: true, instance: true, config: config})}`,
                    id: id,
                });
                for (var i=1; i < nbr; i++) {
                    var option = this.template({tag: "option", value: i});
                    if (i == page) { option.attr("selected", "selected"); }
                    option.append(`${this.translation.paginate} ${i}`);
                    paginate.append(option);
                }
                container.append(paginate);
                var self = this;
                paginate.change(function(){
                    self.elements[config].page.val(this.value);
                    self.delay(config);
                });
            }
        }
    }

    this.counter = function(config, count) {
        var container = this.mclsid("cmd-counter", {everywhere: true, instance: true});
        if (this.exist(container)) {
            container = $(`#${container}`);
            var id = this.mclsid("cmd-counter", {everywhere: true, instance: true, config: config});
            if (this.exist(id)) { $(`#${id}`).remove(); }
            var counter = this.template({
                tag: "label",
                class: `${this.mclsid("cmd-counter", {everywhere: true})} ${this.mclsid("show", {everywhere: true, instance: true, config: config})}`,
                id: id,
            });
            var div = this.template({
                tag: "div",
                class: `${this.mclsid("cmd-counter", {everywhere: true})} ${this.mclsid("show", {everywhere: true, instance: true, config: config})}`,
            });
            counter.append(div);
            counter.append(`<span>${count} ${this.translation.counter}</span>`);
            container.append(counter);
        }
    }

    this.filterscbxchange = function(state, value){
        var posf = this.lists.filters.indexOf(value);
        var pose = this.lists.excludes.indexOf(value);
        if(state == 1) {
            if (posf < 0) { this.lists.filters.push(value); }
            if (pose >= 0) { delete this.lists.excludes[pose]; }
        } else if(state == 2) {
            if (pose < 0) { this.lists.excludes.push(value); }
            if (posf >= 0) { delete this.lists.filters[posf]; }
        } else {
            if (posf >= 0) { delete this.lists.filters[posf]; }
            if (pose >= 0) { delete this.lists.excludes[pose]; }
        }
        var self = this;
        this.elements.filter.val(Object.keys(self.lists.filters).map( function(key){ return self.lists.filters[key] }).join(" "));
        this.elements.exclude.val(Object.keys(self.lists.excludes).map( function(key){ return self.lists.excludes[key] }).join(" "));
        this.elements.form.trigger("change");
    };

    this.filterscbx = function() {
        var self = this;
        $(`.${this.mclsid("filterscbx", {everywhere: true, instance: true})}`).each(function(){
            if (self.lists.filters.indexOf(this.value) >= 0) {
                self.forcecheckbox(this.value, 0);    
            } else if (self.lists.excludes.indexOf(this.value) >= 0) {
                self.forcecheckbox(this.value, 1);
            } else {
                self.forcecheckbox(this.value, 2);
            }
            $(this).change(function(){
                var state = self.gettristate(this.value);
                state = self.forcecheckbox(this.value, state);
                self.filterscbxchange(state, this.value);
            });
        });
        this.elements.filter.val(Object.keys(self.lists.filters).map( function(key){ return self.lists.filters[key] }).join(" "));
        this.elements.exclude.val(Object.keys(self.lists.excludes).map( function(key){ return self.lists.excludes[key] }).join(" "));
    }

    this.oneshow = function(config=null) {
        this.show = config === null ? this.show : config;
        for (config in this.config) { $(`.${this.mclsid("show", {everywhere: true, instance: true, config: config})}`).hide(); }
        $(`.${this.mclsid("show", {everywhere: true, instance: true, config: this.show})}`).show();
    }

    this.start = function() {
        this.form();
        if (this.is("search")) { this.search(); }
        if (this.is("searchex")) { this.searchex(); }
        if (this.is("filterscbx")) { this.filterscbx(); }
        this.initialize();
        this.elements.form.trigger("change");
    }

    this.initialize = function() {
        this.log("debug", "-- initialize --");    
    }

    this.when = function() {
        this.log("debug", "-- when --");    
    }

    this.log("debug", "--- start ---");
    var mighty = this.template({tag: "section", class: this.mclsid("mighty", {everywhere: true}), id: this.mclsid("mighty", {everywhere: true, instance: true})});
    mighty.append(`<h1>Mighty: ${this.id} - <small>${this.url}</small></h1>`);
    $("body").prepend(mighty);
    mighty.hide();
    this.elements.mighty = mighty;
}