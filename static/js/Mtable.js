function Mtable(id, url, options={}) {
    Mcommon.call(this, id, url, options);
    this.columns = {};

    this.delay = function(config) {
        this.elements[config].container.addClass('loading');
        clearTimeout(this.timer[config]);
        var self = this;
        this.timer[config] = setTimeout(function() { self.call(config); }, this.msdelay || 0);
    }

    this.column = function(config, options={}) {
        if (!this.columns.hasOwnProperty(config)) { this.columns[config] = []; }
        this.columns[config].push(options);
    }

    this.table = function(config) {
        var container = this.mclsid("mtable", {everywhere: true, instance: true});
        if (this.exist(container)) {
            container = $(`#${container}`);
            this.elements[config].container = container;
            var table = this.template({
                tag: "table",
                class: `${this.mclsid("mtable-table", {everywhere: true})} ${this.mclsid("show", {everywhere: true, instance: true, config: config})}`,
                id: this.mclsid("mtable-table", {everywhere: true, instance: true, config: config}),
                cellspacing: 0, cellpadding: 0,
            });
            container.append(table);
            this.elements[config].table = table;
            var thead = this.template({
                tag: "thead",
                class: this.mclsid("mtable-thead", {everywhere: true}),
                id: this.mclsid("mtable-thead", {everywhere: true, instance: true, config: config}),
            });
            table.append(thead);
            this.elements[config].thead = thead;
            var tbody = this.template({
                tag: "tbody",
                class: this.mclsid("mtable-tbody", {everywhere: true}),
                id: this.mclsid("mtable-tbody", {everywhere: true, instance: true, config: config}),
            });
            table.append(tbody);
            this.elements[config].tbody = tbody;
        }
    }

    this.shortcuts = function(config, column) {
        var col = column.dataway.replace('.', '__');
        var shortcuts = this.template({
            tag: "div",
            class: this.mclsid("mtable-shortcuts", {everywhere: true}),
            id: this.mclsid("mtable-shortcuts", {everywhere: true, instance: true, config: config, after: col}),
        });
        return shortcuts;
    }

    this.order = function(title) {
        var self = this;
        title.click(function(){
            var col = self.getname(self.mclsid("mtable-title", {everywhere: true, instance: true, after: [""]}), this.id);
            col = col.split("-");
            var config = col[0];
            col = col[1];
            var order = self.elements[config].order.val();
            $(`.${self.mclsid("mtable-title", {everywhere: true})}.order`).removeClass("active");
            $(this).addClass("active");
            $(this).children(`.${self.mclsid("mtable-title-icons-order", {everywhere: true})}`).remove();
            var icons = self.template({
                tag: "span",
                class: self.mclsid("mtable-title-icons-order", {everywhere: true}),
            });
            if (col === order) {
                icons.append(`&nbsp;${self.icons.down}`);
                self.elements[config].order.val(`-${col}`);
            } 
            else {
                icons.append(`&nbsp;${self.icons.up}`);
                self.elements[config].order.val(col);
            }
            $(this).append(icons);
            self.elements[config].form.trigger("change");
        });
    }

    this.th = function(config, column) {
        var col = column.dataway.replace('.', '__');
        var th = this.template({
            tag: "th",
            class: `${this.mclsid("mtable-th", {everywhere: true})} ${this.mclsid("mtable-col", {everywhere: true, instance: true, config: config, after: col})}`,
        });
        var title = this.template({
            tag: "div",
            class: this.mclsid("mtable-title", {everywhere: true}),
            id: this.mclsid("mtable-title", {everywhere: true, instance: true, config: config, after: col}),
        });
        title.append(`<span>${column.title}</span>`);
        if (column.hasOwnProperty("order") && this.is("order")) {
            title.addClass("order");
            var order = this.elements[config].order.val();
            var icons = this.template({
                tag: "span",
                class: this.mclsid("mtable-title-icons-order", {everywhere: true}),
            });
            order = order[0] === "-" ? order.replace("-", "") : order;
            var icon = order[0] === "-" ? `&nbsp;${this.icons.down}` : `&nbsp;${this.icons.up}`;
            if (col === order) {
                icons.append(icon);
                title.addClass("active")
            } else {
                icons.append(`&nbsp;${this.icons.up}`);
            }
            title.append(icons);
            this.order(title);
            
        }
        th.append(this.shortcuts(config, column));
        th.append(title);
        return th;
    }

    this.header = function(config) {
        var tr = this.template({
            tag: "tr",
            class: this.mclsid("mtable-trhead", {everywhere: true}),
            id: this.mclsid("mtable-trhead", {everywhere: true, instance: true, config: config}),
        });
        this.elements[config].trhead= tr;
        this.elements[config].thead.append(tr);
        this.elements[config].th = {};
        var self = this;
        this.columns[config].forEach(function(column){
            var th = self.th(config, column)
            tr.append(th);
            self.elements[config].th[column.title] = th;
        });
    }

    this.td = function(config, column) {
        var col = column.dataway.replace(".", "__");
        var td = this.template({
            tag: "td",
            class: `${this.mclsid("mtable-td", {everywhere: true})} ${this.mclsid("mtable-col", {everywhere: true, instance: true, config: config, after: col})}`,
        });
        var data = this.template({
            tag: "div",
            class: `${this.mclsid("mtable-data", {everywhere: true})} ${this.mclsid("mtable-data", {everywhere: true, instance: true, config: config, after: col})}`,
        });
        if (column.hasOwnProperty("template")) {
            data.append(column.template.replace(/\[\[/g, '{{').replace(/\]\]/g, '}}'));
        }else{
            data.append(`{{ ${column.dataway} }}`);
        }
        td.append(data);
        return td;
    }

    this.tbody = function(config) {
        var tbody = this.template({
            tag: "tbody",
            type: "text/x-handlebars-template",
            id: this.mclsid("mtable-tbody-template", {everywhere: true, instance: true, config: config}),
        });
        var tr = this.template({
            tag: "tr",
            class: this.mclsid("mtable-trbody", {everywhere: true}),
        });
        var self = this;
        this.columns[config].forEach(function(column){
            var col = column.dataway.replace(".", "__");
            var td = self.td(config, column);
            tr.append(td);
        });
        tbody.append('{{#each datas}}');
        tbody.append(tr);
        tbody.append('{{/each}}');
        this.elements.mighty.append(tbody);
        this.elements[config].template = tbody;
    }

    this.displayall = function(config) {
        var displayall = this.template({
            tag: "button",
            class: this.mclsid("cmd-displayer-all", {everywhere: true}),
            id: this.mclsid("cmd-displayer-all", {everywhere: true, instance: true, config: config}),
        });
        displayall.append(this.translation.displayall);
        var self = this;
        displayall.click(function(){ 
            $(`.${self.mclsid("cmd-displayer-input", {everywhere: true, instance: true, config: config})}`).each(function() {
                var input = $(`#${this.id}`);
                input.prop('checked', true); 
                input.trigger("change");
            });
        });
        return displayall;
    }

    this.displaynone = function(config) {
        var displaynone = this.template({
            tag: "button",
            value: config,
            class: this.mclsid("cmd-displayer-none", {everywhere: true}),
            id: this.mclsid("cmd-displayer-none", {everywhere: true, instance: true, config: config}),
        });
        displaynone.append(this.translation.displaynone);
        var self = this;
        displaynone.click(function(){ 
            $(`.${self.mclsid("cmd-displayer-input", {everywhere: true, instance: true, config: config})}`).each(function() {
                var input = $(`#${this.id}`);
                input.prop('checked', false); 
                input.trigger("change");
            });
        });
        return displaynone;
    }

    this.displayinput = function(config, column) {
        var col = column.dataway.replace(".", "__");
        var label = this.template({tag: "label"});
        var input = this.template({
            tag: "input",
            type: "checkbox",
            value: col,
            id: this.mclsid("cmd-displayer-input", {everywhere: true, instance: true, config: config, after: col}),
            class: this.mclsid("cmd-displayer-input", {everywhere: true, instance: true, config: config}),
        });
        label.append(input);
        label.append(`<span>${column.title}</span>`);
        var show = true;
        if (column.hasOwnProperty("show")) { show = column.show; }
        input.prop('checked', show);
        var self = this;
        input.change(function(){
            var col = self.mclsid("mtable-col", {everywhere: true, instance: true, config: config, after: this.value});
            if (self.checkboxstate( $(`#${this.id}`) )) { $(`.${col}`).show(); } 
            else { $(`.${col}`).hide(); }
        });
        return label;
    }

    this.displayer = function(config) {
        var container = this.mclsid("cmd-displayer", {everywhere: true, instance: true});
        if (this.exist(container)) {
            container = $(`#${container}`);
            var displayer = this.template({
                tag: "div",
                class: this.mclsid("show", {everywhere: true, instance: true, config: config}),
                id: this.mclsid("cmd-displayer", {everywhere: true, instance: true}),
            });
            var button = this.template({
                tag: "button",
                value: config,
                class: this.mclsid("cmd-displayer", {everywhere: true}),
            });
            button.append(this.translation.displayer);
            var list = this.template({
                tag: "div",
                class: this.mclsid("cmd-displayer-list", {everywhere: true}),
                id: this.mclsid("cmd-displayer-list", {everywhere: true, instance: true, config: config}),
            });
            list.append(this.displayall(config));
            list.append(this.displaynone(config));
            var self = this;
            this.columns[config].forEach(function(column){
                list.append(self.displayinput(config, column));
            });
            displayer.append(button);
            displayer.append(list);
            list.hide();
            container.append(displayer);
            var self = this;
            button.click(function(){
                var list = $(`#${self.mclsid("cmd-displayer-list", {everywhere: true, instance: true, config: this.value})}`);
                if (list.is(':visible')) { list.hide(); }
                else { list.show(); }
            });
        }
    }

    this._nochange = this.nochange;
    this.nochange = function(options) {
        this._nochange(options);
        this.elements[options.config].container.removeClass('loading');
    }
    
    this._error = this.error;
    this.error = function(xhr, status, error, options) {
        this._error(xhr, status, error, options);
        this.elements[options.config].container.removeClass('loading');
    }   

    this.initialize = function() {
        for (config in this.config) {
            this.table(config);
            this.header(config);
            this.tbody(config);
        }
    }

    this.when = function(response, options) {
        var source = this.elements[options.config].template.html();
        var template = Handlebars.compile(source);
        var html = template({datas: response[this.ajax.results]});
        this.elements[options.config].tbody.html(html);
        if (this.is("displayer") && !this.is(`displayerinit${options.config}`)) {
            this.displayer(options.config);
            $(`.${this.mclsid("cmd-displayer-input", {everywhere: true, instance: true, config: options.config})}`).each(function() {
                var input = $(`#${this.id}`);
                input.trigger("change");
            });
            this.is(`displayerinit${options.config}`, true);
        }
        this.elements[options.config].container.removeClass('loading');
    }

}