import datetime
from rest_framework import serializers
from .models import User, Location, Visit
import time


class TimestampField(serializers.Field):
    def to_native(self, value):
        epoch = datetime.datetime(1970,1,1)
        return int((value - epoch).total_seconds())

    def to_internal_value(self,data):
        pass


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    birth_date = TimestampField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
