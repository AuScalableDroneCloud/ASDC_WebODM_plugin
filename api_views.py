from django.contrib.auth.models import User
from app.models import Project, Task
from rest_framework.views import APIView
from rest_framework import exceptions, permissions, parsers
from rest_framework.response import Response
from app.plugins.views import TaskView
from app.plugins import get_current_plugin
import json
from .pipelines import get_json

def get_user_projects(email, detail=True):
    try:
        user = User.objects.get(email = email)
        #Get users own projects
        projects = Project.objects.filter(owner_id = user.id).order_by('id')
        if detail:
            plist = {p.id: {"name": p.name, "description": p.description, "readonly": False} for p in projects}
        else:
            plist = {p.id: {"readonly": False} for p in projects}

        #Get the shared projects this user has access to (including view only)
        plist = {}
        for e in user.projectuserobjectpermission_set.all().order_by('id'):
            entry = {"readonly": False}
            if detail:
                entry = {"name": e.content_object.name, "description": e.content_object.description, "readonly": False}
            if e.permission.codename == "change_project":
                plist[e.content_object_id] = entry
            elif e.permission.codename == "view_project" and not e.content_object_id in plist:
                entry["readonly"] = True
                plist[e.content_object_id] = entry
    except:
        plist = {}
    return dict(sorted(plist.items()))

class GetUserProjects(APIView):
    # Returns list of user projects given email address
    # ROOTURL/api/plugins/asdc/userprojects?email=email@host.tld

    #Allow read access to anon
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        email = self.request.query_params.get('email', None)
        detail = self.request.query_params.get('detail', False)
        return Response(get_user_projects(email, detail))

class GetUserProjectsAndTasks(APIView):
    # Returns list of user projects and their tasks given email address
    # ROOTURL/api/plugins/asdc/usertasks?email=email@host.tld

    #Allow read access to anon
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        email = self.request.query_params.get('email', None)

        #Get users own projects + tasks
        plist = get_user_projects(email)

        try:
            #Populate the tasks lists
            for p in plist:
                #select column_name,data_type from information_schema.columns where table_name = 'app_task';
                tasks = Task.objects.filter(project_id = p).order_by('-created_at')
                plist[p]["tasks"] = [{"id": str(t.id), "name": t.name} for t in tasks]

        except:
            plist = {}

        return Response(plist)

class GetUserPipelines(APIView):
    # Returns list of user pipelines given email address
    # ROOTURL/api/plugins/asdc/userpipelines?email=email@host.tld

    #Allow read access to anon
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        email = self.request.query_params.get('email', None)
        if email is not None:
            user = User.objects.get(email=email)
        return Response(get_json(user))

class GetProjectTasks(TaskView):
    # Returns list of tasks for given project id in url
    # ROOTURL/api/plugins/asdc/projects/PROJECT_ID/gettasks

    #Allow access only to authorised users
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, project_pk=None):

        #task = self.get_and_check_task(request, pk)
        #task_id  = str(task.id)
        try:
            #select column_name,data_type from information_schema.columns where table_name = 'app_task';
            tasks = Task.objects.filter(project_id = project_pk).order_by('-created_at')
            tlist = [{"id": str(t.id), "name": t.name} for t in tasks]
        except:
            tlist = []

        p = Project.objects.filter(id = project_pk)[0]
        pdata = {"id": p.id, "name": p.name, "description": p.description, "tasks" : tlist}

        return Response(pdata)

class SaveProjects(APIView):
    # Stores passed list of user projects temporarily
    # ROOTURL/api/plugins/asdc/saveprojects?projects=X,Y,Z

    #Allow read access to anon
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = self.request.query_params.get('projects', None)
        #ds = get_current_plugin().get_user_data_store(request.user)
        plugin = get_current_plugin()
        plugin.saved_projects += projects.split(',')
        #Remove duplicates
        plugin.saved_projects = list(set(plugin.saved_projects))
        return Response()

class ClearProjects(APIView):
    # Clear stored list of user projects
    # ROOTURL/api/plugins/asdc/clearprojects

    #Allow read access to anon
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        plugin = get_current_plugin()
        plugin.saved_projects = []
        return Response()

