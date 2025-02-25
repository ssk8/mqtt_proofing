import paho.mqtt.client as mqtt
import datetime

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("pi_proofing")

def on_message(client, userdata, msg):
    print(f'{datetime.datetime.now().strftime("%a %H:%M:%S")} {str(msg.payload)[2:-1]}')

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("192.168.1.106", 1883, 60)

try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    print("\nbye")
