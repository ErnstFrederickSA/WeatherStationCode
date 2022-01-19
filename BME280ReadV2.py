#This will run every day and repeat 10 seconds
import bme280
import smbus2
from time import sleep
import datetime
import sys

port = 1
address = 0x77 
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

today = datetime.date.today()
abbrdate = today.strftime("%b-%d-%Y")
filename = f"{abbrdate}_BME280"

while True:
    sleep(10)
    time = datetime.datetime.now()
    timecheck = datetime.datetime.now().strftime('%H:%M:%S')
    bme280_data = bme280.sample(bus,address)
    humidity  = bme280_data.humidity
    pressure  = bme280_data.pressure
    ambient_temperature = bme280_data.temperature
    with open(f"/home/pi/weather/current/BME280/{filename}.txt", "a+") as logfile:
        logfile.seek(0)
        data = logfile.read(100)
        if len(data) > 0 :
            logfile.write("\n")
        logfile.write(f'{time.hour}:{time.minute}:{time.second}      Humidity: {humidity} | Pressure: {pressure} | Ambient Temperature: {ambient_temperature}')
    if timecheck >= '23:59:45':
        sys.exit()
