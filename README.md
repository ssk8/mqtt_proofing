# mqtt proofing box thermostat

Thermostat for proofing box using wifi/mqtt instead of display and buttons. Written for MicroPython on a RPi Pico W.

BMP280 is overkill as it's only measuring temperature but it was easy and at hand

BME280 library apparently works with the BMP280 (no humidity sensor)

```sh
# to check temperature and setpoint:
alias proof="mosquitto_sub -v -h localhost -p 1883 -t 'pi_proofing/#'"
# to set temperature in degrees C (2 digit number)
alias mosq_set_temp="mosquitto_pub -r -t 'pi_proofing/set-temp' -m "
```
