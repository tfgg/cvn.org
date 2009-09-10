from django.db import models
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from signup.models import CustomUser
import strings

"""
  Shortcuts for invitation creation and automated sending of the emails
"""
class InvitationManager(models.Manager):
    def create_invitation(self, email, message, user):
      invite = Invitation(email=email, user_from=user)
      invite.save()
      
      current_site = Site.objects.get_current()
      
      subject = strings.INVITE_SUBJECT % user
      email_context = { 'message': message,
                        'site': current_site, 
                        'user': user }
      text = render_to_string('invite/invitation_email.txt',
                                 email_context)
      
      send_mail(subject,
                text,
                settings.DEFAULT_FROM_EMAIL,
                [email,])

class Invitation(models.Model):
    email = models.CharField(max_length=80)
    user_from = models.ForeignKey(CustomUser)
    objects = InvitationManager()
    
    def __unicode__(self):
        return u"Invitation sent to %s from %s" % (self.email, self.user_from)
    
    class Meta:
        verbose_name = 'invitation'
        verbose_name_plural = 'invitations'
