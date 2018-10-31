#!/usr/bin/env python

"""test-imu-plot.py: Ask multiwii for raw IMU and plot it using pyqtgraph."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2016 Altax.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

from pymultiwii import MultiWii
import time, math

#board = MultiWii("/dev/tty.usbserial-A801WZA1")


def getTheta():
    global data1, board
    board.getData(MultiWii.RAW_IMU)
    t = float(board.rawIMU['timestamp'])
    ax = board.rawIMU['ax']
    ay = board.rawIMU['ay']
    magnitude = math.sqrt(ax*ax + ay*ay)

    theta = math.degrees(math.atan2(ay/magnitude, ax/magnitude))
    if theta < 0:
        theta = theta + 360
    return theta

def getRotationalV():
    global data1, board
    board.getData(MultiWii.RAW_IMU)
    
    gz = board.rawIMU['gz']
    return gz

 
def get_dtheta_dt():
    global data1, board
    board.getData(MultiWii.RAW_IMU)
    t1 = time.time()
    ax = board.rawIMU['ax']
    ay = board.rawIMU['ay']
    magnitude = math.sqrt(ax*ax + ay*ay)
    theta1 = math.degrees(math.atan2(ay/magnitude, ax/magnitude))

    board.getData(MultiWii.RAW_IMU)
    t2 = time.time()
    ax = board.rawIMU['ax']
    ay = board.rawIMU['ay']
    magnitude = math.sqrt(ax*ax + ay*ay)
    theta2 = math.degrees(math.atan2(ay/magnitude, ax/magnitude))

    return (theta2 - theta1) / (t2 - t1)

def getTime():
    global data1, board
    board.getData(MultiWii.RAW_IMU)
    t = float(board.rawIMU['timestamp'])
    return t

def getClockRate():
    t1 = time.time()
    for i in range(100):
        getTheta()
    
    print((time.time() - t1)/ 100.)

def getLateralVelocity():
    global data1, board
    board.getData(MultiWii.RAW_IMU)
    


if __name__ == '__main__':
    global data1, board
    board = MultiWii("/dev/tty.SLAB_USBtoUART")
    t0 = time.time()
    deltaT = 0
    velocity =0
    position = 0
    for i in range(1000):
        board.getData(MultiWii.RAW_IMU)
        velocity += board.rawIMU['az'] * (time.time() - t0)
        position += velocity * (time.time() - t0)
        t0 = time.time()
        if i % 10 == 0:
            print("acceleration: ", board.rawIMU['az'], "velocity: " ,velocity, "position ", position)
    #print(getTheta(), "degrees")
    getTheta()
    #print("rotationalV",get_dtheta_dt())
    #print(getTime())

   
        

