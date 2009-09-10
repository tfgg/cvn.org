from django.core import mail

from models import Invitation

from signup.unit_tests.testbase import TestCase
from signup.models import CustomUser

import strings

M8R_PRE = "cvn-testing-"
M8R_ADDR = {'frank': M8R_PRE+"frank@mailinator.com", 
            'barry': M8R_PRE+"barry@mailinator.com", 
            'carl': M8R_PRE+"carl@mailinator.com", }

USERS = [{'email': M8R_ADDR['frank'],
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
        invite_form = {'honeypot': '', 'email': M8R_ADDR['frank'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True) # Send the invite        
        self.assertTrue(strings.INVITE_ERROR_REGISTERED % M8R_ADDR['frank'] in response.content)
    
    def test_send_invite(self):
        """ Send a valid invite to an email address, then send an invite again to the same email address """
        invite_form = {'honeypot': '', 'email': M8R_ADDR['barry'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_NOTICE_SUCCESS in response.content)
        self.assertEquals(len(mail.outbox),1)
        self.assertEquals(mail.outbox[0].subject, strings.INVITE_SUBJECT % M8R_ADDR['frank'])
        self.assertEquals(Invitation.objects.filter(email=M8R_ADDR['barry']).count(), 1)
        
        invite_form = {'honeypot': '', 'email': M8R_ADDR['barry'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_ERROR_INVITED % M8R_ADDR['barry'] in response.content)
        
    def test_send_invite_multi(self):
        """ Send a multi-address email """
        invite_form = {'honeypot': '', 'email': 'Barry <%s>, Carl <%s>' % (M8R_ADDR['barry'], M8R_ADDR['carl']), 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_NOTICE_SUCCESS in response.content)
        self.assertEquals(len(mail.outbox),2)
        self.assertEquals(mail.outbox[0].subject, strings.INVITE_SUBJECT % M8R_ADDR['frank'])
        self.assertEquals(Invitation.objects.all().count(), 2)
        self.assertEquals(Invitation.objects.filter(email=M8R_ADDR['barry']).count(), 1)
        self.assertEquals(Invitation.objects.filter(email=M8R_ADDR['carl']).count(), 1)
    
    def test_honeypot(self):
        """ Test the bot honeypot on the invitation form """
        invite_form = {'honeypot': 'BLAH BLAH IM A BOT', 'email': M8R_ADDR['barry'], 'message': 'flump'}
        response = self.client.post("/invite/", invite_form, follow=True)
        self.assertTrue(strings.INVITE_ERROR_HONEYPOT in response.content)
        