from django.contrib.auth.models import User
from app.models import Project
from rest_framework.views import APIView
from rest_framework import exceptions, permissions, parsers
from rest_framework.response import Response

class GetUserProjects(APIView):
    # Returns list of user projects given email address
    # ROOTURL/api/plugins/asdc/userprojects?email=email@host.tld

    #Allow access only to authorised users
    #permission_classes = (permissions.IsAuthenticated,)

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

