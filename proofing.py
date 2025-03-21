import paho.mqtt.client as mqtt
import datetime
import json

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pi_proofing")

def on_message(client, userdata, msg):
    msg = json.loads(str(msg.payload)[2:-1])
    print(f'{datetime.datetime.now().strftime("%a %H:%M:%S")} temp:{msg["temperature"]:.1f}C set:{msg["set_temp"]}C heater is {msg["heater"]*"on" or "off"}')

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.106", 1883, 60)

try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    print("\nbye")
