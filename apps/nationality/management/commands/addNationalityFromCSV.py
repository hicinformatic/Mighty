from mighty.managements import AddModelFromCSV
from mighty.functions import test
from mighty.models.nationality import Nationality

class Command(AddModelFromCSV):
    help = "Add nationality from a CSV"
    fields_mandatory = ["Country", "Alpha2"]
    fields_optional = [ "Alpha3", "Numeric"]

    def do_line(self, line):
        print(line)
        country = {"country": line["Country"], "alpha2": line["Alpha2"]}
        if test(line["Alpha3"]):
            country["alpha3"] = line["Alpha3"]
        if test(line["Numeric"]):
            country["numeric"] = line["Numeric"]
        Nationality.objects.get_or_create(**country)