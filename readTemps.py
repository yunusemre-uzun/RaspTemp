from sensorList import Sensors
from errors import DatabaseException
import threading
import time
import firebase_admin
import sys
from firebase_admin import credentials, db

def initialize_firebase(path_to_key):
    cred = credentials.Certificate(path_to_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://rasptemp-c417a.firebaseio.com"
    })

def writeSensorReadingsToCloudDatabase(sensor_readings, sensor_names):
    ref = db.reference('server')
    users_ref = ref.child('temperatures')
    current_time = time.localtime()
    current_time = '{}-{}-{}-{}:{}'.format(current_time.tm_mday,current_time.tm_mon,current_time.tm_year,current_time.tm_hour,current_time.tm_min)
    print(current_time)
    try:
        users_ref.set({
            current_time: {
                sensor_names[0]: sensor_readings[0],
                sensor_names[1]: sensor_readings[1]
            },
        })
    except Exception as e:
        raise DatabaseException(2,e)


def readSensors(sensorIDs):
    sensor_readings = []
    for id in sensorIDs:
        try:
            sensor_temperature = Sensors.readSensorWithID(id)
            sensor_readings.append(sensor_temperature/1000)
        except Exception as e:
            sensor_readings.append(10)
            print (e)
    printSensorReadings(sensor_readings)
    return sensor_readings

def printSensorReadings(sensor_readings):
    for i,reading in enumerate(sensor_readings):
        print("{}. sensor read {}".format(i,reading))
    return None

def initialize():
    print(sys.path)
    try:
        initialize_firebase(sys.path[0] + "/rasptemp-c417a-firebase-adminsdk-ydsnp-07e62a0cc3.json")
    except Exception as e:
        raise DatabaseException(1,e)
    sensor = Sensors()
    sensorIDs = sensor.getSensorIDs()
    sensorNames = sensor.getSensorNames()
    return sensorIDs, sensorNames

def main(sensorIDs, sensorNames):
    while True:
        sensor_readings = readSensors(sensorIDs)
        try:
            writeSensorReadingsToCloudDatabase(sensor_readings, sensorNames)
        except DatabaseException as e:
            print(e)
        except Exception as e:
            print(e)
        time.sleep(60.0)

if __name__ == '__main__':
    try:
        sensorIDs, sensorNames = initialize()
    except Exception as e:
        print(e)
    main(sensorIDs, sensorNames)

    