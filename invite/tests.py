from django.core import mail

from models import Invitation

from signup.unit_tests.testbase import TestCase
from signup.models import CustomUser

import strings

m8r_pre = "cvn-testing-"
m8r_addr = {'frank': m8r_pre+"frank@mailinator.com", 
            'barry': m8r_pre+"barry@mailinator.com", 
            'carl': m8r_pre+"carl@mailinator.com", }

USERS = [{'email': m8r_addr['frank'],
          'postcode': 'G206BT',
          'can_cc': True,
          'first_name': 'Frank',
          'last_name': 'Fandango',
          'username': 'Frank',
          'password': ''},
         ]

class TestInvite(TestCase):
    def setUp(self):
        self.users = []
        
        for u in USERS:    
            user = CustomUser.objects.create(**u)
            user.save()
            self.users.append(user)
        
        self.assertTrue(self.client.login(username="Frank",password=""))
    
    def test_send_registered_invite(self):
        """ Send an invite to an already registered user """
        invite_form = {'honeypot': '', 'email': m8r_addr['frank'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True) # Send the invite        
        self.assertTrue(strings.INVITE_ERROR_REGISTERED % m8r_addr['frank'] in response.content)
    
    def test_send_invite(self):
        """ Send a valid invite to an email address, then send an invite again to the same email address """
        invite_form = {'honeypot': '', 'email': m8r_addr['barry'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_NOTICE_SUCCESS in response.content)
        self.assertEquals(len(mail.outbox),1)
        self.assertEquals(mail.outbox[0].subject, strings.INVITE_SUBJECT % m8r_addr['frank'])
        self.assertEquals(Invitation.objects.filter(email=m8r_addr['barry']).count(), 1)
        
        invite_form = {'honeypot': '', 'email': m8r_addr['barry'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_ERROR_INVITED % m8r_addr['barry'] in response.content)
        
    def test_send_invite_multi(self):
        """ Send a multi-address email """
        invite_form = {'honeypot': '', 'email': 'Barry <%s>, Carl <%s>' % (m8r_addr['barry'], m8r_addr['carl']), 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_NOTICE_SUCCESS in response.content)
        self.assertEquals(len(mail.outbox),2)
        self.assertEquals(mail.outbox[0].subject, strings.INVITE_SUBJECT % m8r_addr['frank'])
        self.assertEquals(Invitation.objects.all().count(), 2)
        self.assertEquals(Invitation.objects.filter(email=m8r_addr['barry']).count(), 1)
        self.assertEquals(Invitation.objects.filter(email=m8r_addr['carl']).count(), 1)
    
    def test_honeypot(self):
        """ Test the bot honeypot on the invitation form """
        invite_form = {'honeypot': 'BLAH BLAH IM A BOT', 'email': m8r_addr['barry'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_ERROR_HONEYPOT in response.content)
        