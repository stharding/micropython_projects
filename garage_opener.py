# garage_opener.py

from machine import Pin
from network import WLAN, STA_IF
from time import sleep

from umqtt import simple


pin = Pin(5, Pin.OUT)


def do_connect():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('wifi-ssid', 'wifi-password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def handle_garage_button(topic, msg):
    print(topic, msg)
    pin.on()
    mqtt_client.publish(b'garage_btn/sts', b'ON')
    sleep(1)
    pin.off()
    mqtt_client.publish(b'garage_btn/sts', b'OFF')


do_connect()

mqtt_client = simple.MQTTClient('garage_opener', '192.168.0.1')
mqtt_client.set_callback(handle_garage_button)
mqtt_client.connect()
print('connected to mqtt broker!')
mqtt_client.subscribe('garage_btn/cmd')


while True:
    mqtt_client.wait_msg()
