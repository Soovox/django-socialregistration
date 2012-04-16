#-*- coding: utf-8 -*-
from django import forms
from operator import itemgetter
from models import FacebookPage

class SelectPageForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.pages = kwargs.pop("pages")
        super(PageForm, self).__init(*args, **kwargs)
        self.fields["pages"] = forms.ChoiceField(choices=[(page["id"], page["name"]) for page in self.pages])
    
    def save(self, profile):
        selected_page = forms.cleaned_data["pages"]
        index_selected_page = map(itemgetter('self.pages'), self.pages).index(selected_page) 
        page = self.pages[index_selected_page]
        facebook_page, created = FacebookPage.objects.get_or_create(
                            facebook_profile=profile,
                            uid=page["id"],
                            name=page["name"],
                            defaults={"access_token": 
                                    page["access_token"]
                                }               
                            )
        return facebook_page
