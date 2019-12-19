function Mconfig(url, options) {
    //this.id = id;
    this.burl = location.protocol + '//' + location.host + location.pathname;
    this.url = url;
    this.options = options = options === undefined ? {} : options;

    //this.elements = {commands: {},};
    this.form = {search: null,};
    this.config = {};
    this.timer = {};
    this.questions = {i: {}, is: {}, lasts: {},};
    this.lists = {filters: [], excludes: [], tristates: {},};
    this.forces = {filter: null, exclude: null,};

    this.bid = options.hasOwnProperty("bid") ? options.bid : "mighty";
    this.datatype = options.hasOwnProperty("bid") ? options.datatype : "json";
    this.method = options.hasOwnProperty("method") ? options.bid : "GET";
    this.debug = options.hasOwnProperty("debug") ? options.debug : false;
    this.timeout = options.hasOwnProperty("timeout") ? options["timeout"] : 10000;
    this.msdelay = options.hasOwnProperty("msdelay") ? options["msdelay"] : 500;
    this.by = options.hasOwnProperty("by") ? options["by"] : 50;
    this.show = null;

    this.steps = {ready: 0, prepare: 1, send: 2, success: 3, complete: 4, error: 5,};
    this.canshared = ["search", "searchex", "filter", "filterand", "filteror", "exclude", "excludeand", "excludeor"];
    this.cantshared = ["order", "distinct", "page"];
    this.actions = {top: "-top", previous: "-previous", next: "-next",}

    this.ajax = {
        count: "count",
        results: "results",
    }

    this.colors = {
        debug: "#FFFFFF",
        info: "#7bd5ff",
        warn: "#FF7F5D",
        error: "#FF3232",
    };

    this.icons = {
        counter: "&sum;",
        searchex: "&equals;",
        displayer: "&Vert;",
        displayall: "&#9745;",
        displaynone: "&#9744;",
        up: '&darr;',
        down: '&uarr;', 
    };

    this.translation = {
        counter: "Results",
        paginate: "Page",
        search: "Search",
        searchex: "Exact search",
        displayer: "Columns displayed",
        displayall: this.icons.displayall+" Show all",
        displaynone: this.icons.displaynone+" Hide all",
    };
}