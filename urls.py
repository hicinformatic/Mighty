from django.urls import include, path
from django.conf import settings

app_name = 'mighty'
urlpatterns = []

if 'mighty.apps.nationality' in settings.INSTALLED_APPS:
    from mighty.apps.nationality import urls as urls_nationality
    urlpatterns += urls_nationality.urlpatterns

    #if 'rest_framework' in settings.INSTALLED_APPS:
    #    from mighty.apps.nationality.urls import api as urls_nationatliy_api
    #    apipatterns += urls_nationatliy_api.apipatterns

if 'mighty.apps.user' in settings.INSTALLED_APPS:
    from mighty.apps.user import urls as urls_user
    urlpatterns += urls_user.urlpatterns

    #if 'rest_framework' in settings.INSTALLED_APPS:
    #    from mighty.apps.user.urls import api as urls_user_api
    #    apipatterns += urls_user_api.apipatterns

if 'mighty.apps.authenticate' in settings.INSTALLED_APPS:
    from mighty.apps.authenticate import urls as urls_authenticate
    urlpatterns += urls_authenticate.urlpatterns

    #if 'rest_framework' in settings.INSTALLED_APPS:
    #    from mighty.apps.user.urls import api as urls_authenticate_api
    #    apipatterns += urls_authenticate_api.apipatterns