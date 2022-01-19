from typing import Counter
from gpiozero import Button
from time import sleep
import datetime
import sys

raingauge = Button(6)
tipped = 0
sensorsize = 0.2794

today = datetime.date.today()
abbrdate = today.strftime("%b-%d-%Y")
filename = f"{abbrdate}_RainGauge"

def bucket_tip():
    global tipped
    tipped += 1

raingauge.when_pressed = bucket_tip

while True:
    sleep(10)
    time = datetime.datetime.now()
    timecheck = datetime.datetime.now().strftime('%H:%M:%S')
    mmrain = sensorsize * tipped
    with open(f"/home/pi/weather/current/RainSensor/{filename}.txt", "a+") as logfile:
        logfile.seek(0)
        data = logfile.read(100)
        if len(data) > 0 :
            logfile.write("\n")
        logfile.write(f'{time.hour}:{time.minute}:{time.second}      Millimeters of Rain: {mmrain}')
    if timecheck >= '23:59:45':
        sys.exit()
