from django.db.models import Manager
from django.db.models import Count, Avg, Max, Min, When, Case, IntegerField, DecimalField, F, Q

class AnnotateManager(Manager):
    annotate_fields = {}

    def add_count(self, field):
        self.annotate_fields['count_%s' % field] = Count(field)


    def get_queryset(self):
        return super().get_queryset().annotate(count_mandate=Count('mandate'))