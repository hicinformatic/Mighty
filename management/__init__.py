from django.core.management.base import BaseCommand, CommandError
from mighty.functions import test, boolean_input, make_float, make_int, get_or_none
import os.path, csv, sys, logging, re

class Error:
    count = 0
    errors = {}

    def __init__(self, logger):
        self.logger = logger

    def moreone(self):
        self.count += 1

    def add(self, key, msg):
        self.error.moreone()
        if key not in self.errors: self.errors[key] = []
        self.errors[key].append({'message': msg})

class BaseCommand(BaseCommand):
    help = 'Commande Base'
    logger = logging.getLogger('')

    def boolean_input(self, question, default='n'):
        return boolean_input(question, default)

    def get_or_none(self, data):
        return get_or_none(data)

    def make_float(self, flt):
        return make_float(flt)

    def make_int(self, itg):
        return make_int(itg)

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

    def handle(self, *args, **options):
        self.startLog(options.get('verbosity'))
        self.error = Error(self.logger)
        self.pbar = options.get('progressbar')
        self.do(options)
        self.logger.info('--- End ---')

    def do(self, options):
        self.logger.info('--- Doing ---')

