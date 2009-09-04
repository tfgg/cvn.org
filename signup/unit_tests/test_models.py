# python
import datetime

# django
from django.conf import settings

# app
from testbase import TestCase

from signup.models import Constituency, CustomUser
from signup.models import RegistrationManager, RegistrationProfile

this_year = settings.CONSTITUENCY_YEAR
last_year = settings.CONSTITUENCY_YEAR - datetime.timedelta(365)

CONSTITUENCIES = [{'name':'My place',
                   'year': this_year},
                  {'name':'My other place',
                   'year': this_year},
                  {'name':'My place last year',
                   'year': last_year},]

USERS = [{'email':'f@mailinator.com',
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
         ]
        

class ModelsTestCase(TestCase):

    def setUp(self):
        # create a sector
        self.constituencies = []
        self.users = []
        for c in CONSTITUENCIES:    
            const = Constituency.objects.create(**c)
            const.save()
            self.constituencies.append(const)

        for u in USERS:    
            user = CustomUser.objects.create(**u)
            user.save()
            self.users.append(user)        
    
    def test_basic_instance_creation(self):
        """test to make sure the various models can be created"""
        first = self.constituencies[0]
        self.assertEqual(first.slug, 'my-place')
        self.assertEqual(first.get_absolute_url(),
                         u"/constituency/%s/" % first.slug)
        count = 0
        for user in self.users:
            self.assertEqual(user.postcode, USERS[count]['postcode'])
            count += 1
            
    def test_different_dates(self):
        self.users[0].constituencies.add(self.constituencies[0])
        self.users[0].constituencies.add(self.constituencies[2])
        self.assertEqual(self.users[0].current_constituencies.count(), 1)
        
