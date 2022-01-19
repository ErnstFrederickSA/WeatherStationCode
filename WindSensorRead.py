#Will collect data every ten seconds from anemometer
#Need to add wind vane code
from gpiozero import Button
from gpiozero import MCP3008
import datetime
import time
import sys
import math

cminkm = 100000
secondsinhour = 3600

#Anemometer Specs
radius_cm = 9.0
adjustment = 1.18

#Wind vane
windvane = MCP3008(channel=0)
count = 0
volts = {
    0.4 : 0.0,
    1.4 : 22.5,
    1.2 : 45.0,
    2.8 : 67.5,
    2.7 : 90.0,
    2.9 : 112.5,
    2.2 : 135.0,
    2.5 : 157.5,
    1.8 : 180.0,
    2.0 : 202.5,
    0.7 : 225.0,
    0.8 : 247.5,
    0.1 : 270.0,
    0.3 : 292.5,
    0.2 : 315.0,
    0.6 : 337.5
}

today = datetime.date.today()
abbrdate = today.strftime("%b-%d-%Y")
filename = f"{abbrdate}_WindSensors"

speedcount = 0
wind_interval = 10

def spin():
    global speedcount
    speedcount = speedcount + 1

def reset_wind():
    global speedcount
    speedcount = 0

def windspeedcalc(time_sec):
    global speedcount
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = speedcount / 2.0
    dist_km = (circumference_cm * rotations) / cminkm
    kmpersec = dist_km / time_sec
    kmperhour = kmpersec * secondsinhour
    return kmperhour * adjustment

def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

#def windvanevalue(length=10):
#    data = []
#    start_time = time.time()
#    while time.time() - start_time <= length:
#        wind = round(windvane.value * 3.3, 1)
#        if not wind in volts:
#            pass
#        else:
#            data.append(volts[wind])
#    return get_average(data)

def windvanevalue():
    sec_to_run = 10
    data = []
    exec_end_time = datetime.datetime.now() +  datetime.timedelta(seconds=sec_to_run)  
    while True: 
        if datetime.datetime.now() >= exec_end_time: 
            break
        wind = round(windvane.value * 3.3, 1)
        if not wind in volts:
            pass
        else:
            data.append(volts[wind])
    return get_average(data)

speedsensor = Button(5)
speedsensor.when_pressed = spin

while True:
    reset_wind()
    time = datetime.datetime.now()
    timecheck = datetime.datetime.now().strftime('%H:%M:%S')
    with open(f"/home/pi/weather/current/WindSensors/{filename}.txt", "a+") as logfile:
        logfile.seek(0)
        data = logfile.read(100)
        if len(data) > 0 :
            logfile.write("\n")
        logfile.write(f'{time.hour}:{time.minute}:{time.second}      Wind Direction: {windvanevalue()} | Wind Speed: {windspeedcalc(wind_interval)} km/h')
    if timecheck >= '23:59:45':
        sys.exit()
