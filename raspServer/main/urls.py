from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sensors/<str:sensor_id>/<str:new_name>', views.new_name, name='new_name')
]