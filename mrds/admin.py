from django.contrib import admin
from .models import Circuit, Rider, Team, Race, Result
# Register your models here.

class ResultInline(admin.TabularInline):
    model = Result
    extra = 3

class CircuitAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'circuit_name')

class RiderAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'number')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'bike_name')

class RaceAdmin(admin.ModelAdmin):
    list_display = ('year', 'category', 'sequence', 'circuit')
    inlines = [ResultInline]

class ResultAdmin(admin.ModelAdmin):
    list_display = ('race', 'rider', 'team', 'position', 'points', 'speed', 'time')

admin.site.register(Circuit, CircuitAdmin)
admin.site.register(Rider, RiderAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Result, ResultAdmin)