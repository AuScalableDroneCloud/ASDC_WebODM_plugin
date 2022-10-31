from rest_framework import status
from rest_framework.response import Response

from app.plugins import PluginBase, Menu, MountPoint, get_current_plugin
from app.plugins.views import TaskView
from app.plugins import logger
from django.shortcuts import render, redirect
from django import forms
from django.views.generic.base import RedirectView

from .app_views import HomeView, LoadButtonsView
from .api_views import GetUserProjects, GetUserProjectsAndTasks, GetProjectTasks, GetUserPipelines
from .api_views import SaveProjects, ClearProjects

import os
host = os.environ.get('WO_HOST')
port = os.environ.get('WO_PORT')
from .pipelines import get_json
import requests

class Plugin(PluginBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pipelines = {}
        self.saved_projects = []

    def serve_public_assets(self, request):
        """
        Should be overriden by plugins that want to control which users
        have access to the public assets. By default anyone can access them,
        including anonymous users.
        :param request: HTTP request
        :return: boolean (whether the plugin's public assets should be exposed for this request)
        """
        #Using this as a horrible hack to get the pipeline list,
        #since we get the request here, can lookup the user
        self.pipelines = get_json(request.user)
        return True

    def main_menu(self):
        #Super hacky way to force a request and populate pipelines in function above
        proto = "http://" if "localhost" in host else "https://"
        ports = "" if port == "80" else ":" + port
        try:
            requests.get(proto + host + ports + "/plugins/asdc/style.css")
        except:
            pass

        #Default pipelines
        if not self.pipelines:
            self.pipelines = [
                {"tag": "default", "name": "Default", "icon": "fas fa-industry"},
                {"tag": "base", "name": "Base", "icon": "fas fa-project-diagram"},
                {"tag": "exp", "name": "Experimental", "icon": "fas fa-stream"},
            ]

        submenu = []
        for p in self.pipelines:
            tag = p["tag"]
            #submenu += [Menu(p["name"], f"https://jupyter.{host}/hub/spawn?profile={tag}", p["icon"])]
            submenu += [Menu(p["name"], f"javascript:open_jhub('{host}', '{tag}');", p["icon"])]

        prjmenu = [Menu("Add To Saved", f"javascript:save_open_projects();", "fas fa-project-diagram"),
                   Menu("Clear Saved", f"javascript:clear_open_projects();", "fas fa-trash-alt")]
        for p in self.saved_projects:
            prjmenu += [Menu("PRJ " + p, "#", "fas fa-project-diagram")]

        #Icons: https://fontawesome.com/v5/search?m=free
        return [#Menu("ASDC", self.public_url(""), "fas fa-road"),
                Menu("ASDC Tools", "#", "fas fa-tools", submenu=[
                    Menu("Settings", self.public_url(""), "fas fa-cog"),
                    Menu("Cesium", self.public_url("cesium/"), "fas fa-globe-asia"),
                    Menu("Terria", self.public_url("terria/"), "fas fa-map"),
                    #Menu("Terria", f"https://{host}/terria/", "fas fa-map"),
                  ]),
                Menu("JupyterHub", self.public_url("jupyterhub/"), "fab fa-python", submenu=[
                    Menu("Browser: Open projects on right  will be mounted in the selected JupyterHub instance", "#", "fas fa-folder-open icon"),
                    #Menu("JupyterHub inline", self.public_url("jupyterhub/"), "fab fa-python"),
                    Menu("JupyterHub", f"https://jupyter.{host}/", "fab fa-python"),
                    Menu("Project Files", f"javascript:open_jhub('{host}', 'exp');", "fas fa-folder-open icon"),
                        #Menu("Custom Test", f"https://jupyter.{host}/hub/spawn?image=jupyter/minimal-notebook:hub-2.2.2&mem_limit=8196M", "fas fa-stream"),
                  ]),
                  Menu("Pipelines", "#", "fas fa-stream", submenu=submenu),
                  #Menu("Saved projects", "#", "fas fa-stream", submenu=prjmenu),
               ]

    def include_js_files(self):
        return ["load_buttons.js"]

    def include_css_files(self):
        return ['style.css'] #In public

    def build_jsx_components(self):
        return ["OpenButton.jsx", "EditButton.jsx"]

    def app_mount_points(self):
        return [
            MountPoint("$", HomeView(self)),
            #MountPoint('/test/$', lambda request: render(request, self.template_path("iframe.html"), {
            MountPoint('/cesium/$', lambda request: render(request, self.template_path("iframe.html"), {
                'frame_url' : f"https://{host}/cesium/Apps/ASDC/",
            })),
            MountPoint('/terria/$', lambda request: render(request, self.template_path("iframe.html"), {
                'frame_url' : f"https://{host}/terria/",
            })),
            #MountPoint('/jupyterhub/$', lambda request: redirect(f"https://jupyter.{host}")),
            #MountPoint('/pipelines/$', lambda request: redirect(f"https://jupyter.{host}")),

            MountPoint("load_buttons.js$", LoadButtonsView(self)),
            #MountPoint("tasks/(?P<pk>[^/.]+)/open", OpenTaskView.as_view()),
        ]

    def api_mount_points(self):
        return [
            MountPoint('userprojects', GetUserProjects.as_view()),
            MountPoint('usertasks', GetUserProjectsAndTasks.as_view()),
            MountPoint('userpipelines', GetUserPipelines.as_view()),
            MountPoint("projects/(?P<project_pk>[^/.]+)/gettasks", GetProjectTasks.as_view()),
            MountPoint('saveprojects', SaveProjects.as_view()),
            MountPoint('clearprojects', ClearProjects.as_view()),
        ]
