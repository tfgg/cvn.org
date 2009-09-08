# python
import datetime
import cgi

# django
from django.conf import settings

# app
from testbase import TestCase

from signup.models import Constituency, CustomUser
from signup.models import RegistrationManager, RegistrationProfile

users = [{'email':'f@mailinator.com',
          'postcode':'G206BT',
          'can_cc':True,
          'first_name':'f',
          'last_name':'f',
          'username':'f@mailinator.com'},
         {'email':'g@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':True,
          'first_name':'g',
          'last_name':'g',
          'username':'g@mailinator.com'},
         {'email':'h@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':False,
          'first_name':'hoogly',
          'last_name':'h',
          'username':'h@mailinator.com'},
         ]

this_year = settings.CONSTITUENCY_YEAR
last_year = settings.CONSTITUENCY_YEAR - datetime.timedelta(365)
constituencies = [("Glasgow North", this_year),
                  ("Holborn & St Pancras", this_year),
                  ("Holborn & St Pancras", last_year)
                  ]
        
class ViewsTestCase(TestCase):
    
    def setUp(self):
        self.users = []
        self.constituencies = []
        for const, yr in constituencies:
            const = Constituency.objects.create(name=const,
                                                year=yr)
            const.save()
            self.constituencies.append(const)

    def test_viewing_different_models(self):
        "create a bunch of instance of models and view them"
        year = settings.CONSTITUENCY_YEAR
        def page_content(whole_content):
            # rough way of getting the HTML inside the div tag #page-content
            content = whole_content.split('id="main"')[1]
            return content
        
        def page_title(whole_content):
            return whole_content.split('<title>')[1].split('</title>')[0]
        
        response = self.client.get(self.constituencies[0].get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cgi.escape(self.constituencies[0].name)\
                        in page_title(response.content))
        self.assertTrue(u"There are 0" in page_content(response.content))

        # add the first user
        response = self.client.post("/", users[0])
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/")
        self.assertTrue(users[0]['first_name'] in page_content(response.content))
        self.assertTrue("1 volunteers in 1 constituencies (out of a total 2)"\
                        in page_content(response.content))
        

        response = self.client.get("/add_constituency/")
        self.assertTrue(u"Join" in page_title(response.content))
        self.assertTrue(cgi.escape(self.constituencies[0].name) in page_content(response.content))
        
        response = self.client.get(self.constituencies[0].get_absolute_url())
        self.assertTrue(u"the only vol" in page_content(response.content))
        
        # add the second user
        response = self.client.post("/", users[1])
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/")
        self.assertTrue(users[1]['first_name'] in page_content(response.content))
        self.assertTrue("2 volunteers in 2 constituencies (out of a total 2)"\
                        in page_content(response.content))
        

        response = self.client.get("/add_constituency/")
        self.assertTrue(u"Join" in page_title(response.content))
        self.assertTrue(cgi.escape(self.constituencies[1].name) in page_content(response.content))
        
        response = self.client.get(self.constituencies[1].get_absolute_url())
        self.assertTrue(u"the only vol" in page_content(response.content))
        
        # and the third user
        response = self.client.post("/", users[2])
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/")
        self.assertTrue(users[2]['first_name'] in page_content(response.content))
        self.assertTrue("3 volunteers in 2 constituencies (out of a total 2)"\
                        in page_content(response.content))
        
        response = self.client.get("/add_constituency/")
        self.assertTrue(u"Join" in page_title(response.content))
        self.assertTrue(cgi.escape(self.constituencies[2].name) in page_content(response.content))
        
        response = self.client.get(self.constituencies[2].get_absolute_url())
        self.assertTrue(u"2 vol" in page_content(response.content))
        

class TestAddConstituencies(TestCase):
    def setUp(self):
        crewe = Constituency.objects.create(
            name="Crewe & Nantwich",
            year = this_year)
        user = CustomUser.objects.create(
            username = "Frank",
            password = "",
            postcode = "CW1 6AR",
            can_cc = True)
        user.constituencies = [crewe]
        self.assert_(self.client.login(username="Frank", password=""))

    def test_postcode_search(self):
        # user can enter a postcode into the search box to find a
        # constituency.
        # Example: a user in Crewe may search for a postcode in Hendon
        newcastle = Constituency.objects.create(
            name = "Hendon",
            year = this_year)
        self.assert_(self.client.login(username="Frank", password=""))

        # NW4 is in Hendon
        response = self.client.get("/add_constituency/#search", {"q":"NW4 3AS"})
        self.assertContains(response, "Hendon")

    def test_postcode_garbage(self):
        # user could put garbage in the search box. this should not explode
        response = self.client.get("/add_constituency/#search", {"q": u"\u2603"})
        # user is still registered in Crewe
        self.assertContains(response, "Crewe")
        # there is an error message
        self.assertContains(response, "could not find")
        
    def test_invalid_postcode(self):
        # there are postcodes with valid formats that are not valid,
        # eg there are no postcodes that begin with D
        response = self.client.get("/add_constituency/#search", {"q": u"D7 4XP"})
        # user is still registered in Crewe
        self.assertContains(response, "Crewe")
        # there is an error message
        self.assertContains(response, "seems to be invalid")
        
