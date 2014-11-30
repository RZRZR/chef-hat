from energenie import switch_on, switch_off
from time import sleep

while True:
    print("switching on...")
    switch_on()
    sleep(2)
    print("switching off...")
    switch_off()
    sleep(2)
