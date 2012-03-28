#-*- coding: utf-8 -*-
import urlparse
from django.conf import settings
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth2
from socialregistration.settings import SESSION_KEY
import json
import facebook

class Facebook(OAuth2):
    client_id = getattr(settings, 'FACEBOOK_APP_ID', '')
    secret = getattr(settings, 'FACEBOOK_SECRET_KEY', '')
    scope = getattr(settings, 'FACEBOOK_REQUEST_PERMISSIONS', '')
    
    auth_url = 'https://www.facebook.com/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    
    graph = None
    _user_info = None
    
    
    def get_callback_url(self, subdomain=""):
        if self.is_https():
            return urlparse.urljoin(
                getattr(settings, 'HTTPS_SITE_URL').replace("%s.", subdomain + "." if subdomain else ""),
                reverse('socialregistration:facebook:callback'))
        return urlparse.urljoin(
            getattr(settings, 'SITE_URL').replace("%s.", subdomain + "." if subdomain else ""),
            reverse('socialregistration:facebook:callback'))
        
    def get_user_info(self):
        if self._user_info is None:
            self.graph = facebook.GraphAPI(self._access_token)
            self._user_info = self.graph.request('me', args={"fields": "bio,last_name,first_name,gender,birthday,location,website,picture", "type": "large"})
        return self._user_info
    
    @staticmethod
    def get_session_key():
        return '%sfacebook' % SESSION_KEY
