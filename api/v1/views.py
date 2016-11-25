from rest_framework import serializers, views, viewsets, filters
from django import shortcuts

from dreamjub import models as core_models
from api.filters import extended as extended_filters


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Student
        fields = '__all__'


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    # Permissions
    required_scopes = []

    # Content
    queryset = core_models.Student.objects.all()
    serializer_class = StudentSerializer

    # Filtering
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,
                       filters.SearchFilter, extended_filters.TLFilter)
    filter_fields = ('college', 'room', 'year', 'majorShort', 'status',
                     'country', 'active')
    search_fields = ('username', 'firstName', 'lastName')
    ordering_fields = ('id', 'eid', 'year', 'majorShort')

    lookup_field = 'username'


class CurrentStudentView(views.APIView):
    def get(self, request):
        student = shortcuts.get_object_or_404(core_models.Student,
                                              username=request.user.username)

        serializer = StudentSerializer(student)
        return views.Response(serializer.data)
