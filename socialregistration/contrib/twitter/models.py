#-*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from socialregistration.signals import connect

class TwitterProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    twitter_id = models.PositiveIntegerField()
    access_token = models.CharField(max_length=80, null=True, blank=True)
    access_token_secret = models.CharField(max_length=80, null=True, blank=True)
    
    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.twitter_id)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(twitter_id=self.twitter_id)
    
def save_twitter_token(sender, user, profile, client, **kwargs):
    profile.access_token = client.get_access_token().key
    profile.access_token_secret = client.get_access_token().secret
    profile.save()
    
connect.connect(save_twitter_token, sender=TwitterProfile,
    dispatch_uid='socialregistration_twitter_token')
