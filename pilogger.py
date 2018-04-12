import csv
import datetime
import pathlib

file = None
log_file = None

def logger_init():
    global file
    global log_file
    now = datetime.datetime.now()
    filename = "runlog_{0:%Y-%m-%d-%H-%M-%S}.txt".format(now)
    home = pathlib.Path.home().joinpath("Desktop", filename)
    print(home)
    file = open(home, "a")
    log_file = csv.writer(file)
    log_file.writerow(["TIMESTAMP", "EVENT_TYPE", "DATA"])

def logger_finish():
    file.close()

# Events:
#   MOTOR
#   RFID
#   ULTRASONIC
#   LIGHT
#   ENDRUN
def logger_write_motor(speed):
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("MOTOR")
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

def logger_write_light(color):
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("LIGHT")
    fields.append("{}".format(color))
    log_file.writerow(fields)

def logger_write_endrun(elapsed):
    now = datetime.datetime.now()
    fields = []
    fields.append("{:%Y-%m-%d %H:%M:%S.%f}".format(now))
    fields.append("ENDRUN")
    fields.append("{}".format(elapsed))
    log_file.writerow(fields)

