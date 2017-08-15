# Create your views here.
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
import json
from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import list_route, detail_route
from .models import User, Location, Visit
from .serializers import UserSerializer, LocationSerializer, VisitSerializer

from django.db.models import Avg
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)


class NewMixin(object):
    @list_route(methods=['post'])
    def new(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_200_OK, headers=headers)


class UserViewSet(viewsets.ModelViewSet, NewMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['get'])
    def visits(self, request, pk=None):
        data = request.GET
        from_date = data.get('fromDate')
        to_date = data.get('toDate')
        country = data.get('country')
        to_distance = data.get('toDistance')
        filter_ = {
            "user": pk,
            "visited_at__gt": from_date,
            "visited_at__lt": to_date,
            "location__country": country,
            "location__distance__lt": to_distance
        }
        for x in list(filter_.keys()):
            if not filter_[x]:
                del filter_[x]

        visits_set = Visit.objects.filter(**filter_).order_by('visited_at')
        serializer = VisitSerializer(visits_set, many=True)
        result = {"visits": serializer.data}
        return Response(result)


class LocationViewSet(viewsets.ModelViewSet, NewMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @detail_route(methods=['get'])
    def avg(self, request, pk=None):
        data = request.GET
        from_date = data.get('fromDate')
        to_date = data.get('toDate')
        from_age = data.get('fromAge')
        to_age = data.get('toAge')
        gender = data.get('gender')

        filter_ = {
            "pk": pk,
            "visit__visited_at__gt": from_date,
            "visit__visited_at__lt": to_date,
            "visit__user__gender": gender,

        }
        for x in list(filter_.keys()):
            if not filter_[x]:
                del filter_[x]

        locations_avg = Location.objects.filter(**filter_).aggregate(avg=Avg('visit__mark'))
        return Response(locations_avg)


class VisitViewSet(viewsets.ModelViewSet, NewMixin):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
