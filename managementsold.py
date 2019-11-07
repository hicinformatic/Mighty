from django.core.management.base import BaseCommand, CommandError
from mighty.fields import notsignhash
from mighty.functions import test, boolean_input
import os.path, csv, sys, logging, re

class BaseCommand(BaseCommand):
    help = 'Add from a CSV'
    logger = logging.getLogger('')
    row = 0
    totalrows = 0
    alerts = {}
    model = None
    errors = {}
    error_count = 0
    objects = []
    to_disconnect = []

    def log(self, level, msg):
        msg = getattr(self.style, str(level).upper())(msg)
        getattr(self.logger, str(level).lower())(msg)
        self.errors.append(msg)

    def error(self, key, msg):
        self.error_count += 1
        if key not in self.errors:
            self.errors[key] = []
        self.errors[key].append({'line': self.row, 'error': msg})

    def do_errors(self):
        for key, errors in self.errors.items():
            for error in errors:
                self.logger.error("key: %s, line: %s, error: %s" % (key, error["line"], error['error']))
        self.logger.error("number of errors: %s" % self.error_count)

    def startLog(self, verbosity=0):
        if verbosity == 0:
            self.logger.setLevel(logging.WARN)
        elif verbosity == 1:
            self.logger.setLevel(logging.INFO)
        elif verbosity > 1:
            self.logger.setLevel(logging.DEBUG)
        if verbosity > 2:
            self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler(self.stdout))
        self.logger.info('--- Start ---')

    def progressBar(self, value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def getSource(self, field):
        if self.source:
            if field in self.source:
                return self.source[field]
            elif "default" in self.source:
                return self.source["default"]
        return False

    def getOrNone(self, data):
        return data if not test(data) else None

    def getInt(self, number):
        if test(number):
            try:
                return int(number)
            except Exception as e:
                self.error('number', 'Not integer line: %s number: "%s"' % (self.row, number))
                return None
        return None

    def getFloat(self, integer):
        return float(str(integer).strip().replace(u'\xa0', u' ').replace(' ', '').replace(',', '').replace('€', '').replace('%', ''))

    def getNumber(self, integer):
        return int(str(integer).strip().replace(u'\xa0', u' ').replace(' ', '').replace(',', '').replace('€', '').replace('%', ''))

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

class AddModelFromCSV(BaseCommand):
    fields_mandatory = []
    fields_optional = []
    source = None

    def getField(self, field, line):
        value = line[self.afields[field]]
        if '(' in value and ')' in value:
            try:
                value = re.findall(r'(.+)(\(.+\))', value)[0]
                self.alerts[field] = {'info': value[1]}
                value = value[0]
            except Exception as e:
                self.error('info', 'Regex: %s Technical: %s' % (value, str(e)))
                return line[self.afields[field]].strip()
        return value.strip()


    def add_arguments(self, parser):
        parser.add_argument('--csv', required=True)
        parser.add_argument('--comma', default=',')
        parser.add_argument('--progressbar', default=False)

    def check_exist(self):
        if not os.path.isfile(self.csv):
            raise CommandError('CSV "%s" does not exist' % self.csv)

    def check_columns(self):
        for field in self.fields_mandatory:
            if field not in self.fields:
                raise CommandError('Field "%s" does not exist' % field)
        for field in self.fields_optional:
            if field not in self.fields:
                self.log('warning', 'Field "%s" does not exist' % field)

    def check_datas(self, row):
        for field in self.fields_mandatory:
            if test(row[field]):
                return True
        self.error(field, 'Check datas: "%s"' % row[field])
        return False

    def do_line(self, line):
        print('ok')
        for key in line:
            if line[key].lower() in self.line_overwrite:
                line[key] = self.line_overwrite[line[key].lower()]
            elif line[key].strip() in [None, '']:
                line[key] = None
        return line

    def do_delete(self):
        self.logger.info("Nombre de ligne traité: %s" % self.row)
        self.logger.info("Nombre d'objets': %s" % len(self.objects))
        if self.model is not None:
            count = self.model.objects.exclude(id__in=self.objects).count()
            self.logger.info("%s a supprimer: %s" % (self.model._meta.verbose_name, count))
            if count > 0:
                if boolean_input("Supprimer les objets en dehors des scopes de recherche?"):
                    self.model.objects.exclude(id__in=self.objects).delete()
                    self.logger.info("Les objets ont été supprimés")

    def do_before(self):
        pass

    def do_after(self):
        pass

    def sources(self):
        source = None
        for field in self.model._meta.fields:
            if field.attname not in notsignhash:
                fsource = self.getSource(field.attname)
                if fsource:
                    try:
                        source[field.attname] = fsource
                    except Exception as e:
                        source = {field.attname: fsource}
        return source

    def do_loop(self):
        with open(self.csv, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.comma)
            for row in reader:
                self.totalrows += 1
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, delimiter=self.comma)
            self.fields = reader.fieldnames
            self.check_columns()
            self.row = 1
            for row in reader:
                self.row += 1
                if self.pbar:
                    self.progressBar(self.row, self.totalrows)
                else:
                    self.logger.info('Line %s/%s' % (self.row, self.totalrows))
                if self.check_datas(row):
                    self.do_line(row)
                    self.alerts = {}
                else:
                    print('tata')

    def handle(self, *args, **options):
        self.startLog(options.get('verbosity'))
        self.csv = options.get('csv')
        self.pbar = options.get('progressbar')
        self.comma = options.get('comma') if 'comma' in options else ','
        self.check_exist()
        self.do_before()
        self.do_loop()
        self.do_after()
        self.do_delete()
        self.do_errors()
        self.logger.info('--- End ---')