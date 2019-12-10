from django.core.management.base import BaseCommand, CommandError
from django.utils.six.moves import input
from mighty import functions
import os.path, csv, sys, logging, re, time, uuid

now = time.strftime("%Y%m%d")

class Error:
    count = 0
    errors = {}

    def __init__(self, logger):
        self.logger = logger

    def moreone(self):
        self.count += 1

    def add(self, key, msg, current_row=False):
        self.moreone()
        if key not in self.errors: self.errors[key] = []
        if current_row:
            self.errors[key].append("%s | line: %s" % (msg, current_row))
        else:
            self.errors[key].append(msg)

class BaseCommand(BaseCommand):
    help = 'Commande Base'
    logger = logging.getLogger('')
    error = Error
    fields_forbidden = ['id', 'display']
    fields_retrieve = ['uid',]
    fields_associates = {}
    fields_unique = []
    foreignkey = {}
    reverse_associates = {}
    source = {}
    found = {}
    total_rows = 0
    current_row = 0

    def get_model(self, label, model):
        return functions.get_model(label, model)

    def input_get_model(self, reference):
        return functions.input_get_model(reference)

    def boolean_input(self, question, default='n'):
        return functions.boolean_input(question, default)

    def object_search(self, model, reference):
        return functions.object_search(model, reference)

    def multipleobjects_onechoice(self, objects_list, reference, model):
        return functions.multipleobjects_onechoice(objects_list, reference, model)

    def get_or_none(self, data):
        return functions.get_or_none(data)

    def get_uid(self, uid):
        return uuid.UUID('{%s}' % uid)

    def make_float(self, flt):
        return functions.make_float(flt)

    def make_int(self, itg):
        return functions.make_int(itg)

    def make_searchable(self, input_str):
        return functions.make_searchable(input_str)

    def make_string(self, input_str):
        return functions.make_string(input_str)

    def test(self, data):
        return functions.test(data)

    def similar_text(self, str1, str2):
        return functions.similar_text(str1, str2)

    def foreignkey_from(self, model, field, data, ret):
        return functions.foreignkey_from(model, field, data, ret)

    def create_parser(self, prog_name, subcommand, **kwargs):
        self.subcommand = subcommand
        return super().create_parser(prog_name, subcommand)

    def progressBar(self, value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def startLog(self, verbosity=0):
        if verbosity == 0: self.logger.setLevel(logging.WARN)
        elif verbosity == 1: self.logger.setLevel(logging.INFO)
        elif verbosity > 1: self.logger.setLevel(logging.DEBUG)
        if verbosity > 2: self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler(self.stdout))
        self.logger.info('--- Start ---')

    def get_fk_from(self, fields):
        if self.test(fields):
            for field in fields.split(','):
                self.foreignkey[field] = {
                    'model': self.input_get_model(field), 
                    'field': input("What field to use for the reference %s: " % field),
                    'data': input("What field data to use for the reference %s: " % field),
                    'return': input("What field return to use for the reference %s: " % field)
                }
                self.logger.info('Model use for field %s: %s' % (field, self.foreignkey[field]))

    def add_arguments(self, parser):
        parser.add_argument('--logfile', default="%s_%s.log" % (str(self.subcommand).lower(), now))
        parser.add_argument('--progressbar', action="store_true")
        parser.add_argument('--create', action="store_true")
        parser.add_argument('--myself', action="store_true")
        parser.add_argument('--label', required=True)
        parser.add_argument('--model', required=True)
        parser.add_argument('--search', default=None)
        parser.add_argument('--retrieve', default=None)
        parser.add_argument('--forbidden', default=None)
        parser.add_argument('--foreignkey', default=None)
        parser.add_argument('--encoding', default='utf8')

    def handle(self, *args, **options):
        self.error = Error(self.logger)
        self.search = options.get('search')
        self.create = options.get('create')
        self.myself = options.get('myself')
        retrieve = options.get('retrieve')
        if retrieve: self.fields_retrieve = [field for field in retrieve.split(",")]
        forbidden = options.get('forbidden')
        if forbidden: self.fields_forbidden = [field for field in forbidden.split(",")]
        self.pbar = options.get('progressbar')
        self.startLog(options.get('verbosity'))
        self.encoding = options.get('encoding')
        self.model = self.get_model(options.get('label'), options.get('model'))
        self.before(options)
        self.get_fk_from(options.get('foreignkey'))
        self.do(options)
        self.after(options)
        self.errors_in_logfile(options.get('logfile'))
        self.logger.info('--- End ---')

    def before(self, options):
        pass

    def do(self, options):
        self.logger.info('--- Doing ---')

    def after(self, options):
        pass

    def errors_in_logfile(self, logfile):
        with open(logfile, "w") as f:
            for key, errors in self.error.errors.items():
                f.write("==== Field in error: %s (errors: %s)====\n" % (key, len(errors)))
                for error in errors:
                   f.write("%s\n" % error)
        f.close()
        self.logger.info('Errors: %s' % self.error.count)

    def field(self, field, row):
        #sfield = self.fields_associates[field] if field in self.fields_associates else field
        #if hasattr(self, 'get_%s' % field):
        #    return getattr(self, 'get_%s' % field)(row[sfield])
        #return row[sfield] if self.test(row[sfield]) else None
        sfield = self.fields_associates[field] if field in self.fields_associates else field
        if hasattr(self, 'get_%s' % field):
            return getattr(self, 'get_%s' % field)(row[sfield])
        elif sfield in row and self.test(row[sfield]):
            if sfield in self.foreignkey:
                return self.foreignkey_from(
                    self.foreignkey[sfield]['model'],
                    self.foreignkey[sfield]['field'],
                    row[self.foreignkey[sfield]['data']],
                    self.foreignkey[sfield]['return']
                )
            return row[sfield]
        return None
