from energenie import switch_on, switch_off
from time import sleep
import RPi.GPIO as GPIO
from temp import take_temp

desired_temp = 21

def main():
    while True:
        temp = take_temp()
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
