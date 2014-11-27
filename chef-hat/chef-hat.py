from energenie import switch_on, switch_off
import lcdtest as lcd
from time import sleep
import RPi.GPIO as GPIO

def main():
    lcd.init()
    lcd.write("Sous", 1)
    lcd.write("Vide", 2)
    sleep(2)
    lcd.write("Turning", 1)
    lcd.write("on", 2)
    sleep(2)
    switch_on(0)
    lcd.write("Turning", 1)
    lcd.write("off", 2)
    sleep(2)
    switch_off(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
