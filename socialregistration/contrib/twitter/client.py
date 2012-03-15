#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth
from socialregistration.settings import SESSION_KEY
import urlparse

class Twitter(OAuth):
    api_key = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
    secret_key = getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', '')
    
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    auth_url = 'https://api.twitter.com/oauth/authenticate'
    
    def get_callback_url(self):
        if self.is_https():
            return urlparse.urljoin(
                getattr(settings, 'HTTPS_SITE_URL', 'https://'),
                reverse('socialregistration:twitter:callback'))
        return urlparse.urljoin(
            getattr(settings, 'SITE_URL', 'http://'),
            reverse('socialregistration:twitter:callback'))
    
    def get_user_info(self):
        return self._access_token_dict

    @staticmethod
    def get_session_key():
        return '%stwitter' % SESSION_KEY

