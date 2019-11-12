from django.db.models import Q
from mighty.functions import make_searchable, test, logger

class Filter(object):
    config = {
        "operators": ["range", "in", "list"],
        "category": ":",
        "marker": "--",
        "operator": "~",
        "_separator": " ",
        "key_separator": "==",
        "range_separator": "-",
        "in_separator": ",",
        "list_separator": ",",
        "safe": "$",
    }

    def __init__(self, request, model):
        self.queryset = None
        self.model = model
        self.request = request
        self.filters = {}
        self.select_related = []
        self.prefetch_related = []
        self.params = {
            "searchex": {
                "param": "searchex",
                "mask": "iexact",
                "fields": {},
                **self.config,
            }, 
            "search": {
                "param": "search",
                "mask": "icontains",
                "fields": {},
                **self.config,
            }, 
            "filter":  {
                "param": "filter",
                "separator": " ",
                "fields": {},
                **self.config,

            }, 
            "exclude":  {
                "param": "exclude",
                "separator": " ",
                "fields": {},
                **self.config,
            }, 
            "order":  {
                "param": "order",
                "fields": {},
            }, 
            "distinct":  {
                "param": "distinct",
                "fields": {},
            },
        }

    def operators(self, param):
        return self.params[param]["operators"]
    
    def category(self, param):
        return self.params[param]["category"]

    def separator(self, param, key="_"):
        return self.params[param]["%sseparator" % key]

    def fields(self, param):
        return self.params[param]["fields"]

    def mask(self,param):
        return self.params[param]["mask"]

    def marker(self,param):
        return self.params[param]["marker"]

    def param(self, param):
        return self.params[param]["param"]

    def add(self, param, field, exact=False, *args, **kwargs):  
        self.params[param]["fields"][field] = kwargs

    def distinct(self):
        distinct_param = self.request.GET.get(self.param("distinct"))
        return distinct_param.split() if test(distinct_param) else list(self.fields("distinct").keys())
    
    def order(self):
        order_param = self.request.GET.get(self.param("order"))
        return order_param.split() if test(order_param) else list(self.fields("order").keys())

    def getQ_range(self, param, field, value, *args, **kwargs):
        operator = kwargs["operator"] if "operator" in kwargs else Q.AND
        negative = kwargs["negative"] if "negative" in kwargs else False
        value = value.split(self.separator(param, "range_"))
        return self.get_Q("%s__gte" % field, value[0], negative).add(self.get_Q("%s__lte" % field, value[1]), operator)

    def getQ_in(self, param, field, value, *args, **kwargs):
        operator = kwargs["operator"] if "operator" in kwargs else Q.AND
        negative = kwargs["negative"] if "negative" in kwargs else False
        value = value.split(self.separator(param, "in_"))
        return self.get_Q("%s__in" % field, value, negative)

    def getQ_list(self, param, field, value, operator=Q.AND, negative=False):
        value = value.split(self.separator(param, "list_"))
        q = Q()
        for v in value:
            q.add(self.get_Q("%s" % field, v), operator)
        return q

    def get_Q(self, field, value, negative=False):
        logger("mighty", "info", "field: %s, value: %s, negative: %s" % (field, value, negative), self.request.user)
        if isinstance(value, str):
            if value[:1] == self.config["safe"]:
                return ~Q(**{field: value[1:]}) if negative else Q(**{field: value[1:]})    
            return ~Q(**{field: make_searchable(value)}) if negative else Q(**{field: make_searchable(value)})
        return ~Q(**{field: value}) if negative else Q(**{field: value})

    def get_S(self, search, ex=False):
        psearch = "searchex" if ex else "search"
        for field, args in self.fields(psearch).items():
            field = "{field}__{mask}".format(field=field, mask=args["mask"] if "mask" in args else self.mask(psearch))
            try:
                the_Q |= self.get_Q(field, search, negative=field["negative"] if "mask" in field else False)
            except UnboundLocalError:
                the_Q = self.get_Q(field, search, negative=field["negative"] if "mask" in field else False)
        return the_Q

    def search(self, ex=False, *args, **kwargs):
        psearch = "searchex" if ex else "search"
        search_param = self.request.GET.get(self.param(psearch))
        if test(search_param):
            search_param = search_param.split(self.separator(psearch))
            the_Q = self.get_S(search_param[0], ex)
            if len(search_param) > 1:
                for search in search_param[1:]:
                    the_Q.add(self.get_S(search), kwargs["operator"] if "operator" in kwargs else Q.AND)
            return the_Q
        return None

    def dispatch(self, param, filtr):
        field, value = filtr.split(self.separator(param, "key_"))
        category, field = field.split(self.category(param))
        #if self.operators(param) in category[0]:
        #    pass
        return category, field, value

    def get_F(self, field, value, *args, **kwargs):
        param = kwargs["param"] if "param" in kwargs else "filter"
        operator = kwargs["operator"] if "operator" in kwargs else Q.AND
        negative = kwargs["negative"] if "negative" in kwargs else False
        try:
            if self.marker(param) in field:
                field = field.split(self.marker(param))
                field[1] = field[1].split(self.config["operator"])
                if len(field[1]) > 1 and field[1][1] == 'or':
                    kwargs["operator"] = Q.OR
                    operator = Q.OR
                field[1] = field[1][0]
                if field[1] in self.operators(param):
                    return getattr(self, "getQ_%s" % field[1])(param, field[0], value, operator, negative)
            else:
                return self.get_Q(field, value, negative)
        except ValueError:
            pass
        return None

    def filter(self, *args, **kwargs):
        param = kwargs["param"] if "param" in kwargs else "filter"
        operator = kwargs["operator"] if "operator" in kwargs else Q.OR
        negative = kwargs["negative"] if "negative" in kwargs else False
        filter_param = self.request.GET.get(self.param(param))
        if test(filter_param):
            filters = {}
            for filtr in filter_param.split(self.separator(param)):
                category, field, value = self.dispatch(param, filtr)
                if category not in filters:
                    filters[category] = []
                filters[category].append(self.get_F(field, value, **kwargs))
            for category, filtr in filters.items():
                newf = Q()
                for filtr in filters[category]:
                    newf |= filtr
                filters[category] = newf
            newf = Q()
            for category, filtr in filters.items():
                newf &= filtr
            filters = newf
            return filters
        return None
            
    def get(self):
        logger("mighty", "info", "model: %s" % self.model.__name__, self.request.user)
        queryset = self.queryset if self.queryset else self.model.objects
        if self.select_related: queryset = queryset.select_related(*self.select_related)
        if self.prefetch_related: queryset = queryset.prefetch_related(*self.prefetch_related)

        q = Q()
        qS = self.search()
        if qS: q.add(qS, Q.AND)
        
        qSe = self.search(True)
        if qSe: q.add(qSe, Q.AND)

        qF = self.filter()
        if qF: q.add(qF, Q.AND)

        qE = self.filter(param="exclude")
        logger("mighty", "info", "exclude: %s" % qE, self.request.user)
        if qE: queryset = queryset.exclude(qE)

        logger("mighty", "info", "filters: %s" % q, self.request.user)

        order = self.order()
        logger("mighty", "info", "order_by: %s" % order, self.request.user)
        if order: queryset = queryset.order_by(*order)

        distinct = self.distinct()
        logger("mighty", "info", "distinct: %s" % distinct, self.request.user)
        if distinct:
            dqueryset = self.queryset if self.queryset else self.model.objects
            if self.select_related: dqueryset = dqueryset.select_related(*self.select_related)
            if self.prefetch_related: dqueryset = dqueryset.prefetch_related(*self.prefetch_related)
            q.add(Q(id__in=dqueryset.filter(q).order_by(*distinct).distinct(*distinct).values_list('id', flat=True)), Q.AND)

        return queryset, q