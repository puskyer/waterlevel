# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import gc

from machine import Pin
from  wifisetup import do_connect
do_connect()

mqtt_server = '192.168.1.41'
mqtt_port = 1883
mqtt_user = 'mqttUser'
mqtt_password = ' '
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'bilgpump'
topic_pub = b'notification'
keepalive = 0
relay_pin = 3
led_pin = 2
off = 1
on = 0


last_message = 0
message_interval = 30
counter = 0


def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'bilgpump' and msg == b'on':
    turn_pump_on()
    led_on()
    print('ESP received On message')
  if topic == b'bilgpump' and msg == b'off':
    turn_pump_off()
    led_off()
    print('ESP received off message')
  if topic == b'bilgpump' and msg == b'restart':
    print('ESP received restart message')
    time.sleep(10)
    machine.reset()

def connect_and_subscribe():
  global client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password, topic_sub
  client = MQTTClient(client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password, keepalive)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker'% (mqtt_server))
  print('subscribed to %s topic' % (topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def blink_led():
  Pin(led_pin, Pin.OUT).value(on)
  time.sleep(1)
  Pin(led_pin, Pin.OUT).value(off)
  print('LED blinked!')

def led_on():
  Pin(led_pin, Pin.OUT).value(on)
  print('LED On!')

def led_off():
  Pin(led_pin, Pin.OUT).value(off)
  print('LED Off!')

def turn_pump_on():
  Pin(relay_pin, Pin.OUT).value(1)
  print('Pump On!')
  
def turn_pump_off():
  Pin(relay_pin, Pin.OUT).value(0)
  print('Pump Off!')

try:
  blink_led()
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello waiting for Pump action #%d' % counter
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
      #print ('publishing to topic %s' % (topic_pub))
      #print ('with message %s' % (msg))
      #print ('last_message is %s' % (last_message))
  except OSError as e:
    restart_and_reconnect()
