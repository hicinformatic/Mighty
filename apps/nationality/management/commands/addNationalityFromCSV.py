from django.core.files import File

from mighty.managements import AddModelFromCSV
from mighty.functions import test, image_directory_path
from mighty.models.nationality import Nationality
from mighty.apps.nationality.apps import NationalityConfig

import os.path

class Command(AddModelFromCSV):
    help = "Add nationality from a CSV"
    fields_mandatory = ["Country", "Alpha2"]
    fields_optional = [ "Alpha3", "Numeric"]

    def do_line(self, line):
        src = '%s/flags' % NationalityConfig.directory
        country = {"country": line["Country"], "alpha2": line["Alpha2"]}
        if test(line["Alpha3"]):
            country["alpha3"] = line["Alpha3"]
        if test(line["Numeric"]):
            country["numeric"] = line["Numeric"]

        nat = Nationality.objects.get_or_create(**country)[0]

        flagalpha2 = '%s/%s.png' % (src, line["Alpha2"].lower())
        if os.path.isfile(flagalpha2):
            f = open(flagalpha2, "rb")
            flag = File(f)
            nat.image.save(flagalpha2, flag, save=True)