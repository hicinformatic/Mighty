from django.conf import settings
from mighty.views import ModelViewSet, ListView
from mighty.models.nationality import Nationality
from mighty.apps.nationality import filters


class NationalityViewSet(ModelViewSet):
    slug = '<int:pk>'
    filter_model = filters.NationalityFilter
    model = Nationality
    list_display = ('__str__', 'image_html',)
    fields = ('country', 'alpha2', 'alpha3', 'numeric')

if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.views.api import ApiModelViewSet
    from mighty.apps.nationality.serializers import NationalitySerializer

    class NationalityApiViewSet(ApiModelViewSet):
        slug = '<int:pk>'
        filter_model = filters.NationalityFilter
        model = Nationality
        list_display = ('__str__', 'image_html',)
        fields = ('country', 'alpha2', 'alpha3', 'numeric')
        queryset = Nationality.objects.all()
        serializer_class = NationalitySerializer

