from rest_framework import status
from rest_framework.response import Response

from app.plugins import PluginBase, Menu, MountPoint, get_current_plugin
from app.plugins.views import TaskView
from django.shortcuts import render, redirect
from django import forms
from django.views.generic.base import RedirectView

from .app_views import HomeView, LoadButtonsView
from .api_views import GetUserProjects, GetUserProjectsAndTasks, GetProjectTasks

import os
host = os.environ.get('WO_HOST')

class Plugin(PluginBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def main_menu(self):
        #Icons: https://fontawesome.com/v5/search?m=free
        return [#Menu("ASDC", self.public_url(""), "fas fa-road"),
                Menu("ASDC Tools", "#", "fas fa-toolbox", submenu=[
                    Menu("Settings", self.public_url(""), "fas fa-globe-asia"),
                    Menu("Cesium", self.public_url("cesium/"), "fas fa-globe-asia"),
                    Menu("Terria", self.public_url("terria/"), "fas fa-map"),
                    #Menu("Terria", f"https://{host}/terria/", "fas fa-map"),
                  ]),
                Menu("JupyterHub", self.public_url("jupyterhub/"), "fab fa-python", submenu=[
                    #Menu("JupyterHub inline", self.public_url("jupyterhub/"), "fab fa-python"),
                    Menu("JupyterHub", f"https://jupyter.{host}/", "fab fa-python"),
                    Menu("Project Files", f"javascript:location.href = 'https://jupyter.{host}/hub/spawn?profile=exp-' + new URLSearchParams(window.location.search).get('project_task_open').replaceAll(',','-')", "fas fa-folder-open icon"),
                    #Menu("Pipelines", "#", "fas fa-stream", submenu=[
                        Menu("Default", f"https://jupyter.{host}/hub/spawn?profile=default", "fas fa-stream"),
                        Menu("Base", f"https://jupyter.{host}/hub/spawn?profile=base", "fas fa-stream"),
                        Menu("Fracture Detection", f"https://jupyter.{host}/hub/spawn?profile=fd", "fas fa-stream"),
                        Menu("Experimental", f"https://jupyter.{host}/hub/spawn?profile=exp", "fas fa-stream"),
                        #Menu("Custom Test", f"https://jupyter.{host}/hub/spawn?image=jupyter/minimal-notebook:hub-2.2.2&mem_limit=8196M", "fas fa-stream"),
                    #]), #It seems only one submenu level is possible
                  ]),
               ]

    def include_js_files(self):
        return ["load_buttons.js"]

    #def include_css_files(self):
    #    return ['test.css'] #In public

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
            MountPoint("projects/(?P<project_pk>[^/.]+)/gettasks", GetProjectTasks.as_view()),
            #MountPoint("projects/(?P<project_pk>[^/.]+)/tasks/(?P<pk>[^/.]+)/checkforurl", CheckUrlTaskView.as_view()),
            #MountPoint('task/(?P<pk>[^/.]+)/shortlink', GetShortLink.as_view()),
        ]
