from mighty.views import ModelViewSet, ListView
from mighty.models.user import Nationality
from mighty.apps.nationality import filters

class NationalityViewSet(ModelViewSet):
    slug = '<int:pk>'
    filter_model = filters.NationalityFilter
    model = Nationality
    list_display = ('__str__', 'image_html',)
    fields = ('country', 'alpha2', 'alpha3', 'numeric')