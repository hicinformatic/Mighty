from mighty.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--forcedisplay', action="store_true")

    def do(self, options):
        self.total_rows = self.model.objects.all().count()
        self.logger.info('Total rows: %s' % self.total_rows)
        self.force_display = options.get('forcedisplay')
        for obj in self.model.objects.all():
            if self.pbar: self.progressBar(self.current_row, self.totalrows)
            else: self.logger.info('Update object %s/%s "%s"' % (self.current_row, self.total_rows, str(obj)))
            self.do_object(obj)
            self.current_row += 1

    def do_object(self, obj):
        obj.display = None
        obj.save()