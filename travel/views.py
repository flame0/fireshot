# Create your views here.
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import list_route
from .models import User, Location, Visit
from .serializers import UserSerializer, LocationSerializer, VisitSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(methods=['post'])
    def new(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_200_OK, headers=headers)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
