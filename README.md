# mqtt proofing box thermostat

Thermostat for proofing box using wifi/mqtt instead of display and buttons. Written for MicroPython on a RPi Pico W.

BMP280 is overkill as it's only measuring temperature but it was easy and at hand

BME280 library apparently works with the BMP280 (no humidity sensor)

use proofing.py to monitor temperature, setpoint, heater status

```sh
# to check from command line:
alias proof="mosquitto_sub -v -h localhost -p 1883 -t 'pi_proofing/#'"
# to set temperature in degrees C (2 digit number)
alias mosq_set_temp="mosquitto_pub -r -t 'pi_proofing/set-temp' -m "
```
<img src=https://raw.githubusercontent.com/ssk8/mqtt_proofing/2c79a1b277538c0e45221fb4e355f7bea11ba194/proofing.jpg  width="600"/>
