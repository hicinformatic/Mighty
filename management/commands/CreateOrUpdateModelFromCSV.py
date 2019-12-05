from django.core.management.base import CommandError
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from os.path import isfile
import csv

from mighty.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--csv', required=True)
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
        obj = False
        models_srch = False
        models_args = {field: self.field(field, row) for field in self.fields_retrieve}
        if self.test(self.search) and self.field(self.search, row):
            for field in self.search.split(","):
                for search in self.field(field, row).split(" "):
                    if models_srch:
                        models_srch = models_srch & Q(to_search__icontains=search)
                    else:
                        models_srch = Q(to_search__icontains=search)

        try:
            obj = self.model.objects.get(Q(**models_args) | models_srch) if models_srch else self.model.objects.get(Q(**models_args))
            update = True
        except self.model.DoesNotExist:
            if self.create:
                sobj = self.field(self.search, row)
                if sobj not in self.found:
                    if self.myself:
                        obj = self.object_search(self.model, sobj)
                        if obj:
                            self.found[sobj] = obj
                            update = True
                    elif self.test(models_args):
                        obj = self.model(**models_args)
                        obj.save()
                        update = True
                else:
                    obj = self.found[sobj]
                    update = True
        except MultipleObjectsReturned:
            objects_list = self.model.objects.filter(Q(**models_args) | models_srch) if models_srch else self.model.objects.get(Q(**models_args))
            obj = self.multipleobjects_onechoice(objects_list, str(models_args), self.model)
            update = True if obj else False
            
        if update:
            model_fields = {}
            for field in obj.fields(['ManyToOneRel',]):
                if field.name not in self.fields_forbidden:
                    sfield = self.field(field.name, row)
                    if sfield :
                        setattr(obj, field.name, sfield)
            obj.save()    