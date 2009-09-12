from unittest import TestCase

from signup import twfy
from signup.management.commands import constituencies
from settings import CONSTITUENCY_YEAR

import pickle

class TestManConstituency(TestCase):
    def setUp(self):
        """ Prime the fetch cache """
        params = {"date": CONSTITUENCY_YEAR.strftime("%Y")}
        url = twfy.svcurl("getConstituencies", params)
        data = pickle.load(open("signup/unit_tests/twfy.getConstituencies"))
        twfy.fetch.prime(url, data)
        
    def test_load(self):
        """ Test loading the constituencies """
        command = constituencies.Command()
        command.handle('load', silent=True)
        