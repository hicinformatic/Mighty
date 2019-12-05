from django.core.management.base import CommandError
from django.utils.text import get_valid_filename

from mighty.management import BaseCommand
from mighty.models.abstracts import IMAGE_DEFAULT

import os, shutil

class Command(BaseCommand):
    excludes = [IMAGE_DEFAULT, ]

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--directory', required=True)
        parser.add_argument('--mode', default="export")


    def do(self, options):
        self.directory = options.get("directory")
        self.mode = options.get("mode")

        if self.mode == "export" and not os.path.isdir(self.directory):
            os.mkdir(self.directory)
            self.logger.info('Directory created: %s' % self.directory)
        elif self.mode == "import" and os.path.isdir(self.directory):
            self.logger.info('Directory found: %s' % self.directory)
        else:
            raise CommandError('Please check mode (%s) or directory (%s)' % (self.mode, self.directory))

        self.totalrows = self.model.objects.all().count()
        for obj in self.model.objects.all():
            self.current_row+=1
            if self.pbar:
                self.progressBar(self.current_row, self.totalrows)
            else:
                self.logger.info('Update object %s/%s "%s"' % (self.current_row, self.totalrows, obj.display))

            if self.mode == "export" and obj.valid_imagename not in self.excludes:
                self.export_image(obj)
            else:
                self.import_image(obj)

    def import_image(self, obj):
        pass

    def export_image(self, obj):
        original = os.getcwd() + obj.image_url
        copy = os.getcwd() + "/%s/%s%s" % (self.directory, get_valid_filename(obj), obj.image_extension)
        os.system('cp %s %s' % (original, copy))