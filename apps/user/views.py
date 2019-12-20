from django.conf import settings
from mighty.views import ModelViewSet, DetailView
from mighty.models.user import User
from mighty.apps.user import filters, fields

class UserMe(DetailView):
    no_permission = True
    def get_header(self):
        return {'title': 'me',}

    def get_object(self, queryset=None):
        user = User.objects.get(id=self.request.user.id)
        print(user)
        print(self.request.user.has_perm(user.perm('detail')))
        return None

    def get_context_data(self, **kwargs):
        context = super(UserMe, self).get_context_data(**kwargs)
        if "oauth2_provider" in settings.INSTALLED_APPS:
            from oauth2_provider.models import Application
            applications = Application.objects.filter(user=self.object)
            context.update({'applications': applications})
        return context

class UserViewSet(ModelViewSet):
    me_no_permission = True
    model = User
    filter_model = filters.UserFilter
    add_fields = fields.add
    export_fields = fields.export
    list_is_ajax = True
    fields = fields.lst

    def __init__(self, model=None):
        super(UserViewSet, self).__init__()
        self.addNotuseid('me')
        self.addView('me', UserMe, 'me/')

if 'rest_framework' in settings.INSTALLED_APPS:
    from mighty.views.api import ApiModelViewSet
    from mighty.apps.user.serializers import UserSerializer
    from rest_framework.generics import RetrieveAPIView

    class UserMeApi(RetrieveAPIView):
        slug = '<uuid:uid>'
        def get_object(self):
            return User.objects.get(id=52)

    class UserApiViewSet(ApiModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        filter_model = filters.UserFilter
        model = User
        serializer_class = UserSerializer

        def __init__(self, model=None):
            super(UserApiViewSet, self).__init__()
            self.addView('me', UserMeApi, '%s/me/')