from sensorList import Sensors
from errors import DatabaseException
import threading
import time
import firebase_admin
import sys
from datetime import datetime
from firebase_admin import credentials, db

file = 'logs.txt'

def initialize_firebase(path_to_key):
    cred = credentials.Certificate(path_to_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://rasptemp-c417a.firebaseio.com"
    })

def writeSensorReadingsToCloudDatabase(sensor_readings, sensor_names):
    ref = db.reference('server')
    users_ref = ref.child('temperatures')
    current_time = datetime.now()
    current_time = current_time.strftime("%m-%d-%Y, %H:%M:%S")
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
    global file
    current_time = datetime.now()
    current_time = current_time.strftime("%m/%d/%Y, %H:%M:%S \n")
    with open(file, 'a') as f:
        f.write(current_time)
    for i,reading in enumerate(sensor_readings):
        print("{}. sensor read {}".format(i,reading))
        with open(file, 'a') as f:
            f.write("{}. sensor read {} \n".format(i,reading))
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
    sensor_readings = readSensors(sensorIDs)
    try:
        writeSensorReadingsToCloudDatabase(sensor_readings, sensorNames)
    except DatabaseException as e:
        print(e)
    except Exception as e:
        print(e)
    #time.sleep(60.0)

def regular(interval, worker_function, sensorIDs, sensorNames):
    threading.Timer(interval, regular, args=[ interval,worker_function, sensorIDs, sensorNames]).start()
    worker_function(sensorIDs, sensorNames)


if __name__ == '__main__':
    try:
        sensorIDs, sensorNames = initialize()
    except Exception as e:
        print(e)
    regular(10, main, sensorIDs, sensorNames)

    #main(sensorIDs, sensorNames)

    