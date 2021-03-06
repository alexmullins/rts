import csv
import datetime
import pathlib

start = None
file = None
log_file = None

def logger_init():
    global file
    global log_file
    global start
    now = datetime.datetime.now()
    start = now
    filename = "runlog_{0:%Y-%m-%d-%H-%M-%S}.txt".format(now)
    home = pathlib.Path.home().joinpath("Desktop", filename)
    print("Creatd log file: {}", home)
    file = open(home, "a")
    log_file = csv.writer(file)
    log_file.writerow(["TIMESTAMP", "EVENT_TYPE", "DATA"])

# Events:
#   MOTOR
#   RFID
#   ULTRASONIC
#   LIGHT
#   ERROR
#   ENDRUN
def logger_write_motor(motor, speed):
    m = "LEFT"
    if motor == 1:
        m = "RIGHT"
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("MOTOR-{}".format(m))
    fields.append("{}".format(speed))
    log_file.writerow(fields)

def logger_write_rfid(rfid_id):
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("RFID")
    fields.append("{}".format(rfid_id))
    log_file.writerow(fields)

def logger_write_ultrasonic(distance):
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("ULTRASONIC")
    fields.append("{}".format(distance))
    log_file.writerow(fields)

def logger_write_light(light, color):
    l = "FIRST"
    if light == 1:
        l = "SECOND"
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("LIGHT-{}".format(l))
    fields.append("{}".format(color))
    log_file.writerow(fields)

def logger_write_error(err):
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("LIGHT")
    fields.append("{}".format(err))
    log_file.writerow(fields)

def logger_write_endrun():
    now = datetime.datetime.now()
    elapsed = now - start
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("ENDRUN")
    fields.append("{}".format(elapsed))
    log_file.writerow(fields)
    file.close()

