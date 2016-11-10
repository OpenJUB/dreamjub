from rest_framework import serializers, views
from oauth2_provider.ext.rest_framework import TokenHasScope
from django.shortcuts import get_object_or_404

from dreamjub import models as core_models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Student
        fields = '__all__'


class CurrentStudentView(views.APIView):
    permission_classes = [TokenHasScope]
    required_scopes = ['profile']

    def get(self, request):
        student = get_object_or_404(core_models.Student,
                                    username=request.user.username)

        serializer = StudentSerializer(student)
        return views.Response(serializer.data)
