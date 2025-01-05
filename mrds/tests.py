from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from .models import Circuit, Race, Rider, Team, Result

class MRDSTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.circuit = Circuit.objects.create(shortname='Test Circuit', circuit_name='Test Circuit Name')
        self.rider = Rider.objects.create(name='Test Rider', country='Test Country', number=99)
        self.team = Team.objects.create(name='Test Team', bike_name='Test Bike')
        self.race = Race.objects.create(year=2023, category='MotoGP', sequence=1, circuit=self.circuit)
        self.result = Result.objects.create(race=self.race, rider=self.rider, team=self.team, position=1, points=25, speed=150.0, time='1:30:00')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Circuit Name')

    def test_circuit_detail_view(self):
        response = self.client.get(reverse('circuit_detail', args=[self.circuit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Circuit Name')
        self.assertContains(response, 'MotoGP')

    def test_race_detail_view(self):
        response = self.client.get(reverse('race_detail', args=[self.race.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Rider')
        self.assertContains(response, 'Test Team')

    def test_add_race(self):
        response = self.client.post(reverse('add_race', args=[self.circuit.id]), {
            'year': 2024,
            'category': 'Moto2',
            'sequence': 2
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Race.objects.filter(year=2024, category='Moto2', sequence=2, circuit=self.circuit).exists())

    def test_add_result(self):
        response = self.client.post(reverse('add_result', args=[self.race.id]), {
            'rider': self.rider.id,
            'team': self.team.id,
            'position': 2,
            'points': 20,
            'time': '1:31:00',
            'speed': 145.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Result.objects.filter(race=self.race, rider=self.rider, team=self.team, position=2, points=20, speed=145.0, time='1:31:00').exists())


class CircuitModelTest(TestCase):
    def setUp(self):
        self.circuit = Circuit.objects.create(shortname='Test Circuit', circuit_name='Test Circuit Name')

    def test_circuit_creation(self):
        self.assertEqual(self.circuit.shortname, 'Test Circuit')
        self.assertEqual(self.circuit.circuit_name, 'Test Circuit Name')


class RiderModelTest(TestCase):
    def setUp(self):
        self.rider = Rider.objects.create(name='Test Rider', country='Test Country', number=99)

    def test_rider_creation(self):
        self.assertEqual(self.rider.name, 'Test Rider')
        self.assertEqual(self.rider.country, 'Test Country')
        self.assertEqual(self.rider.number, 99)

class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', bike_name='Test Bike')

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.bike_name, 'Test Bike')

class RaceModelTest(TestCase):
    def setUp(self):
        self.circuit = Circuit.objects.create(shortname='Test Circuit', circuit_name='Test Circuit Name')
        self.race = Race.objects.create(year=2023, category='MotoGP', sequence=1, circuit=self.circuit)

    def test_race_creation(self):
        self.assertEqual(self.race.year, 2023)
        self.assertEqual(self.race.category, 'MotoGP')
        self.assertEqual(self.race.sequence, 1)
        self.assertEqual(self.race.circuit, self.circuit)

class ResultModelTest(TestCase):
    def setUp(self):
        self.circuit = Circuit.objects.create(shortname='Test Circuit', circuit_name='Test Circuit Name')
        self.rider = Rider.objects.create(name='Test Rider', country='Test Country', number=99)
        self.team = Team.objects.create(name='Test Team', bike_name='Test Bike')
        self.race = Race.objects.create(year=2023, category='MotoGP', sequence=1, circuit=self.circuit)
        self.result = Result.objects.create(race=self.race, rider=self.rider, team=self.team, position=1, points=25, speed=150.0, time='1:30:00')

    def test_result_creation(self):
        self.assertEqual(self.result.race, self.race)
        self.assertEqual(self.result.rider, self.rider)
        self.assertEqual(self.result.team, self.team)
        self.assertEqual(self.result.position, 1)
        self.assertEqual(self.result.points, 25)
        self.assertEqual(self.result.speed, 150.0)
        self.assertEqual(self.result.time, '1:30:00')