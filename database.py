import sys
import sqlite3
import time
from datetime import datetime
from sensorList import Sensors

class LocalDatabase(object):
    __instance = None
    @staticmethod
    def getInstance():
        if LocalDatabase.__instance is None:
            LocalDatabase()
        else:
            return LocalDatabase.__instance

    def __init__(self):
        try:
            self.conn = sqlite3.connect(sys.path[0] + "/raspServer/db.sqlite3")
        except Exception as e:
            print(e)
        LocalDatabase.__instance = self
        sensors = Sensors().getSensorIDsAndNames()
        for id, name in sensors.items():
            self.createSensorInDatabaseIfNotExist(id, name)
        
    
    def getSensorIDs(self):
        cur = self.conn.cursor()
        cur.execute("SELECT sensor_id FROM main_sensor")
        rows = cur.fetchall()
        sensorIDs = []
        for row in rows:
            sensorIDs.append(row[0])
        return sensorIDs
    
    def getSensorNames(self):
        cur = self.conn.cursor()
        cur.execute("SELECT sensor_name FROM main_sensor")
        rows = cur.fetchall()
        sensor_names = []
        for row in rows:
            sensor_names.append(row[0])
        return sensor_names
    
    def updateSensorData(self, sensor_readings):
        cur = self.conn.cursor()
        for reading in sensor_readings:
            query = "UPDATE main_sensor SET temperature_data=?, temperature_date=? WHERE sensor_id=?"
            try:
                cur.execute(query, reading)
            except Exception as e:
                print(e)
            try:
                self.conn.commit()
            except Exception as e:
                print(e)
    
    def getSensorNameWithID(self, id):
        cur = self.conn.cursor()
        cur.execute("SELECT sensor_name FROM main_sensor WHERE sensor_id=?",(id,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][0]

    def createSensorInDatabaseIfNotExist(self, id, name):
        cur = self.conn.cursor()
        if self.getSensorNameWithID(id) == None:
            cur.execute("INSERT INTO main_sensor(sensor_id, sensor_name, temperature_date, notification_treshold, temperature_data) VALUES (?, ?, ?, ?, ?)"
            ,(id, name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 24, 10))

    
    def destroyConnection(self):
        self.__instance = None
        self.conn.close()