from django.conf import settings

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .. import models, serializers, filters

""" Nationality """
class NationalityList(generics.ListAPIView):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalitySerializer

class NationalityDetail(generics.RetrieveAPIView):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalitySerializer

class NationalityCreate(generics.CreateAPIView):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalitySerializer

class NationalityUpdate(generics.UpdateAPIView):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalitySerializer

class NationalityDelete(generics.DestroyAPIView):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalitySerializer

    def get_queryset(self):
        queryset, q = filters.NationalityFilter(self.request)
        return queryset.filter(q)

""" User """
class UserList(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        queryset, q = filters.UserFilter(self.request)
        return queryset.filter(q)

class UserDetail(generics.RetrieveAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserUpdate(generics.UpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDelete(generics.DestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

if 'mighty.app.extend' in settings.INSTALLED_APPS:
    class UserExtendList(generics.ListAPIView):
        queryset = models.UserExtend.objects.all()
        serializer_class = serializers.UserExtendSerializer

    def get_queryset(self):
        queryset, q = filters.UserExtendFilter(self.request)
        return queryset.filter(q)

    class UserExtendDetail(generics.RetrieveAPIView):
        queryset = models.UserExtend.objects.all()
        serializer_class = serializers.UserExtendSerializer

    class UserExtendCreate(generics.CreateAPIView):
        queryset = models.UserExtend.objects.all()
        serializer_class = serializers.UserExtendSerializer

    class UserExtendUpdate(generics.UpdateAPIView):
        queryset = models.UserExtend.objects.all()
        serializer_class = serializers.UserExtendSerializer

    class UserExtendDelete(generics.DestroyAPIView):
        queryset = models.UserExtend.objects.all()
        serializer_class = serializers.UserExtendSerializer

    class UserHistoryList(generics.ListAPIView):
        queryset = models.UserHistory.objects.all()
        serializer_class = serializers.UserHistorySerializer

    def get_queryset(self):
        queryset, q = filters.UserHistoryFilter(self.request)
        return queryset.filter(q)

    class UserHistoryDetail(generics.RetrieveAPIView):
        queryset = models.UserHistory.objects.all()
        serializer_class = serializers.UserHistorySerializer

    class UserHistoryCreate(generics.CreateAPIView):
        queryset = models.UserHistory.objects.all()
        serializer_class = serializers.UserHistorySerializer

    class UserHistoryUpdate(generics.UpdateAPIView):
        queryset = models.UserHistory.objects.all()
        serializer_class = serializers.UserHistorySerializer

    class UserHistoryDelete(generics.DestroyAPIView):
        queryset = models.UserHistory.objects.all()
        serializer_class = serializers.UserHistorySerializer
