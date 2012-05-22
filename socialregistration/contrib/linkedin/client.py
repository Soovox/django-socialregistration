from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from socialregistration.clients.oauth import OAuth
from socialregistration.settings import SESSION_KEY
import json
import urlparse

class LinkedIn(OAuth):
    api_key = getattr(settings, 'LINKEDIN_CONSUMER_KEY', '')
    secret_key = getattr(settings, 'LINKEDIN_CONSUMER_SECRET_KEY', '')
    
    request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken'
    access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
    auth_url = 'https://www.linkedin.com/uas/oauth/authenticate'
    
    _user_info = None
    
    def get_callback_url(self, subdomain=""):
        if self.is_https():
            return urlparse.urljoin(
                getattr(settings, 'HTTPS_SITE_URL').replace("%s.", subdomain + "." if subdomain else ""),
                reverse('socialregistration:linkedin:callback'))
        return urlparse.urljoin(
            getattr(settings, 'SITE_URL').replace("%s.", subdomain + "." if subdomain else ""),
            reverse('socialregistration:linkedin:callback'))
    
    def get_user_info(self):
        if self._user_info is None:
            self._user_info = json.loads(
                self.request("http://api.linkedin.com/v1/people/~:(id)?format=json"))
            
        return self._user_info

    @staticmethod
    def get_session_key():
        return '%slinkedin' % SESSION_KEY
