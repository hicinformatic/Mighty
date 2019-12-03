from django.core.management.base import CommandError
from django.db.models import Q
from os.path import isfile
import csv

from mighty.management import BaseCommand

class Command(BaseCommand):
    total_rows = 0
    current_row = 0

    def create_parser(self, prog_name, subcommand, **kwargs):
        self.subcommand = subcommand
        return super().create_parser(prog_name, subcommand)

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--csv', required=True)
        parser.add_argument('--label', required=True)
        parser.add_argument('--model', required=True)
        parser.add_argument('--comma', default=',')

    def check_row(self, row):
        for field in self.fields_retrieve:
            sfield = self.fields_associates[field] if field in self.fields_associates else field
            if not self.test(row[sfield]):
                self.error.add(field, "Test fail", self.current_row)
                return False
        return True

    def do(self, options):
        self.csv = options.get('csv')
        self.comma = options.get('comma')
        if not isfile(self.csv): raise CommandError('CSV "%s" does not exist' % self.csv)
        with open(self.csv, encoding=self.encoding) as csvfile:
            self.reverse_associates = {v: k for k, v in self.fields_associates.items()}
            reader = csv.DictReader(csvfile, delimiter=self.comma)
            for row in reader: self.total_rows += 1
            self.logger.info('Total rows: %s' % self.total_rows)
            csvfile.seek(0)
            self.fields = reader.fieldnames
            for field in self.fields_retrieve:
                sfield = self.fields_associates[field] if field in self.fields_associates else field
                if sfield not in self.fields: raise CommandError('Field "%s" does not exist' % field)
            for row in reader:
                if self.pbar: self.progressBar(self.current_row, self.total_rows)
                else: self.logger.info('Line %s/%s' % (self.current_row, self.total_rows))
                if self.current_row > 0:
                    if self.check_row(row): self.do_line(row)
                    else: self.logger.error('Check datas failed')
                self.current_row += 1
    
    def do_line(self, row):
        model_args = {field: self.field(field, row) for field in self.fields_retrieve}
        models_srch = Q()
        for field in self.field("denomination", row).split(" "):
            models_srch.add


        models_srch = {"to_search": field for field in self.field("denomination", row).split(" ")}
        print(models_srch)
        try:
            obj = self.model.objects.get(Q(**model_args) | Q(**models_srch))
        except self.model.DoesNotExist:
            if row["Société"] not in self.found:
                obj = self.object_search(self.model, row["Société"])
                if obj is None:
                    obj = self.model(**model_args)
                    obj.save()
                else:
                    self.found[row["Société"]] = obj
            elif row["Société"] not in self.found:
                obj = self.found[row["Société"]]
        
        #model_fields = {}
        #for field in obj.fields():
        #    if field.name not in self.fields_forbidden:
        #        if field.name in row and self.test(row[field.name]):
        #            setattr(obj, field.name, self.field(field.name, row))
        #        elif self.reverse_associates[field.name] in row and self.test(row[self.reverse_associates[field.name]]):
        #            setattr(obj, field.name, self.field(field.name, row))
        #obj.save()
        #        model_fields[field.name] = self.field(field.name, row)
        #self.model.objects.filter(pk=obj.pk).update(**model_fields)
                
    