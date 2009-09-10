from django import forms

from signup.models import CustomUser
from signup.forms import TemplatedForm
from models import Invitation

import strings

class InviteForm(TemplatedForm):
    honeypot = forms.CharField(required=False)
    email = forms.EmailField(label="Their email address",
                             required=True)
    message = forms.CharField(label="A short message",
                              max_length=200,
                              widget=forms.Textarea,
                              required=False,
                              initial=strings.INVITE_TEXT)
    
    def clean_email(self):
        """
        Validate that the email is not already used by a registered 
        user and has not already been sent an invite.
        """
        user = CustomUser.objects.all()\
               .filter(email=self.cleaned_data['email'].lower())
        if user:
            raise forms.ValidationError(strings.INVITE_ERROR_REGISTERED)
        
        invite = Invitation.objects.all()\
                .filter(email=self.cleaned_data['email'].lower())
        if invite:
            raise forms.ValidationError(strings.INVITE_ERROR_INVITED)
        
        return self.cleaned_data['email'].lower()
        
    def clean_honeypot(self): # Honeypot to catch bots. Will this work?
        if self.cleaned_data['honeypot'] != "":
            raise forms.ValidationError(strings.INVITE_ERROR_HONEYPOT)
        else:
            return self.cleaned_data['honeypot']
        
    def save(self, user):
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        
        Invitation.objects.create_invitation(email=email, message=message, user=user)