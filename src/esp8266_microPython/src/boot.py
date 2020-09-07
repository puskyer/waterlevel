# This file is executed on every boot (including wake-boot from deepsleep)

import uos, machine
import gc
import esp
import time
from umqttsimple import MQTTClient
import ubinascii
import micropython
import network
import webrepl

#uos.dupterm(None, 1) # disable REPL on UART(0)
esp.osdebug(None)
gc.collect()
webrepl.start()    # start webrepl

org_freq = machine.freq()          # get the current frequency of the CPU
print('Machine freq was %s' % (org_freq))
machine.freq(160000000)            # set the CPU frequency to 160 MHz
print('Machine freq set to %s' % (160000000))

#from  wifisetup import do_connect
#do_connect()

#ssid = ''
#ssid_password = ''
ssid = ''
ssid_password = ''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, ssid_password)

while station.isconnected() == False:
    #pass
    time.sleep_ms(500)
    print('Connecting')
print('Connection successful')
print(station.ifconfig())

