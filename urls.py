from django.conf import settings

app_name = 'mighty'
urlpatterns = []

if 'mighty.apps.nationality' in settings.INSTALLED_APPS:
    from mighty.apps.nationality import urls as urls_nationality
    urlpatterns += urls_nationality.urlpatterns

if 'mighty.apps.user' in settings.INSTALLED_APPS:
    from mighty.apps.user import urls as urls_user
    urlpatterns += urls_user.urlpatterns

if 'mighty.apps.authenticate' in settings.INSTALLED_APPS:
    from mighty.apps.authenticate import urls as urls_authenticate
    urlpatterns += urls_authenticate.urlpatterns

if 'mighty.apps.grapher' in settings.INSTALLED_APPS:
    from mighty.apps.grapher import urls as urls_grapher
    urlpatterns += urls_grapher.urlpatterns