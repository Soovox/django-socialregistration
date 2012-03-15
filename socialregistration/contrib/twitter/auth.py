#-*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from socialregistration.contrib.twitter.models import TwitterProfile


class TwitterAuth(ModelBackend):
    
    def authenticate(self, twitter_id=None):
        try:
            return TwitterProfile.objects.get(
                twitter_id=twitter_id
            ).user
        except TwitterProfile.DoesNotExist:
            return None
