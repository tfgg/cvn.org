import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction

from slugify import smart_slugify
from signup import models, twfy
from settings import CONSTITUENCY_YEAR

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args or (args and args[0] not in ('load')):
            raise CommandError("USAGE: ./manage.py %s load" % \
                    os.path.basename(__file__).split('.')[0])

        transaction.enter_transaction_management()
        transaction.managed(True)

        year = CONSTITUENCY_YEAR.strftime("%Y")
        constituencies = twfy.getConstituencies()

        for c in constituencies:
            item = models.Constituency(name=c,
                                       year=CONSTITUENCY_YEAR)
            item.slug = smart_slugify(item.name, 
                                      manager=models.Constituency.objects,
                                      lower_case=True)
            print "Loading %s <%s>" % (item.name, item.slug)
            item.save()            
        transaction.commit()
