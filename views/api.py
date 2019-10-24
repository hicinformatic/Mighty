from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from mighty.views import ModelViewSet
from mighty.permissions import HasMightyPermission

class ListAPIView(ListAPIView):
    def get_queryset(self):
        if self.filter_model is None:
            return super().get_queryset()
        else:
            queryset, q = self.filter_model(self.request)
        return queryset.filter(q)

class DisableApiView(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        return self.disable(request, *args, **kwargs)

    def disable(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_disable(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_disable(self, instance):
        instance.disable()

class EnableApiView(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        return self.enable(request, *args, **kwargs)

    def enable(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_enable(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_enable(self, instance):
        instance.enable()

class ApiModelViewSet(ModelViewSet):
    permission_classes = [HasMightyPermission]
    views = {
        'list':    { 'view': ListAPIView, 'url': '' },
        'add':     { 'view': CreateAPIView, 'url': 'add/' },
        'detail':  { 'view': RetrieveAPIView, 'url': '%s/detail/' },
        'change':  { 'view': UpdateAPIView, 'url': '%s/change/' },
        'delete':  { 'view': DestroyAPIView, 'url': '%s/delete/' },
        'enable':  { 'view': EnableApiView, 'url': '%s/enable/' },
        'disable': { 'view': DisableApiView, 'url': '%s/disable/' },
    }

    def view(self, view, *args, **kwargs):
        View = super().view(view)
        View.permission_classes = self.permission_classes
        View.queryset = self.queryset
        View.serializer_class = self.serializer_class
        View.lookup_field = 'pk'
        return View

    def name(self, view):
        return 'api-%s-%s' % (str(self.model.__name__.lower()), view)

#from django.shortcuts import get_object_or_404
#from rest_framework import viewsets
#from rest_framework.response import Response
#from rest_framework.decorators import action

#class ApiModelViewSet(viewsets.ModelViewSet):
#    queryset = None
#    serializer_class = None
#    filter_model = None
#
#    @action(methods=['post',], detail=False, url_path='add', url_name='add')
#    def add(self, request, *args, **kwargs):
#        serializer = self.serializer_class(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(serializer.data)
#
#    def list(self, request):
#        if self.filter_model is None:
#            queryset = self.queryset
#        else:
#            queryset, q = self.filter_model(self.request)
#            queryset = queryset.filter(q)
#        return Response(self.serializer_class(queryset, many=True).data)
#
#    @action(detail=True, url_path='detail', url_name='detail')
#    def odetail(self, request, pk=None):
#        return self.retrieve(request, pk)
#
#    @action(methods=['get', 'post',], detail=True, url_path='change', url_name='change')
#    def change(self, request, pk=None, *args, **kwargs):
#        return self.update(request, pk)
    