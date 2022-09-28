from django.contrib.auth.models import User
from app.models import Project, Task
from rest_framework.views import APIView
from rest_framework import exceptions, permissions, parsers
from rest_framework.response import Response
from app.plugins.views import TaskView

class GetUserProjects(APIView):
    # Returns list of user projects given email address
    # ROOTURL/api/plugins/asdc/userprojects?email=email@host.tld

    #Allow read access to anon
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        email = self.request.query_params.get('email', None)
        detail = self.request.query_params.get('detail', False)
        try:
            user = User.objects.get(email = email)
            #TODO: support shared projects too (read/write or read only)
            projects = Project.objects.filter(owner_id = user.id)
            if detail:
                plist = [{"id": p.id, "name": p.name, "description": p.description} for p in projects]
            else:
                plist = [p.id for p in projects]
        except:
            plist = []

        return Response(plist)

class GetUserProjectsAndTasks(APIView):
    # Returns list of user projects and their tasks given email address
    # ROOTURL/api/plugins/asdc/usertasks?email=email@host.tld

    #Allow read access to anon
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        email = self.request.query_params.get('email', None)
        try:
            user = User.objects.get(email = email)
            #TODO: support shared projects too (read/write or read only)

            plist = []
            projects = Project.objects.filter(owner_id = user.id)
            for p in projects:
                #Populate the tasks list
                #select column_name,data_type from information_schema.columns where table_name = 'app_task';
                tasks = Task.objects.filter(project_id = p.id)
                tlist = [{"id": t.id, "name": t.name} for t in tasks]
                #Append project entry
                plist.append({"id": p.id, "name": p.name, "description": p.description, "tasks" : tlist})

        except:
            plist = []

        return Response(plist)


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
            tasks = Task.objects.filter(project_id = project_pk)
            tlist = [{"id": t.id, "name": t.name} for t in tasks]
        except:
            tlist = []

        p = Project.objects.filter(id = project_pk)[0]
        pdata = {"id": p.id, "name": p.name, "description": p.description, "tasks" : tlist}

        return Response(pdata)

"""
class CheckUrlTaskView(TaskView):
    def get(self, request, project_pk=None, pk=None):

        # Assert that task exists
        self.get_and_check_task(request, pk)

        # Check if there is an imported url associated with the project and task
        combined_id = "{}_{}".format(project_pk, pk)
        data = get_current_plugin().get_global_data_store().get_json(combined_id, default = None)

        if data == None or 'ddbWebUrl' not in data:
            return Response({'ddbWebUrl': None}, status=status.HTTP_200_OK)
        else:
            return Response({'ddbUrl': data['ddbWebUrl']}, status=status.HTTP_200_OK)


"""
