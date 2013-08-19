#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class UserForm(forms.Form):
    """
    Default user creation form. Can be altered with the 
    `SOCIALREGISTRATION_SETUP_FORM` setting.
    """
    username = forms.RegexField(r'^[-\w]+$', max_length=29, min_length=5,
                                error_messages = {'invalid': _("username may contain only letters, numbers and dashes.")})
    email = forms.EmailField(
        help_text=_(u"Don't worry, we will never sell your info or abuse it.")
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError(_(u'This username is already in use.'))
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            email = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError(_(u'This email is already associated with another user.'))
#        
#    def clean(self):
#        if "password" in self.cleaned_data and "password2" in self.cleaned_data:
#            if self.cleaned_data['password'] != self.cleaned_data['password2']:
#                raise forms.ValidationError(_(u'Password does not match the confirm password'))
#        return self.cleaned_data
    
    def save(self, request, user, profile, client):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.set_unusable_password()
        user.save()
        profile.user = user
        profile.save()
        return user, profile
    