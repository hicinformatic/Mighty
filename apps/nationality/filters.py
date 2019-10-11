from mighty.filters import Filter
from mighty.models.nationality import Nationality

def NationalityFilter(view, request):
    NationalityFilter = Filter(request, Nationality)
    NationalityFilter.add("search", "to_search")
    NationalityFilter.add("search", "country")
    NationalityFilter.add("search", "alpha2")
    NationalityFilter.add("search", "alpha3")
    NationalityFilter.add("search", "numeric")
    return NationalityFilter.get()