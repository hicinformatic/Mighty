from django.core.management.base import CommandError
from os.path import isfile
import csv, uuid

from mighty.management import BaseCommand

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
        parser.add_argument('--csv', required=True)
        parser.add_argument('--label', required=True)
        parser.add_argument('--model', required=True)
        parser.add_argument('--comma', default=',')
        parser.add_argument('--encoding', default='utf8')

    def check_row(self, row):
        for field in self.fields_retrieve:
            if not self.test(row[field]):
                self.error.add(field, "Test fail", self.current_row)
                return False
        return True

    def do(self, options):
        self.csv = options.get('csv')
        self.comma = options.get('comma')
        self.encoding = options.get('encoding')
        if not isfile(self.csv): raise CommandError('CSV "%s" does not exist' % self.csv)
        with open(self.csv, encoding=self.encoding) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.comma)
            for row in reader: self.total_rows += 1
            self.logger.info('Total rows: %s' % self.total_rows)
            csvfile.seek(0)
            self.fields = reader.fieldnames
            for field in self.fields_retrieve:
                if field not in self.fields: raise CommandError('Field "%s" does not exist' % field)
            for row in reader:
                if self.pbar: self.progressBar(self.current_row, self.total_rows)
                else: self.logger.info('Line %s/%s' % (self.current_row, self.total_rows))
                if self.current_row > 0:
                    if self.check_row(row): self.do_line(row)
                    else: self.logger.error('Check datas failed')
                self.current_row += 1
    
    def do_line(self, row):
        model_args = {field: self.field(field, row) for field in self.fields_retrieve}
        try:
            obj = self.model.objects.get(**model_args)
        except self.model.DoesNotExist:
            obj = self.model(**model_args)
            obj.save()
        
        model_fields = {}
        for field in obj.fields():
            if field.name in row and self.test(row[field.name]) and field.name not in self.fields_forbidden:
                model_fields[field.name] = row[field.name]
        self.model.objects.filter(pk=obj.pk).update(**model_fields)
                
    