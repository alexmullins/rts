# This code is an example for running a motor to a target position set by the encoder of another motor.
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import serial
import io

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.reset_all()
left_Motor = BP.PORT_D         #motor D is the left motor of the robot.
right_Motor = BP.PORT_A        #motor A is the right motor of the robot.
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)

#initialize serial port for RFID
ser = serial.Serial('/dev/ttyS0')

#loop that i believe reads from the rfid with a timeout, would probably use this inside our route functions
def readRFID():
    with serial.Serial('/dev/ttyS0') as ser:
        data = None
        if((ser.inWaiting()) > 12):                     #check if there is any RFID data
            data = ser.read(14)
            id = data.decode("utf-8")
            time.sleep(.001)
            print(id)
            return id[1:13]                                        #return RFID value
        return

def leftTurn():
    t_end = time.time()+ 2
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 0)
        getUltraSonicData()
        BP.set_motor_power(right_Motor, 25)
        time.sleep(1)
        
def rightTurn():
    t_end = time.time()+ 2
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 25)
        BP.set_motor_power(right_Motor, 0)
        time.sleep(1)
        
def driveForward():
    BP.set_motor_power(left_Motor, 16)
    BP.set_motor_power(right_Motor, 16)
    time.sleep(0.2)
def driveForwardFast():
    BP.set_motor_power(left_Motor, 20)
    BP.set_motor_power(right_Motor, 20)
    time.sleep(0.2)
def stop():
    BP.set_motor_power(left_Motor, 0)
    BP.set_motor_power(right_Motor, 0)
    
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
def getUltraSonicData():
    time.sleep(.01)
    try:
        value = BP.get_sensor(BP.PORT_1)
        isObstacle(value)                        # print the distance in CM
    except brickpi3.SensorError as error:
        print(error)
def isObstacle(distance):
    time.sleep(0.05)
    print(distance)
    if(distance < 15):
        while True:
            stop()
            value = BP.get_sensor(BP.PORT_1)
            if(value > 15):
                break
            time.sleep(0.2)
    return
def getLightSensors():
    try:
        time.sleep(0.02)
        value = BP.get_sensor(BP.PORT_3)
        secondValue = BP.get_sensor(BP.PORT_2)
        print(value, secondValue)
        getInLine(value, secondValue)
        getUltraSonicData()
    except brickpi3.SensorError as error:
        print(error)
def getInLine(leftSensor, rightSensor):
    if(rightSensor - leftSensor > 300):
        driftRight()
    if(rightSensor - leftSensor < -250):
        driftLeft()
def driftLeft():
    t_end = time.time()+ .5
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 0)
        BP.set_motor_power(right_Motor, 16)
        time.sleep(0.01)
        
def driftRight():
    t_end = time.time()+ .5
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 16)
        BP.set_motor_power(right_Motor, 0)
        time.sleep(0.01)
def testSensors():
    t_end = time.time()+ 20
    while time.time() < t_end:
        getUltraSonicData()
        try:
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID
        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            BP.reset_all()
    stop()
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
                break
        t_end = time.time() + .6 #run got 5 seconds
        while time.time() < t_end:
            driveForward()
        leftTurn()
        
        #drive until RFID tag 43 is reached and turn right
        while True:
            getUltraSonicData()
            time.sleep(.005)
            driveForward()
            getLightSensors()
            id = readRFID()
            if(id == tag35):
                stop()
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
        stop()
        BP.reset_all() 
    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()
#BP.reset_all()
routeB()
#stop()