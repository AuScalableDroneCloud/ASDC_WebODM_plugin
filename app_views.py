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
    pipelines_url = forms.CharField(label='Custom pipelines repo URL(s) (comma-separated)', required=False, max_length=1024, widget=forms.TextInput(attrs={'placeholder': 'Pipelines Url'}))

def HomeView(plugin):
    @login_required
    def home(request):
        ds = plugin.get_user_data_store(request.user)

        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                ds.set_string('pipelines_url', form.cleaned_data['pipelines_url'])
                messages.success(request, 'Settings updated.')

        form = SettingsForm(initial={'pipelines_url': ds.get_string('pipelines_url', default="")})

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
