from rest_framework import serializers
from .models import Circuit, Race, Result, Rider, Team

class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = '__all__'

class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    rider = serializers.SlugRelatedField(slug_field='name', queryset=Rider.objects.all())
    team = serializers.SlugRelatedField(slug_field='name', queryset=Team.objects.all())

    class Meta:
        model = Result
        fields = '__all__'

class RiderDetailSerializer(serializers.ModelSerializer):
    total_points = serializers.FloatField()
    teams = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Rider
        fields = ['name', 'number', 'country', 'total_points', 'teams']

class ResultDetailSerializer(serializers.ModelSerializer):
    race = RaceSerializer()
    rider = RiderSerializer()
    team = TeamSerializer()
    result_id = serializers.IntegerField(source='id')

    class Meta:
        model = Result
        fields = ['result_id', 'race', 'rider', 'team', 'position', 'points', 'time', 'speed']