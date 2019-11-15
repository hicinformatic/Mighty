from django.core.management.base import CommandError
from django.apps import apps
from os.path import isfile
import csv, uuid

from mighty.management import BaseCommand

class updateModel(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--progressbar', default=False)

    def handle(self, *args, **options):
        self.startLog(options.get('verbosity'))
        self.pbar = options.get('progressbar')
        self.do_loop()
        self.logger.info('--- End ---')

    def do_loop(self):
        self.totalrows = self.model.objects.all().count()
        for obj in self.model.objects.all():
            self.row+=1
            if self.pbar:
                self.progressBar(self.row, self.totalrows)
            else:
                self.logger.info('Update object %s/%s "%s"' % (self.row, self.totalrows, obj.display))
            self.alerts = {}
            self.do_update(obj)
        self.do_after()

    def do_after(self):
        pass

class Command(BaseCommand):
    fields_forbidden = ['id',]
    fields_retrieve = ['uid',]
    fields_associates = {}
    total_rows = 0
    current_row = 0
    source = {}

    def create_parser(self, prog_name, subcommand, **kwargs):
        self.subcommand = subcommand
        return super().create_parser(prog_name, subcommand)

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--label', required=True)
        parser.add_argument('--model', required=True)
        parser.add_argument('--encoding', default='utf8')

    def do(self, options):
        self.total_rows = self.model.objects.all().count()
        self.logger.info('Total rows: %s' % self.total_rows)
        for obj in self.model.objects.all():
            if self.pbar: self.progressBar(self.current_row, self.totalrows)
            else: self.logger.info('Update object %s/%s "%s"' % (self.current_row, self.total_rows, obj.display))
            self.do_object(obj)
            self.current_row += 1

    def field(self, field, row):
        field = self.fields_associates[field] if field in self.fields_associates else field
        if hasattr(self, 'get_%s' % field):
            return getattr(self, 'get_%s' % field)(row[field])
        return row[field]
    
    def do_object(self, obj):
        obj.save()


    