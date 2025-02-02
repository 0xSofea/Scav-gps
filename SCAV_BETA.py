#!/usr/bin/env python3
import time
import serial
import json
import numpy
import paho.mqtt.client as mqtt
from datetime import datetime

MQTT_HOST = 'mqtt://192.168.43.174'
MQTT_PORT = 1883
START_TOPIC = 'start'
END_TOPIC = 'end'
        

# mqttc = mqtt.Client()
# mqttc.connect(MQTT_HOST, MQTT_PORT)
# mqttc.on_connect = onconnect


commands = [
    b'at!entercnd=\"A710\"\r',
    b'at!custom=\"gpsenable\",1\r',
    b'at!custom=\"gpssel\",0\r',
    b'at!gpsautostart=1,1,100,10,10\r',
    b'at!gpsloc?\r'
]

dev = serial.Serial("/dev/ttyUSB2", 115200, timeout=0)
dev.flushInput() 

def latlon(raw):
    return round((float(raw[0]) + float(raw[2])/60 + float(raw[4])/(60*60)) * (-1 if raw[6] in ['W', 'S'] else 1), 7)

def dateTime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def skipLines(dev):
    raw = dev.readline()
    res = raw.decode('utf-8').strip('\r\n')
    if "Lat:" in res or "Lon:" in res:
        return res.strip("Lat: ").rsplit(' ',1)[0].split(" ")
    else:
        return skipLines(dev)

for cmd in commands:
    print("Command: ",cmd)
    dev.write(cmd)    
    
while True:
    raw_lat = (skipLines(dev))
    raw = dev.readline()
    res = raw.decode('utf-8').strip('\r\n').rsplit(' ',1)[0]
    if "Lon:" in res:
        raw_lon = res.strip("Lon: ").split(" ")
        lat = latlon(raw_lat)        
        lon = latlon(raw_lon)
        
        data = json.dumps({
            'time': dateTime(),
            'Lat': lat,
            'Lon': lon           
        })
        print(data)
      
    if 3.52 <= lat <= 3.543500 and 103.427400 <= lon <= 103.427900:         
        data = json.dumps({
            'header': 'Canseleri Tun Abdul Razak UMP',
            'subheader': 'Lorem ipsum',
            'description': 'Lorem Ipsum'
        })
        print('Canseleri')
        #mqttc.publish(START_TOPIC, data)
         
    if 3.53900 <= lat <= 3.543980 and 103.429096 <= lon <= 103.429300:      
        data = json.dumps({
            'header': 'Faculty of Electrical & Electronics Engineering',
            'subheader': 'Lorem ipsum',
            'description': 'Lorem Ipsum'
        })
        print("fkee")
       # mqttc.publish(START_TOPIC, data)
        
    if 3.537 <= lat <= 3.5436 and 103.429533 <= lon <= 103.431738:        
        data = json.dumps({
            'header': 'Fakulti Teknologi Kejuruteraan Mekanikal & Automatif',
            'subheader': 'Lorem ipsum',
            'description': 'Lorem Ipsum'
        })
        print("fkm")
        #mqttc.publish(START_TOPIC, data)
        
    if 3.536 <= lat <= 3.538 and 103.432870 <= lon <= 103.434297:        
        data = json.dumps({
            'header': 'Faculty of Manufacturing Engineering',
            'subheader': 'Lorem ipsum',
            'description': 'Lorem Ipsum'
        })
        #mqttc.publish(START_TOPIC, data)
        print(data)
        
    #print(data)

    dev.write(b'at!gpsloc?\r')
    time.sleep(1)
