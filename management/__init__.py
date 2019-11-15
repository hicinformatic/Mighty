from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from mighty.functions import test, boolean_input, make_float, make_int, get_or_none, make_searchable
import os.path, csv, sys, logging, re, time

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

    def boolean_input(self, question, default='n'):
        return boolean_input(question, default)

    def get_or_none(self, data):
        return get_or_none(data)

    def get_uid(self, uid):
        return uuid.UUID('{%s}' % uid)

    def make_float(self, flt):
        return make_float(flt)

    def make_int(self, itg):
        return make_int(itg)

    def make_searchable(self, input_str):
        return make_searchable(input_str)

    def test(self, data):
        return test(data)
    
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

    def add_arguments(self, parser):
        parser.add_argument('--progressbar', default=False)
        parser.add_argument('--logfile', default="%s_%s.log" % (str(self.subcommand).lower(), now))

    def handle(self, *args, **options):
        self.startLog(options.get('verbosity'))
        self.error = Error(self.logger)
        self.pbar = options.get('progressbar')
        self.get_model(options.get('label'), options.get('model'))
        self.do(options)
        self.get_errors(options.get('logfile'))
        self.logger.info('--- End ---')

    def get_model(self, label, model):
        self.model = apps.get_model(label, model)

    def do(self, options):
        self.logger.info('--- Doing ---')

    def get_errors(self, logfile):
        f = open(logfile, "w")
        for key, errors in self.error.errors.items():
            f.write("==== Field in error: %s (errors: %s)====\n" % (key, len(errors)))
            for error in errors:
                f.write("%s\n" % error)
        f.close()
        self.logger.info('Errors: %s' % self.error.count)

    def field(self, field, row):
        sfield = self.fields_associates[field] if field in self.fields_associates else field
        if hasattr(self, 'get_%s' % field):
            return getattr(self, 'get_%s' % field)(row[sfield])
        return row[sfield]
