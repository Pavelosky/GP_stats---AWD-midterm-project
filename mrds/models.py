from django.db import models

# Create your models here.

class Circuit(models.Model):
    shortname = models.CharField(max_length=50)
    circuit_name = models.CharField(max_length=100)

    def __str__(self):
        return f" Circuit {self.circuit_name} - {self.shortname}"


class Rider(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    number = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    bike_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Race(models.Model):
    year = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    sequence = models.PositiveIntegerField()
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} - {self.category} - {self.sequence}"


class Result(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.IntegerField(null=True, blank=True)
    points = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    time = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Race {self.race} - Rider {self.rider} - Position {self.position}"