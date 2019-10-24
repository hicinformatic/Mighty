from mighty.filters import Filter
from mighty.models.grapher import Graph

def GraphFilter(view, request):
    GraphFilter = Filter(request, Graph)
    GraphFilter.add("search", "to_search")
    GraphFilter.add("search", "country")
    GraphFilter.add("search", "alpha2")
    GraphFilter.add("search", "alpha3")
    GraphFilter.add("search", "numeric")
    return GraphFilter.get()