from errors import DatabaseException
import threading
import time
import firebase_admin
import sys
from database import LocalDatabase
from sensorList import Sensors
from datetime import datetime
from firebase_admin import credentials, db

file = 'logs.txt'


def initialize_firebase(path_to_key):
    cred = credentials.Certificate(path_to_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://rasptemp-c417a.firebaseio.com"
    })

def writeSensorReadingsToCloudDatabase(sensor_readings):
    ref = db.reference('server')
    users_ref = ref.child('temperatures')
    local_database = LocalDatabase.getInstance()
    data = {}
    current_time = datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
    for sensor_reading in sensor_readings:
        data[local_database.getSensorNameWithID(sensor_reading[2])] = sensor_reading[0]
        current_time = sensor_reading[1]
    try:
        users_ref.set({
            current_time: data,
        })
    except Exception as e:
        raise DatabaseException(2,e)

def readSensors(sensorIDs):
    sensor_readings = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for id in sensorIDs:
        try:
            sensor_temperature = Sensors.readSensorWithID(id)
            sensor_readings.append((sensor_temperature/1000,current_time, id,))
        except Exception as e:
            sensor_readings.append((10,current_time, id,))
            print (e)
    printSensorReadings(sensor_readings)
    return sensor_readings

def printSensorReadings(sensor_readings):
    global file
    current_time = datetime.now()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S \n")
    with open(file, 'a') as f:
        f.write(current_time)
    for i,reading in enumerate(sensor_readings):
        print("{}. sensor read {}".format(i,reading))
        with open(file, 'a') as f:
            f.write("{}. sensor read {} \n".format(i,reading))
    return None

def initialize():
    try:
        initialize_firebase(sys.path[0] + "/rasptemp-c417a-firebase-adminsdk-ydsnp-68e9d136f8.json")
    except Exception as e:
        raise DatabaseException(1,e)

def main(sensorIDs):
    sensor_readings = readSensors(sensorIDs)
    try:
        writeSensorReadingsToCloudDatabase(sensor_readings)
    except DatabaseException as e:
        print(e)
    except Exception as e:
        print(e)
    local_database = LocalDatabase.getInstance()
    try:
        local_database.updateSensorData(sensor_readings)
    except Exception as e:
        print(e)
    

def regular(interval, worker_function):
    threading.Timer(interval, regular, args=[ interval,worker_function]).start()
    local_database = LocalDatabase().getInstance()
    sensorIDs = local_database.getSensorIDs()
    worker_function(sensorIDs)
    local_database.destroyConnection()


if __name__ == '__main__':
    try:
       initialize()
    except Exception as e:
        print(e)
    regular(60, main)

    #main(sensorIDs, sensorNames)

    