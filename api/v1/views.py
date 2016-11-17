from rest_framework import serializers, views, viewsets, filters, decorators
from django import shortcuts
from django import conf
from django import http

from dreamjub import models as core_models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Student
        exclude = ('id', 'eid', 'picture')


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    # Permissions
    required_scopes = []

    # Content
    queryset = core_models.Student.objects.all()
    serializer_class = StudentSerializer

    # Filtering
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,
                       filters.SearchFilter)
    filter_fields = ('college', 'room', 'year', 'majorShort', 'status',
                     'country', 'active')
    search_fields = ('username', 'firstName', 'lastName')
    ordering_fields = ('id', 'eid', 'year', 'majorShort')

    lookup_field = 'username'

    @decorators.detail_route()
    def image(self, request, username=None):
        user = self.get_object()

        if not user.picture:
            raise shortcuts.Http404()

        if conf.settings.DEBUG:
            return shortcuts.redirect(user.picture.url)
        else:
            # Serve the file using nginx's X-Accel-Redirect header
            # https://www.nginx.com/resources/wiki/start/topics/examples/x
            # -accel/#x-accel-redirect
            r = http.HttpResponse()
            r['X-Accel-Redirect'] = "/media/" + user.picture.name
            r['Content-Type'] = "image/jpg"

            return r


class CurrentStudentView(views.APIView):
    def get(self, request):
        student = shortcuts.get_object_or_404(core_models.Student,
                                              username=request.user.username)

        serializer = StudentSerializer(student)
        return views.Response(serializer.data)
