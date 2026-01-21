#!/usr/bin/python3


import paho.mqtt.client as mqtt
import json
import datetime

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connection: {reason_code}")
    client.subscribe("pi_proofing")

def on_message(client, userdata, msg):
    dt = datetime.datetime.now().strftime("%a %H:%M:%S") 
    pl = json.loads(msg.payload)
    print(f"{datetime.datetime.now().strftime('%a %H:%M:%S')} temp: {pl['temperature']}°C, heater is {('off', 'on')[pl['heater']]}, set temp:{pl['set_temp']}°C, humidity: {pl['humidity']}%")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.106", 1883, 60)

try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    print("\nbye")
