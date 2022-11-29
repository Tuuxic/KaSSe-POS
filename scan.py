import atexit
from time import sleep
import serial

SCANNER_PATH = '/dev/ttyUSB0'
BAUD = 115200

NUL = 0x00
CMD = 0x01
STX = 0x02
ETX = 0x03


def run(callback):
    ser = serial.Serial(SCANNER_PATH, BAUD, timeout=0, rtscts=True, dsrdtr=True)

    atexit.register(ser.close)

    line = b''

    while True:
        if ser.inWaiting() > 0:
            reading = ser.read(ser.inWaiting())
            line += reading
            if b'\n' in line:
                line = line.partition(b'\n')[0]
                callback(line[:-3].decode())
                line = b''
        sleep(0.01)


if __name__ == '__main__':
    run(print)
