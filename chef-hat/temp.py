from glob import glob
from time import sleep

device_location = '/sys/bus/w1/devices/28*'
device_dir = glob(device_location)[0]
device_file = device_dir + '/w1_slave'


def take_temp():
    with open(device_file) as f:
        text = f.read()
    temp_data = text.split('\n')[1].split()[9]
    temp = float(temp_data[2:]) / 1000
    return temp

def main():
    while True:
        print(take_temp())
        sleep(1)

if __name__ == '__main__':
    main()
