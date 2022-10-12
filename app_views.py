import requests

from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.plugins import logger

from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms

class SettingsForm(forms.Form):
    username = forms.CharField(label='Username', required=False, max_length=1024, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', required=False, max_length=1024, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    #registry_url = forms.CharField(label='Registry URL', required=False, max_length=1024, widget=forms.TextInput(attrs={'placeholder': 'Registry Url'}))

def HomeView(plugin):
    @login_required
    def home(request):
        ds = plugin.get_user_data_store(request.user)

        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                #ds.set_string('registry_url', form.cleaned_data['registry_url'])
                ds.set_string('username', form.cleaned_data['username'])
                ds.set_string('password', form.cleaned_data['password'])
                ds.set_string('token', None)
                messages.success(request, 'Settings updated.')

        form = SettingsForm(initial={'username': ds.get_string('username', default=""), 
                                     'password': ds.get_string('password', default=""), 
                                     })
                                     #'registry_url': ds.get_string('registry_url', default="") or DEFAULT_HUB_URL})

        return render(request, plugin.template_path("app.html"), {
            'title': 'ASDC',
            'form': form
        })

    return home


def LoadButtonsView(plugin):
    def view(request):

        return render(
            request,
            plugin.template_path("load_buttons.js"),
            {
                "api_url": "/api" + plugin.public_url("").rstrip("/"),
            },
            content_type="text/javascript",
        )

    return view
