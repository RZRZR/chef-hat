from glob import glob
import os
from time import sleep

def get_device_file():
    devices_path = '/sys/bus/w1/devices/'
    devices = glob(devices_path + '28*')
    if not devices:
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-therm')
    devices = glob(devices_path + '28*')
    device_file = devices[0] + '/w1_slave'
    return device_file

def take_temp():
    with open(device_file) as df:
        text = df.read()
    temp_data = text.split('\n')[1].split()[9]
    temp = float(temp_data[2:]) / 1000
    return temp

device_file = get_device_file()

def main():
    while True:
        print(take_temp())
        sleep(1)

if __name__ == '__main__':
    main()
