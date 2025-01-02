from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Sum
from .models import Circuit, Rider, Team, Race, Result
from .serializers import RaceSerializer, ResultSerializer, RiderDetailSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def add_race_result(request):
    if request.method == 'POST':
        serializer = RaceSerializer(data=request.data)
        if serializer.is_valid():
            race = serializer.save()
            result_data = request.data.get('result')
            result_data['race'] = race.id
            result_serializer = ResultSerializer(data=result_data)
            if result_serializer.is_valid():
                result = result_serializer.save()
                return Response({'id': result.id}, status=status.HTTP_201_CREATED)
            return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def top_riders_by_category_and_year(request, category, year):
    results = Result.objects.filter(race__category=category, race__year=year)
    top_riders = results.values('rider__name').annotate(total_points=Sum('points')).order_by('-total_points')
    return Response(top_riders)

@api_view(['GET'])
@permission_classes([AllowAny])
def average_speeds_at_circuit(request, circuit_id):
    results = Result.objects.filter(race__circuit_id=circuit_id)
    avg_speed = results.aggregate(average_speed=Avg('speed'))
    return Response(avg_speed)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def edit_race_result(request, result_id):
    if request.method == 'PATCH':
        result = get_object_or_404(Result, id=result_id)
        serializer = ResultSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'id': result.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def manufacturer_performance_over_time(request):
    performance = Result.objects.values('team__bike_name').annotate(total_points=Sum('points')).order_by('-total_points')
    return Response(performance)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_race_results_for_circuit(request, circuit_id):
    if request.method == 'DELETE':
        results = Result.objects.filter(race__circuit_id=circuit_id)
        count, _ = results.delete()
        return Response({'deleted': count})
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
