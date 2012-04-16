#-*- coding: utf-8 -*-
import requests
import urlparse
import simplejson
from django.conf import settings
from django.core.urlresolvers import reverse
from oauth_hook import OAuthHook
from socialregistration.clients.oauth import OAuth
from socialregistration.settings import SESSION_KEY


class Twitter(OAuth):
    api_key = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
    secret_key = getattr(settings, 'TWITTER_CONSUMER_SECRET_KEY', '')
    
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    auth_url = 'https://api.twitter.com/oauth/authenticate'
    
    _user_info = None
    
    def get_callback_url(self, subdomain=""):
        if self.is_https():
            return urlparse.urljoin(
                getattr(settings, 'HTTPS_SITE_URL').replace("%s.", subdomain + "." if subdomain else ""),
                reverse('socialregistration:twitter:callback'))
        return urlparse.urljoin(
            getattr(settings, 'SITE_URL').replace("%s.", subdomain + "." if subdomain else ""),
            reverse('socialregistration:twitter:callback'))
    
    def get_user_info(self):
        if self._user_info is None:
            oauth_hook = OAuthHook(self._access_token_dict["oauth_token"], self._access_token_dict["oauth_token_secret"], 
                                   settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET_KEY, True)
            client = requests.session(hooks={'pre_request': oauth_hook})
            response = client.get('https://api.twitter.com/1/users/show.json?user_id=%s&include_entities=false' % self._access_token_dict["user_id"])
            self._user_info = simplejson.loads(response.content)
        return self._user_info

    @staticmethod
    def get_session_key():
        return '%stwitter' % SESSION_KEY

