from subprocess import *
import time, sys, os, subprocess, threading
import thread
from datetime import datetime
import glob
from energenie import switch_on, switch_off
import RPi.GPIO as GPIO

os.system('modprobe w1-gpio gpiopin=12')
os.system('modprobe w1-therm')

# Define GPIO mapping
hotter_btn = 2
colder_btn = 3
start_btn = 4

GPIO.setup(hotter_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(colder_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(start_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Where to find the temp sensor (don't change)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

target_temp = 55.00

# This reads the one wire sensor file and converts it to degrees C (to 2 decimal places)
def take_temp():
    file = device_file
    tfile = open(file)
    text = tfile.read()
    tfile.close()
    temprdata = text.split("\n")[1].split(" ")[9]
        # The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
    temperature = float(temprdata[2:])
        # Put the decimal point in the right place and display it.
    temperature = temperature / 1000
    return temperature

# This sets up the data to be displayed on the LCD screen
def oled_info(temperature, target_temp, heater):
    # Turning the temperature and target into strings and assigning error messages
    if temperature:
        temp_string = "{:.2f}".format(temperature)
    else:
        temp_string = "--.--"
    target_string = "{:.1f}".format(target_temp)

    if heater == 1:
        heater_info = "ON "
    if heater == 0:
        heater_info = "OFF"
    print "Target %s --- %s --- Temp %s" %(target_string, heater_info, temp_string)

# This is called only when the hotter Target Temp button is hit
def hotter_target(hotter_btn):
    global target_temp
    target_temp = target_temp + 1
    print "TARGET TEMP UPDATED:   %d" %target_temp
    return target_temp

# This is called only when the colder Target Temp button is hit
def colder_target(colder_btn):
    global target_temp
    target_temp = target_temp - 1
    print "TARGET TEMP UPDATED:   %d" %target_temp
    return target_temp

# This is decides if the energenie socket (i.e. the heating element) should be on or off
def slowcooker(temperature, target_temp):
    if temperature < target_temp:
        switch_on(1) # turn on the energenie socket
        heater = 1
    else:
        switch_off(1) # turn off the energenie socket
        heater = 0
    return heater

def main():
    while 1:
        try:
            temperature = take_temp()
            slowcooker(temperature, target_temp)
            heater = slowcooker(temperature, target_temp)
            thread.start_new_thread(oled_info, (temperature, target_temp, heater) )
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit(0)

# Call backs on the GPIO
GPIO.add_event_detect(hotter_btn, GPIO.RISING, callback=hotter_target, bouncetime=1000)
GPIO.add_event_detect(colder_btn, GPIO.RISING, callback=colder_target, bouncetime=1000)


if __name__=="__main__":
    print "Hey Rachel!"
    main()

