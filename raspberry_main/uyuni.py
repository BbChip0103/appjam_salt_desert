#-*- coding:utf-8 -*-
# written in python3

import RPi.GPIO as GPIO
import time
from twilio.rest import Client
import smbus
import requests
import threading

import config

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(26, GPIO.OUT)

i2c = smbus.SMBus(1) # sudo i2cdetect -y (number)
URL = config.SERVER_URL

account_sid = config.TWILIO_CONFIG['account_sid']
auth_token  = config.TWILIO_CONFIG['auth_token']
client = Client(account_sid, auth_token)

def OnSwitchPressed() :
    while True:
        input_value = GPIO.input(21)
        print(input_value)

        if input_value == False:
            GPIO.output(26, True)
            message = client.messages.create(
                to="+821073632379",
                from_="+17604528298",
                body="1번 지점 구조요청 신호 발생!!!")
            print(message)

        else:
            GPIO.output(26, False)

        time.sleep(0.5)

def SendWaterLevel() :
    while True :
        water_level = i2c.read_byte(0x04)
        print(water_level)

        data = {'water_level': water_level}
        res = requests.post(url=URL, data=data)
        time.sleep(10)

try:
    threading._start_new_thread(OnSwitchPressed, ())
    threading._start_new_thread(SendWaterLevel, ())

    while True :
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
    print("press key interrupt")
