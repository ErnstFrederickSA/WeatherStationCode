#!/bin/bash
python3 BME280ReadV2.py &
python3 WindSensorRead.py &
python3 RainGaugeRead.py & 