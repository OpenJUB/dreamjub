from rest_framework import serializers, views
from oauth2_provider.ext import rest_framework as oauth_ext
from django import shortcuts

from dreamjub import models as core_models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Student
        fields = '__all__'


class CurrentStudentView(views.APIView):
    permission_classes = [oauth_ext.TokenHasScope]
    required_scopes = ['profile']

    def get(self, request):
        student = shortcuts.get_object_or_404(core_models.Student,
                                              username=request.user.username)

        serializer = StudentSerializer(student)
        return views.Response(serializer.data)
