from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Circuit, Race, Rider, Team, Result

def index(request):
    circuits = Circuit.objects.all()
    return render(request, 'index.html', {'circuits': circuits})

def circuit_detail(request, circuit_id):
    circuit = get_object_or_404(Circuit, id=circuit_id)
    races = Race.objects.filter(circuit=circuit)
    categories = Race.objects.values_list('category', flat=True).distinct()
    return render(request, 'circuit_detail.html', {'circuit': circuit, 'races': races, 'categories': categories})

def race_detail(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    results = Result.objects.filter(race=race)
    riders = Rider.objects.all()
    teams = Team.objects.all()
    return render(request, 'race_detail.html', {'race': race, 'results': results, 'riders': riders, 'teams': teams})

def add_race(request, circuit_id):
    if request.method == 'POST':
        year = request.POST['year']
        category = request.POST['category']
        sequence = request.POST['sequence']
        circuit = get_object_or_404(Circuit, id=circuit_id)
        Race.objects.create(year=year, category=category, sequence=sequence, circuit=circuit)
        return redirect('circuit_detail', circuit_id=circuit_id)
    return redirect('circuit_detail', circuit_id=circuit_id)

def add_result(request, race_id):
    if request.method == 'POST':
        race = get_object_or_404(Race, id=race_id)
        rider = get_object_or_404(Rider, id=request.POST['rider'])
        team = get_object_or_404(Team, id=request.POST['team'])
        position = request.POST['position']
        points = request.POST['points']
        time = request.POST['time']
        speed = request.POST['speed']
        Result.objects.create(race=race, rider=rider, team=team, position=position, points=points, time=time, speed=speed)
        return redirect('race_detail', race_id=race_id)
    return redirect('race_detail', race_id=race_id)
