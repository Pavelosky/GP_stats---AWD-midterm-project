from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Circuit, Race, Rider, Team, Result

def index(request):
    circuits = Circuit.objects.all()
    return render(request, 'index.html', {'circuits': circuits})

def circuit_detail(request, circuit_id):
    circuit = get_object_or_404(Circuit, id=circuit_id)
    races = Race.objects.filter(circuit=circuit)
    return render(request, 'circuit_detail.html', {'circuit': circuit, 'races': races})

def race_detail(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    results = Result.objects.filter(race=race)
    return render(request, 'race_detail.html', {'race': race, 'results': results})
