#!/bin/env python

import serial
import paho.mqtt.client as mqtt
import time
import json

def getValues():
        with serial.Serial("/dev/ttyUSB0", baudrate=9600, parity=serial.PARITY_EVEN, bytesize=serial.SEVENBITS) as ser:
                l = ser.read(1000).split('\r\n')
        return l[l.index('/EBZ5DD32R10DTB_107')+4:l.index('/EBZ5DD32R10DTB_107')+15]
        
def splitValues(l):
        values = {}
        for i in l:
                sp = i.split('(')
                tmp_name = 'ebz_'+sp[0].split(':')[1].split('*')[0]
                tmp_value = sp[1].split('*')[0]
                values[tmp_name] = float(tmp_value)
        return values
        
def sendmqtt(val, channel):
        client = mqtt.Client()
        client.connect("127.0.0.1", 1883, 60)
        client.publish(channel, payload= json.dumps(val))


if __name__ == "__main__":
        print('Start loop')
        while True:
                sendmqtt(splitValues(getValues()),'power_meter')
                print('Sent value')
                time.sleep(30)
