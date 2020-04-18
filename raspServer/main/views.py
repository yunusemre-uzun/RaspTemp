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

