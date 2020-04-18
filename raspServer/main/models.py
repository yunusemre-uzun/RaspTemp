from django.db import models

class Sensor(models.Model):
    sensor_id = models.CharField(max_length=200)
    sensor_name = models.CharField(max_length=200)
    temperature_date = models.DateTimeField('time read')
    notification_treshold = models.IntegerField(default=24)
    temperature_data = models.FloatField(default=None)
    def __str__(self):
        return self.sensor_id
    
    #def chanceSensorName(self, new_name):
