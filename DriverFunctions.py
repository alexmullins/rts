import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import serial
import io
import pilogger
#replace sensor-data printouts with write-out to log files

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.reset_all()
left_Motor = BP.PORT_D         #motor D is the left motor of the robot.
right_Motor = BP.PORT_A        #motor A is the right motor of the robot.
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
pilogger.logger_init()

def readRFID():
    with serial.Serial('/dev/ttyS0') as ser:
        data = None
        if((ser.inWaiting()) > 12):                     #check if there is any RFID data
            data = ser.read(14)
            id = data.decode("utf-8")
            time.sleep(.001)
            print(id)
            pilogger.logger_write_rfid(id)
            return id[1:13]                                        #return RFID value
        return

def leftTurn():
    t_end = time.time()+ 2
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 0)
        pilogger.logger_write_motor(0, 0)
        getUltraSonicData()
        BP.set_motor_power(right_Motor, 25)
        pilogger.logger_write_motor(1, 25)
        time.sleep(1)
        
def rightTurn():
    t_end = time.time()+ 2
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 25)
        pilogger.logger_write_motor(0, 25)
        BP.set_motor_power(right_Motor, 0)
        pilogger.logger_write_motor(1, 0)
        time.sleep(1)
        
def driveForward():
    BP.set_motor_power(left_Motor, 16)
    pilogger.logger_write_motor(0, 16)
    BP.set_motor_power(right_Motor, 16)
    pilogger.logger_write_motor(1, 16)
    time.sleep(0.2)
def driveForwardFast():
    BP.set_motor_power(left_Motor, 20)
    pilogger.logger_write_motor(0, 20)
    BP.set_motor_power(right_Motor, 20)
    pilogger.logger_write_motor(1, 20)
    time.sleep(0.2)
def stop():
    BP.set_motor_power(left_Motor, 0)
    pilogger.logger_write_motor(0, 0)
    BP.set_motor_power(right_Motor, 0)
    pilogger.logger_write_motor(1, 0)
    
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
        pilogger.logger_write_error(error)
def isObstacle(distance):
    time.sleep(0.05)
    print(distance)
    pilogger.logger_write_ultrasonic(distance)
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
        pilogger.logger_write_light(value)
        pilogger.logger_write_light(secondValue)
        getInLine(value, secondValue)
        getUltraSonicData()
    except brickpi3.SensorError as error:
        print(error)
        pilogger.logger_write_error(error)
def getInLine(leftSensor, rightSensor):
    if(rightSensor - leftSensor > 300):
        driftRight()
    if(rightSensor - leftSensor < -250):
        driftLeft()
def driftLeft():
    t_end = time.time()+ .5
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 0)
        pilogger.logger_write_motor(0, 0)
        BP.set_motor_power(right_Motor, 16)
        pilogger.logger_write_motor(1, 16)
        time.sleep(0.01)
        
def driftRight():
    t_end = time.time()+ .5
    while time.time() < t_end:
        BP.set_motor_power(left_Motor, 16)
        pilogger.logger_write_motor(0, 16)
        BP.set_motor_power(right_Motor, 0)
        pilogger.logger_write_motor(1, 0)
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