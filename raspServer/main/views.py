from django.template import loader
from django.http import HttpResponse

from .models import Sensor


def index(request):
    sensor_list = Sensor.objects.order_by('sensor_id')
    template = loader.get_template('index.html')
    context = {
        'sensor_list': sensor_list,
    }
    return HttpResponse(template.render(context, request))

def new_name(request, sensor_id, new_name):
    try:
        sensor = Sensor.objects.get(sensor_id=sensor_id)
    except Exception as e:
        print(e)
    sensor.sensor_name = new_name
    sensor.save()
    return HttpResponse(status=201)

