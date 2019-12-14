from django.core.files import File
from mighty.management.commands.CreateOrUpdateModelFromCSV import Command

import os.path

class Command(Command):
    testconfig = ["none",]
    fields_retrieve = ['country','alpha2','alpha3']
    fields_associates = {
        'country': 'Country',
        'alpha2': 'Alpha2',
        'alpha3': 'Alpha3',
        'numeric': 'Numeric',
    }

#    def do_line(self, line):
#        src = '%s/flags' % NationalityConfig.directory
#        country = {"country": line["Country"], "alpha2": line["Alpha2"]}
#        if test(line["Alpha3"]):
#            country["alpha3"] = line["Alpha3"]
#        if test(line["Numeric"]):
#            country["numeric"] = line["Numeric"]
#
#        nat = Nationality.objects.get_or_create(**country)[0]
#
#        flagalpha2 = '%s/%s.png' % (src, line["Alpha2"].lower())
#        if os.path.isfile(flagalpha2):
#            f = open(flagalpha2, "rb")
#            flag = File(f)
#            nat.image.save(flagalpha2, flag, save=True)