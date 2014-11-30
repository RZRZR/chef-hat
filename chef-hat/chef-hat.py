from energenie import switch_on, switch_off
from time import sleep
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

desired_temp = 21


def main():
    sensor = W1ThermSensor()
    while True:
        temp = sensor.get_temperature()
        print(temp)
        if temp < desired_temp:
            switch_on()
        else:
            switch_off()
        sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
