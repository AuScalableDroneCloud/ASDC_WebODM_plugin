from django.contrib.auth.models import User
from app.models import Project
from rest_framework.views import APIView
from rest_framework import exceptions, permissions, parsers
from rest_framework.response import Response

class GetUserProjects(APIView):
    # Returns list of user projects given email address
    # ROOTURL/api/plugins/asdc/userprojects?email=email@host.tld
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        email = self.request.query_params.get('email', None)
        try:
            user = User.objects.get(email = email)
            projects = Project.objects.filter(owner_id = user.id)
            plist = [p.id for p in projects]
        except:
            plist = []

        return Response(plist)

