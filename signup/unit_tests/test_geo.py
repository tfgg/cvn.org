from unittest import TestCase

from signup import geo

class TestNeighbors(TestCase):
    # Consituencies neighboring other consituencies

    # Editied down output from twfy getGeometry
    # http://www.theyworkforyou.com/api/docs/getGeometry
    data = {
        "Chipping Barnet" : {
            "name" : "Chipping Barnet",
            "centre_lat" : 51.6395895436,
            "centre_lon" : -0.192217329457,
            },
        
        "Hendon" : {
            "name" : "Hendon",
            "centre_lat" : 51.606570454,
            "centre_lon" : -0.252407672041,
            },
        "Altrincham & Sale West" : {
            "name" : "Altrincham & Sale West",
            "centre_lat" : 53.3989495951,
            "centre_lon" : -2.38207857643,
            },
        "Hertsmere" : {
            "name" : "Hertsmere",
            "centre_lat" : 51.6802918234,
            "centre_lon" : -0.274986273182,
            },

        "Stretford & Urmston" : {
            "name" : "Stretford & Urmston",
            "centre_lat" : 53.4450638328,
            "centre_lon" : -2.35374956251,
            },
        "Tatton" : {
            "name" : "Tatton",
            "centre_lat" : 53.2797662137,
            "centre_lon" : -2.38760476605,
            },
        }

    # when twfy doesn't know the data for a constituency, they return
    # records like this
    tricky_data = {
        u'Belfast East': {},
        u'Belfast North': {},
        u'Belfast South': {},
        u'Belfast West': {}
        }


    def test_center(self):
        self.assertEqual((53.3989495951, -2.38207857643),
                         geo.center(self.data, "Altrincham & Sale West"))

    def test_neigbors_south(self):
        # Hendon & Hertsmere are closer to Chipping Barnet then Tatton
        self.assertEqual(geo.neighbors("Chipping Barnet", limit=3, _data=self.data),
                         ["Hendon", "Hertsmere", "Tatton"])
                         
    def test_neigbors_north(self):
        # Tatton and Stretford are closer to Altrincham then Hertsmere
        self.assertEqual(geo.neighbors("Altrincham & Sale West", limit=3, _data=self.data),
                         ["Stretford & Urmston", "Tatton", "Hertsmere"])
        

    def test_tricky_data(self):
        # should not explode if the constituency does not have a full
        # set of data
        data = self.data.copy()
        data.update(self.tricky_data)
        self.assertEqual(geo.neighbors("Altrincham & Sale West", limit=3, _data=data),
                         ["Stretford & Urmston", "Tatton", "Hertsmere"])
