from unittest import TestCase

from signup import twfy

class TestTwfyErrors(TestCase):
    def test_getConstituencies_invalid_arg(self):
        # getConstituencies takes date, latitude, longetude, distance
        self.assertRaises(ValueError, twfy.getConstituencies, lat=52)
        
    def test_getConstituencies_geo_arg(self):
        # getConstituencies takes lat, lng, dist but if you provide
        # one you must proved all of them
        self.assertRaises(ValueError, twfy.getConstituencies, latitude=52)
