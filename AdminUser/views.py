from django.shortcuts import render
from .models import Movies
from .serializer import ModelSerializer, MovieSerializers
from Utils.custome_viewsets import ModelViewSet
from Utils.custome_permissions import IsAdminUserProject, BlacklistUpdateMethodPermission
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from Utils.exceptions import InvalidParameterException

# Create your views here.
class MovieModelViewSetAPIView(ModelViewSet):
    model = Movies
    queryset = Movies.objects.all()
    serializer_class = MovieSerializers

    create_success_message = "Movie information has been created successfully"
    retrieve_success_message = "Movie information has been retrieved successfully"
    update_success_message = "Movie information has been updated successfully"
    list_success_message = "Movie information has been returned successfully"

    def get_permissions(self):
        if self.action in ['list', 'create', ]:
            permission_classes = [IsAdminUserProject,]
            return [permission() for permission in permission_classes]

        if self.action in ['partial_update', 'retrieve', 'destroy']:
            permission_classes = [IsAdminUserProject]
            return [permission() for permission in permission_classes]

        if self.action == 'update':
            permission_classes = [IsAdminUserProject | BlacklistUpdateMethodPermission]
            return [permission() for permission in permission_classes]

        return super().get_permissions()

    @action(detail=False, methods=['POST'])
    def allocate_movies_to_theter(self, request):
        movie_id = self.request.data.get('movie_id')
        theter_id = self.request.data.get('theter_id')

        if not movie_id and not theter_id:
            raise InvalidParameterException

            

    