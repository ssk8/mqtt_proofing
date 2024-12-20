from machine import Pin, I2C
from time import sleep
import network
from umqtt.simple import MQTTClient
import config
import lib.BME280 as BME280

topic = "pi_proofing"
sleep_time = 5
heater_pin = 22

MQTT_TOPIC_TEMPERATURE = topic + '/temperature'
MQTT_TOPIC_PRESSURE = topic + '/pressure'
MQTT_TOPIC_HUMIDITY = topic + '/humidity'
MQTT_TOPIC_SET = topic + '/set-temp'

MQTT_SERVER = config.mqtt_server
MQTT_PORT = 1883
MQTT_USER = config.mqtt_username
MQTT_PASSWORD = config.mqtt_password
MQTT_CLIENT_ID = b"picow_proof"
MQTT_KEEPALIVE = 7200


heater = Pin(heater_pin, Pin.OUT, value=1)
set_temp = None

i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=10000)

bme = BME280.BME280(i2c=i2c, addr=0x76)

def get_sensor_readings():
    temp = bme.temperature[:-1]
    hum = bme.humidity[:-1]
    pres = bme.pressure[:-3]
    return temp, hum, pres

def initialize_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(ssid, password)

    connection_timeout = 10
    for _ in range(connection_timeout):
        if wlan.status() >= 3:
            break
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    if wlan.status() != 3:
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

def connect_mqtt():
    try:
        client = MQTTClient(client_id=MQTT_CLIENT_ID,
                            server=MQTT_SERVER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=MQTT_KEEPALIVE,)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise 

def change_set_temp(topic, message):
    global set_temp
    set_temp = int(str(message)[2:4])
    print(f'new set_temp = {set_temp}')

try:
    if not initialize_wifi(config.wifi_ssid, config.wifi_password):
        print('Error connecting to the network... exiting program')
    else:
        client = connect_mqtt()
        client.set_callback(change_set_temp)
        client.subscribe(MQTT_TOPIC_SET)
        while True:
            client.check_msg()
            temperature, humidity, pressure = [float(m) for m in get_sensor_readings()]
            if set_temp:
                if temperature < set_temp:
                    heater.value(0)
                else:
                    heater.value(1)
            msg = f'temp:{temperature:.1f}C (set:{set_temp if set_temp else "--"}C), heater({heater.value()*'off),' or 'on), '} p:{round(pressure)}hPa, h:{round(humidity)}%'
            client.publish(topic, msg)
            print(msg)
            sleep(sleep_time)

except Exception as e:
    heater.value(1)
    print('Error:', e)
