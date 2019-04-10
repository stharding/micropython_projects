# garage_opener.py

from machine import Pin
from time import sleep

# from library installed by: upip.install('micropython-umqtt.simple')
from umqtt import simple

# from my common module
from common import connect_to_wifi

MQTT_BROKER = '192.168.0.1'


def main():
    # pin labeled '01' on my esp8266
    pin = Pin(5, Pin.OUT)

    def handle_garage_button(topic, msg):
        print(topic, msg)
        pin.on()
        mqtt_client.publish(b'garage_btn/sts', b'ON')
        sleep(1)
        pin.off()
        mqtt_client.publish(b'garage_btn/sts', b'OFF')


    connect_to_wifi('wifi-ssid', 'wifi-password')

    mqtt_client = simple.MQTTClient('garage_opener', MQTT_BROKER)
    mqtt_client.set_callback(handle_garage_button)
    mqtt_client.connect()
    print('connected to mqtt broker!')
    mqtt_client.subscribe('garage_btn/cmd')


    while True:
        mqtt_client.wait_msg()


main()
