import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from django.contrib.auth.models import User

from slugify import smart_slugify
from casestudies import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args or (args and args[0] not in ('rollback','commit')):
            raise CommandError("USAGE: ./manage.py %s rollback|commit" % \
                    os.path.basename(__file__).split('.')[0])

        rollback = args[0] == 'rollback'
        transaction.enter_transaction_management()
        transaction.managed(True)
        
        for item in models.SectorTag.objects.filter(slug__isnull=True):
            item.slug = smart_slugify(item.sector, 
                                      manager=models.SectorTag.objects,
                                      lower_case=True)
            print "\tsector:", item.slug
            item.save()
            
        for item in models.TechnologyTag.objects.filter(slug__isnull=True):
            item.slug = smart_slugify(item.technology, 
                                      manager=models.TechnologyTag.objects,
                                      lower_case=True)
            print "\ttechnology:", item.slug
            item.save()
            
        for item in models.Client.objects.filter(slug__isnull=True):
            item.slug = smart_slugify(item.name, 
                                      manager=models.Client.objects,
                                      lower_case=True)
            print "\tclient:", item.slug
            item.save()
            
        for item in models.Page.objects.filter(slug__isnull=True):
            item.slug = smart_slugify(item.title,
                                      manager=models.Page.objects,
                                      lower_case=True)
            print "\tpage:", item.slug
            item.save()

        for item in models.CaseStudy.objects.filter(slug__isnull=True):
            item.slug = smart_slugify(item.title,
                                      manager=models.CaseStudy.objects,
                                      lower_case=True)
            print "\tcase_study:", item.slug
            item.save()
            
        for item in models.News.objects.filter(slug__isnull=True):
            item.slug = smart_slugify(item.title,
                                      manager=models.News.objects,
                                      lower_case=True)
            print "\tnews:", item.slug
            item.save()
            
        for item in models.Quote.objects.filter(slug__isnull=True):
            item.slug = smart_slugify(item.quote[:50],
                                      manager=models.Quote.objects,
                                      lower_case=True)
            print "\tquote:", item.slug
            item.save()
            
        if rollback:
            transaction.rollback()
        else:
            transaction.commit()
