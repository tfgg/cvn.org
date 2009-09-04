# python
import datetime
import random
import re
import sha

# django
from django.db import models
from django.db.models import Model as DjangoModel
from django.db.models import permalink
from django.contrib.auth.models import User, UserManager
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail

# app
from slugify import smart_slugify
from settings import CONSTITUENCY_YEAR

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class Model(DjangoModel):
    class Meta:
        abstract = True
    """same as django model but allows you to be lazy about the slug"""
    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug') and 'slug' in self._meta.get_all_field_names():
            if kwargs.get('title'):
                kwargs['slug'] = smart_slugify(kwargs['title'], lower_case=True)
            elif kwargs.get('name'):
                kwargs['slug'] = smart_slugify(kwargs['name'], lower_case=True)
            elif kwargs:
                import warnings
                warnings.warn("Unable to automagically set slug (%s)" % \
                              self._meta.get_all_field_names())
        super(Model, self).__init__(*args, **kwargs)

class Constituency(Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    year = models.DateField()
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.year)
    
    @permalink
    def get_absolute_url(self):
        return ("constituency", (self.slug,))

    class Meta:
        verbose_name_plural = "Constituencies"

    
class CustomUser(User):
    postcode = models.CharField(max_length=9)
    constituencies = models.ManyToManyField(Constituency)
    can_cc = models.BooleanField(default=False)
    objects = UserManager()

    @property
    def current_constituencies(self):
        "Return constituencies matching current year"
        return self.constituencies.filter(year=CONSTITUENCY_YEAR)

    @property
    def display_name(self):
        if self.first_name:
            name = self.first_name
        else:
            name = self.email
        return name
    
    def __unicode__(self):
        return self.email
    
    @permalink
    def get_absolute_url(self):
        return ("user", (self.id,))



class RegistrationManager(models.Manager):
    """
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    
    """
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        profile = self.get_user(activation_key,
                                only_activated=False)
        if profile and not profile.activated and \
               not profile.activation_key_expired():
            user = profile.user
            user.is_active = True
            user.save()
            profile.activated = True
            profile.save()
            return profile
        else:
            return False

    def get_user(self, activation_key, only_activated=True):
        profile = None
        if SHA1_RE.search(activation_key):
            profile = RegistrationProfile.objects.all()\
                      .filter(activation_key=activation_key)
            if only_activated:
                profile = profile.filter(activated=True)
            if profile:
                profile = profile[0]
        return profile
        
    def create_profile(self,
                       user):
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+user.username).hexdigest()
        profile = RegistrationProfile(user=user,
                                      activation_key=activation_key)
        profile.save()

        user.is_active = False
        user.save()
        current_site = Site.objects.get_current()
        subject = "Please confirm your registration"
        email_context = {'activation_key': profile.activation_key,
                         'site': current_site,
                         'user': user}
        message = render_to_string('activation_email.txt',
                                   email_context)
        
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email,])
        return profile
    
        
    def delete_expired_users(self):
        for profile in RegistrationProfile.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()
                    profile.delete()


class RegistrationProfile(Model):
    """
    A simple profile which stores an activation key for use in passwordless
    site interaction

    """
    user = models.ForeignKey(CustomUser,
                             verbose_name='user')
    email = models.CharField(max_length=80)
    activation_key = models.CharField(max_length=50)
    objects = RegistrationManager()
    activated = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'registration profile'
        verbose_name_plural = 'registration profiles'
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user
    
    def activation_key_expired(self):
        expiration_date = datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS)
        return not self.activated and \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True
