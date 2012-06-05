from classytags.core import Tag, Options
from classytags.arguments import Argument, KeywordArgument
from classytags.helpers import InclusionTag
from django import template
from profile.models import Profile, LEVELS

register = template.Library()

class FoursquareTag(Tag):
    name = "foursquare_button"
    
    options = Options(Argument('template_id', required=False, resolve=False))
    
    def render_tag(self, context, template_id=None):
        if template_id:
             self.template = 'socialregistration/foursquare/foursquare_button_%s.html' % template_id
        else:
            self.template = 'socialregistration/foursquare/foursquare_button.html'
        return template.loader.render_to_string(self.template, context)
    
register.tag(FoursquareTag)