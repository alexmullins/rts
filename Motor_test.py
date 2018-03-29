#!/usr/bin/env python
# This code is an example for running a motor to a target position set by the encoder of another motor.
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import serial
import io

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
left_Motor = BP.PORT_D         #motor D is the left motor of the robot.
right_Motor = BP.PORT_A        #motor A is the right motor of the robot.

#initialize serial port for RFID
ser = serial.Serial('/dev/ttyS0')

#loop that i believe reads from the rfid with a timeout, would probably use this inside our route functions
def readRFID():
    with serial.Serial('/dev/ttyS0', 19200, timeout = 1) as ser:
        data = ""
        while len(data) < 12:                              #read until a 12 byte rfid id is read.
            data = ser.read(ser.inWaiting())
            print(data)
            time.sleep(0.1)
        return data                                        #return RFID value
    

def routeA():
    #drive until RFIDtag 11 is reached and turn left
	tag11 = 5400C9090296
	tag36 = 5400C9B34967
	tag43 = 700026EE77CF
    while True:
		driveForward()
        id = readRFID()
        if(id == tag11):
            break
    leftTurn()
    
    #drive until RFID tag 43 is reached and turn right
    while True:
        BP.set_motor_power(left_Motor, 20)
        BP.set_motor_power(right_Motor, 20)
        time.sleep(1)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.
        id = readRFID()
        if(id == tag43):
            break
    rightTurn()
    
    #drive until RFID tag 36 is reached and stop
    while True:
        BP.set_motor_power(left_Motor, 20)
        BP.set_motor_power(right_Motor, 20)
        time.sleep(1)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.
        id = readRFID()
        if(id == tag36):
            break
    BP.set_motor_power(left_Motor, 0)
    BP.set_motor_power(right_Motor, 0)


def rightTurn():
    t_end = time.time()+ 3
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 0)
        BP.set_motor_power(right_Motor, 20)
        time.sleep(1)
        
def leftTurn():
    t_end = time.time()+ 3
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 20)
        BP.set_motor_power(right_Motor, 0)
        time.sleep(1)
        
def driveForward():
    BP.set_motor_power(left_Motor, 20)
    BP.set_motor_power(right_Motor, 20)
    time.sleep(1)
    
def demoFunction():
    t_end = time.time() + 5 #run got 5 seconds
    try:
        while time.time() < t_end:
            driveForward()
        rightTurn()
        t_end = time.time() + 5
        while time.time() < t_end:
            driveForward()
        leftTurn()
        t_end = time.time()+ 5
        while time.time() < t_end:
            driveForward()
        BP.reset_all()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware
demoFunction()