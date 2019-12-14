from django.core.management.base import CommandError
from os.path import isfile
import csv

from mighty.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--csv', required=True)
        parser.add_argument('--comma', default=',')

    def check_row(self, row):
        if self.bypasscheck:
            return True
        for field in self.fields_retrieve:
            sfield = self.good_field(field)
            if not self.test(row[sfield]):
                self.error.add(field, "Test failed for field: %s, value: %s" % (field, row[self.good_field(field)]), self.current_row)
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
                if self.current_row > 1:
                    if self.check_row(row): self.do_line(row)
                    else: self.logger.error('Check datas failed')
                self.current_row += 1
    
    def do_line(self, row):
        self.current_datas = row
        self.alerts = {}
        models_args = {field: self.field(field, row) for field in self.fields_retrieve}

        obj = self.give_one(row, models_args)
        if not obj:
            obj = self.search_one(row, models_args)
        if not obj:
            obj = self.create_one(row, models_args)

        if obj:
            model_fields = {}
            for field in obj.fields():
                if field.name not in self.fields_forbidden:
                    try:
                        sfield = self.field(field.name, row)
                        if hasattr(sfield, "strip"):
                            sfield = sfield.strip()
                        if sfield:
                            if field.__class__.__name__ == 'ManyToManyField':
                                getattr(obj, field.name).add(*sfield)
                            else:
                                setattr(obj, field.name, sfield)
                    except Exception as e:
                        error = (self.good_field(field.name), row[self.good_field(field.name)], obj, str(e))
                        self.error.add(field, "Field error: %s, value: %s, - %s, error: %s" % error, self.current_row)

            for afield in self.alerts:
                for alert in self.alerts[afield]:
                    obj.add_alert(alert, afield)
            obj.save()
        