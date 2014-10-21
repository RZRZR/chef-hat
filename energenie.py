import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# The GPIO pins for the Energenie module
BIT1 = 26
BIT2 = 13
BIT3 = 21
BIT4 = 19
ON_OFF_KEY = 5
ENABLE = 6

GPIO.setup(BIT1, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BIT2, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BIT3, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BIT4, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(ON_OFF_KEY, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENABLE, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

# Codes for switching on and off the sockets
#        all     1       2       3       4
ON  = ['1011', '1111', '1110', '1101', '1100']
OFF = ['0011', '0111', '0110', '0101', '0100']

def change_plug_state(socket, on_or_off):
    state = on_or_off[socket][3] == '1'
    GPIO.output(BIT1, state)
    state = on_or_off[socket][2] == '1'
    GPIO.output(BIT2, state)
    state = on_or_off[socket][1] == '1'
    GPIO.output(BIT3, state)
    state = on_or_off[socket][0] == '1'
    GPIO.output(BIT4, state)
    sleep(0.1)
    GPIO.output(ENABLE, True)
    sleep(0.25)
    GPIO.output(ENABLE, False)

def switch_on(socket):
    change_plug_state(socket, ON)

def switch_off(socket):
    change_plug_state(socket, OFF)
