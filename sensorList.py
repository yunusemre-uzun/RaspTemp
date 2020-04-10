class Sensors(object):
    def __init__(self):
        self.sensorIDs = [
            "28-030297790ba5",
            "28-030297791fbc",
        ]
        self.sensorNames = [
            "Ranza-1",
            "Ranza-2",
        ]
    
    def getSensorIDs(self):
        return self.sensorIDs
    
    def getSensorNames(self):
        return self.sensorNames
    
    @staticmethod
    def readSensorWithID(id):
        try:
            mytemp = ''
            filename = 'w1_slave'
            f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
            line = f.readline() # read 1st line
            crc = line.rsplit(' ',1)
            crc = crc[1].replace('\n', '')
            print(crc)
            if crc=='YES':
                line = f.readline() # read 2nd line
                mytemp = line.rsplit('t=',1)
            else:
                raise Exception('Temperature sensor reading error on sensor {}'.format(id))
            return int(mytemp[1])
        except:
            raise Exception('Temperature sensor id error on sensor {}'.format(id))