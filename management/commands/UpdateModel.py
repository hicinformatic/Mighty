from mighty.management import BaseCommand

class updateModel(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--force-display', action="store_true")

    def do(self, options):
        self.totalrows = self.model.objects.all().count()
        for obj in self.model.objects.all():
            self.row+=1
            if self.pbar:
                self.progressBar(self.row, self.totalrows)
            else:
                self.logger.info('Update object %s/%s "%s"' % (self.row, self.totalrows, obj.display))
            self.alerts = {}
            self.do_update(obj)

    def do_update(self, obj):
        pass