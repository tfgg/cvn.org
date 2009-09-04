import datetime
import re

from django import forms
from django.template import Context, loader

from models import CustomUser, Constituency, RegistrationProfile
from settings import CONSTITUENCY_YEAR
import twfy

POSTCODE_RE = re.compile(r'\b[A-PR-UWYZ][A-HK-Y0-9][A-HJKSTUW0-9]?[ABEHMNPRVWXY0-9]? {0,2}[0-9][ABD-HJLN-UW-Z]{2}\b',re.I)

class TemplatedForm(forms.Form):
    def output_via_template(self):
        "Helper function for fieldsting fields data from form."
        bound_fields = [forms.forms.BoundField(self, field, name) for name, field \
                        in self.fields.items()]
        c = Context(dict(form = self, bound_fields = bound_fields))
        t = loader.get_template('forms/form.html')
        return t.render(c)

    def as_table(self):
        return self.output_via_template()

class UserForm(TemplatedForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    postcode = forms.CharField(label="Your postcode",
                               required=True)
    can_cc = forms.BooleanField(label="Share your email address?",
                                help_text=("If you agree, we'll share your "
                                           "email address with others in "
                                           "your constituency, to make "
                                           "collaboration smooth"),
                                required=False)

    def clean_email(self):
        """
        Validate that the email is not already in use.
        
        """
        user = CustomUser.objects.all()\
               .filter(email=self.cleaned_data['email'].lower())
        if user:
            raise forms.ValidationError('This email is already registered')
        return self.cleaned_data['email'].lower()

    def clean_postcode(self):
        code = self.cleaned_data['postcode']
        if not POSTCODE_RE.match(code):
            raise forms.ValidationError("Please enter a valid postcode")
        return code
        
    def save(self, domain_override=""):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User`` (by calling
        ``RegistrationProfile.objects.create_inactive_user()``).
        
        """
        email = self.cleaned_data['email']
        postcode = self.cleaned_data['postcode']
        can_cc = self.cleaned_data['can_cc']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        user = CustomUser.objects.create(username=email,
                                         email=email,
                                         postcode=postcode,
                                         can_cc=can_cc,
                                         first_name=first_name,
                                         last_name=last_name,
                                         is_active=False)
        constituency = Constituency.objects.all()\
                       .filter(name=twfy.getConstituency(postcode))\
                       .filter(year=CONSTITUENCY_YEAR)[0]
        user.constituencies.add(constituency)
        user.save()
        profile = RegistrationProfile.objects.create_profile(user)
        return profile
