# This code is an example for running a motor to a target position set by the encoder of another motor.
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import serial
import io
from DriverFunctions import *
#initialize serial port for RFID
ser = serial.Serial('/dev/ttyS0')

#loop that i believe reads from the rfid with a timeout, would probably use this inside our route functions
def routeA():
    tag11 = "5400C9090296"
    tag36 = "5400C9B34967"
    tag35 = "700026F241E5"
    
    try:
        #drive until RFIDtag 11 is reached and turn left
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag11):
                stop()
                print("Turning Left (South) at Tag 11")
                break
        t_end = time.time() + .6 #run got 5 seconds
        while time.time() < t_end:
            driveForward()
        leftTurn()
        
        #drive until detecting object or RFID tag 43 is reached and turn right
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag35):
                stop()
                print("Turning right(West) at Tag 35")
                break
        t_end = time.time() + .75
        while time.time() < t_end:
            driveForward()
        rightTurn()
        
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForwardFast()
            getLightSensors()
            id = readRFID()
            if(id == tag36):
                t_end = time.time() + 2
                while time.time() < t_end:
                    driveForward()
                print("Reached destination at tag 36")
                stop()
                BP.reset_all() 
                break
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()
def routeB():
    tag11 = "5400C9090296"
    tag34 = "790072A348E0"
    tag8 =  "5400C96AC037"
    tag42 = "7900726AF998"
    tag15 = "5400CA3903A4"
    try:
        #drive until RFIDtag 11 is reached and turn left
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForwardFast()
            getLightSensors()
            id = readRFID()
            if(id == tag8):
                stop()
                print("Turning right(South) at Tag 8")
                break
        t_end = time.time() + .6 #run got 5 seconds
        while time.time() < t_end:
            driveForward()
        rightTurn()
        
        #drive until RFID tag 43 is reached and turn right
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag34):
                stop()
                print("Turning left(East) at Tag 34")
                break
        t_end = time.time() + 1
        while time.time() < t_end:
            driveForward()
        leftTurn()
        
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForwardFast()
            getLightSensors()
            id = readRFID()
            if(id == tag42):
                print("Turning left(North) at Tag 42")
                t_end = time.time() + .75
                while time.time() < t_end:
                    driveForward()
                leftTurn()
                break
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForwardFast()
            getLightSensors()
            id = readRFID()
            if(id == tag15):
                print("Turning right(East) at Tag 15")
                t_end = time.time() + .45
                while time.time() < t_end:
                    driveForward()
                rightTurn()
                break
            
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForwardFast()
            getLightSensors()
            id = readRFID()
            if(id == tag11):
                t_end = time.time() + 6.5
                while time.time() < t_end:
                    getUltraSonicData()
                    time.sleep(.005)
                    driveForward()
                    getLightSensors()
                stop()
                print("Reached destination at tag 11")
                BP.reset_all() 
                break
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all() 
def routeC():
    tag36 = "5400C9B34967"
    tag48 = "5400CA7D6586"
    tag58 = "70002710480F"
    tag31 = "790072AF76D2"
    tag23 = "700027321B7E"
    try:
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag36):
                print("Turning right(South) at Tag 36")
                t_end = time.time() + .45
                while time.time() < t_end:
                    driveForward()
                    stop()
                break
        rightTurn()
        
        #drive until RFID tag 43 is reached and turn right
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag48):
                print("Turning left(East) at Tag 48")
                t_end = time.time() + .7
                while time.time() < t_end:
                    driveForward()
                    stop()
                break
        leftTurn()
        
        #drive until RFID tag 36 is reached and stop
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag58):
                print("turning left(North) at tag 58")
                t_end = time.time() + 1
                while time.time() < t_end:
                    driveForward()
                    stop()
                break
        leftTurn()
        
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            getUltraSonicData()
            id = readRFID()
            if(id == tag31):
                print("Turning left(West) at Tag 31")
                t_end = time.time() + .75
                while time.time() < t_end:
                    driveForward()
                    stop()
                break
        leftTurn()
        
        while True:
                driveForward()
                getLightSensors()
                id = readRFID()
                if(id == tag23):
                    print("reached destination at tag 23")
                    t_end = time.time() + .8
                    while time.time() < t_end:
                        driveForward()
                        stop()
                    break
        stop()
        BP.reset_all() 
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()  
def routeD():
    tag32 = "5400CA681FE9"
    tag38 = "7000272D6E14"
    tag29 = "700026FC3993"
    tag26 = "7000270DEAB0"
    tag63 = "7000271A4F02"
    try:
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag32):
               print("Turning left(East) at Tag 32")
               t_end = time.time() + .5
               while time.time() < t_end:
                   driveForward()
                   stop()
               break
        leftTurn()
            
        #drive until RFID tag 43 is reached and turn right
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForwardFast()
            getLightSensors()
            id = readRFID()
            if(id == tag38):
                print("Turning left(North) at Tag 38")
                t_end = time.time() + .5
                while time.time() < t_end:
                    driveForward()
                    stop()
                break   
        leftTurn()
            
        #drive until RFID tag 36 is reached and stop
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag29):
                print("Turning right(East) at Tag 29")
                t_end = time.time() + .3
                while time.time() < t_end:
                    driveForward()
                    stop()
                break
        rightTurn()
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag26):
                print("Turning right(South) at Tag 26")
                t_end = time.time() + .4
                while time.time() < t_end:
                    driveForward()
                    stop()
                break
        rightTurn()
        
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForwardFast()
            getLightSensors()
            id = readRFID()
            getUltraSonicData()
            if(id == tag63):
                t_end = time.time() + 2
                while time.time() < t_end:
                    driveForward()
                    stop()
                break
        print("Reached destination at tag 63")
        stop()
        BP.reset_all() 
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()
#BP.reset_all()
routeA()
#stop()