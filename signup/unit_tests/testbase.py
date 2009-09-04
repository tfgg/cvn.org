# django
from django.test import TestCase as DjangoTestCase
from django.conf import settings

# app

class TestCase(DjangoTestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        
        


    
