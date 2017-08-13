import datetime
from rest_framework import serializers
from .models import User, Location, Visit
import time


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))

    def to_internal_value(self, data):
        return datetime.datetime.utcfromtimestamp(int(data))


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    birth_date = TimestampField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Location
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    visited_at = TimestampField()

    class Meta:
        model = Visit
        fields = '__all__'
