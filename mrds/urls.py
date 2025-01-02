from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('circuit/<int:circuit_id>/', views.circuit_detail, name='circuit_detail'),
    path('race/<int:race_id>/', views.race_detail, name='race_detail'),
    path('circuit/<int:circuit_id>/add_race/', views.add_race, name='add_race'),
    path('race/<int:race_id>/add_result/', views.add_result, name='add_result'),
    path('result/<int:result_id>/delete/', views.delete_result, name='delete_result'),
    path('api/add_race_result/', api.add_race_result, name='add_race_result'),
    path('api/top_riders/<str:category>/<int:year>/', api.top_riders_by_category_and_year, name='top_riders_by_category_and_year'),
    path('api/average_speeds/<int:circuit_id>/', api.average_speeds_at_circuit, name='average_speeds_at_circuit'),
    path('api/edit_race_result/<int:result_id>/', api.edit_race_result, name='edit_race_result'),
    path('api/manufacturer_performance/', api.manufacturer_performance_over_time, name='manufacturer_performance_over_time'),
    path('api/remove_race_results/<int:circuit_id>/', api.remove_race_results_for_circuit, name='remove_race_results_for_circuit'),
]