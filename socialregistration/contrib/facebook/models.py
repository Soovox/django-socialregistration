from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from socialregistration.signals import connect, login

class FacebookProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    uid = models.CharField(max_length=255, blank=False, null=False)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.uid)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(uid=self.uid)
    
#class FacebookPage(models.Model):
#    facebook_profile = models.ForeignKey(FacebookProfile)
#    uid = models.CharField(max_length=255)
#    name = models.CharField(max_length=255)
#    access_token = models.CharField(max_length=255, null=True, blank=True)
#    

def save_facebook_token(sender, user, profile, client, **kwargs):    
    profile.access_token = client.graph.access_token
    profile.save()
    
connect.connect(save_facebook_token, sender=FacebookProfile,
    dispatch_uid='socialregistration.facebook.connect')
login.connect(save_facebook_token, sender = FacebookProfile,
    dispatch_uid = 'socialregistration.facebook.login')