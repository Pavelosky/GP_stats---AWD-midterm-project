from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Sum
from .models import Circuit, Rider, Team, Race, Result
from .serializers import RaceSerializer, ResultSerializer, RiderDetailSerializer, ResultDetailSerializer, RiderSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def add_rider(request):
    if request.method == 'POST':
        serializer = RiderSerializer(data=request.data)
        if serializer.is_valid():
            rider = serializer.save()
            return Response({'id': rider.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_race_result(request, race_id):
    if request.method == 'POST':
        race = get_object_or_404(Race, id=race_id)
        result_data = request.data
        result_data['race'] = race.id
        result_serializer = ResultSerializer(data=result_data)
        if result_serializer.is_valid():
            result = result_serializer.save()
            return Response({'id': result.id}, status=status.HTTP_201_CREATED)
        return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def top_riders_by_category_and_year(request, category, year):
    results = Result.objects.filter(race__category=category, race__year=year)
    top_riders = results.values('rider__name').annotate(total_points=Sum('points')).order_by('-total_points')
    return Response(top_riders)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def edit_race_result(request, result_id):
    if request.method == 'PATCH':
        result = get_object_or_404(Result, id=result_id)
        
        data = request.data
        
        serializer = ResultSerializer(result, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'id': result.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_race_result(request, result_id):
    if request.method == 'DELETE':
        result = get_object_or_404(Result, id=result_id)
        result.delete()
        return Response({'deleted': result_id})
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_riders(request):
    riders = Rider.objects.all()
    rider_data = []
    for rider in riders:
        total_points = Result.objects.filter(rider=rider).aggregate(total_points=Sum('points'))['total_points']
        teams = Result.objects.filter(rider=rider).values_list('team__name', flat=True).distinct()
        rider_data.append({
            'name': rider.name,
            'number': rider.number,
            'country': rider.country,
            'total_points': total_points,
            'teams': list(teams)
        })
    serializer = RiderDetailSerializer(rider_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_results_sorted(request, year):
    results = Result.objects.filter(race__year=year).order_by('race__category', 'race__id')
    data = {}
    
    for result in results:
        category = result.race.category
        race_id = result.race.id
        circuit_name = result.race.circuit.circuit_name
        
        if category not in data:
            data[category] = {}
        
        if circuit_name not in data[category]:
            data[category][circuit_name] = []
        
        data[category][circuit_name].append({
            'race_id': race_id,
            'result_id': result.id,
            'rider': result.rider.name,
            'team': result.team.name,
            'position': result.position,
            'points': result.points,
            'time': result.time,
            'speed': result.speed
        })
    
    return Response(data)
