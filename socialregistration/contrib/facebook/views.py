from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from socialregistration.contrib.facebook.client import Facebook
from socialregistration.contrib.facebook.models import FacebookProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class FacebookRedirect(OAuthRedirect):
    client = Facebook
    template_name = 'socialregistration/facebook/facebook.html'

class FacebookCallback(OAuthCallback):
    client = Facebook
    template_name = 'socialregistration/facebook/facebook.html'
    
    def get_redirect(self):
        return reverse('socialregistration:facebook:setup')

class FacebookSetup(SetupCallback):
    client = Facebook
    profile = FacebookProfile
    template_name = 'socialregistration/facebook/facebook.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'uid': client.get_user_info()['id']}

@login_required
def get_facebook_pages(request):
    profile = get_object_or_404(FacebookProfile, user=request.user)
    graph = facebook.GraphAPI(profile.access_token)
    pages = [p for p in graph.get_connections('me', 'accounts')["data"] if p["category"] != "Application"]
    if request.POST:
        form = SelectPageForm(request.POST, pages=pages)
        if form.is_valid():
            form.save(profile)
            messages.success(request, "Facebook page added successfully")
            return HttpResponseRedirect(reverse("index"))
    else:
        form = SelectPageForm(pages=pages)
    return render(request, 'socialregistration/facebook/pages.html', {"form":form})
    
    