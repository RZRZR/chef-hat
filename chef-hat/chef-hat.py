from energenie import switch_on, switch_off
from time import sleep
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import lcd

desired_temp = 21


def main():
    sensor = W1ThermSensor()
    lcd.init()
    while True:
        temp = sensor.get_temperature()
        print(temp)
        lcd.write("%s" % temp)
        if temp < desired_temp:
            switch_on()
            print("on")
            lcd.write("on", 2)
        else:
            switch_off()
            print("off")
            lcd.write("off", 2)
        sleep(5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
