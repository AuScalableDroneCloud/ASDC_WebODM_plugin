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
from .pipelines import get_json
import requests

class Plugin(PluginBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Just get the default pipelines without custom user settings
        self.saved_projects = []

    def main_menu_user(self, user):
        submenu = []
        pipelines = get_json(user)
        for p in pipelines:
            tag = p["tag"]
            #Set the open function, will alert and abort if inputs not available
            function = 'pipeline_run';
            if "inputs" in p and "task" in p["inputs"]:
                function = 'pipeline_task';
            elif "inputs" in p and "project" in p["inputs"]:
                function = 'pipeline_project';

            #submenu += [Menu(p["name"], f"https://jupyter.{host}/hub/spawn?profile={tag}", p["icon"])]
            submenu += [Menu(p["name"], f"javascript:{function}('{user.email}', '{host}', '{tag}');", p["icon"])]

        prjmenu = [Menu("Add To Saved", f"javascript:save_open_projects();", "fas fa-project-diagram"),
                   Menu("Clear Saved", f"javascript:clear_open_projects();", "fas fa-trash-alt")]
        for p in self.saved_projects:
            prjmenu += [Menu("PRJ " + p, "#", "fas fa-project-diagram")]

        #Icons: https://fontawesome.com/v5/search?m=free
        return [#Menu("ASDC", self.public_url(""), "fas fa-road"),
                Menu("ASDC Tools", "#", "fas fa-tools", submenu=[
                    Menu("Settings", self.public_url(""), "fas fa-cog"),
                    Menu("JupyterHub", f"https://jupyter.{host}", "fab fa-python"),
                    Menu("JupyterHub - base", f"https://jupyter.{host}/hub/spawn?profile=base", "fab fa-python"),
                    Menu("JupyterHub - gpu", f"https://jupyter.{host}/hub/spawn?profile=gpu", "fab fa-python"),
                    Menu("JupyterHub - ml", f"https://jupyter.{host}/hub/spawn?profile=ml", "fab fa-python"),
                    Menu("Project Files", f"javascript:pipeline_project('{user.email}', '{host}', 'base');", "fas fa-folder-open icon"),
                    #Menu("Cesium", self.public_url("cesium/"), "fas fa-globe-asia"),
                    #Menu("Terria", self.public_url("terria/"), "fas fa-map"),
                    Menu("Cesium", f"https://terria.{host}/", "fas fa-globe-asia"),
                    Menu("Terria", f"https://cesium.{host}", "fas fa-map"),
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
