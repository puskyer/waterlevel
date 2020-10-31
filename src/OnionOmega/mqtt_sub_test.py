#!/usr/bin/python
import paho.mqtt.client as mqtt
import time,logging
from OmegaExpansion import onionI2C
import sys

broker="192.168.1.41"

topic ="OnionOmega/notification"
topic1="OnionOmega/info"
port=1883
QOS=1
delay=5
client_id="OnionOmega"
mqttVer="MQTTv311"
username ="mqttUser"
password ="MqttPass"

i2c = onionI2C.OnionI2C(0)
# set the i2c verbosity
i2c.setVerbosity(1)
i2c_addr = 0x0
i2c_devAddr = 0x08

readi2c_HB = b'0x0'      # this is the Low mark for water level
readi2c_LB = b'0x0'      # this is the High mark for water level
count = 1
readi2c = bytearray([0,0])


# mqttJson = '{"Temperature" : "temperature" , "Humidity" : "humidity" , "eCO2ppm" : "eCO2" , "TVOCppb" : "tVOC" , "Baseline_HB" : "baseline_HB" , "Baseline_LB" : "baseline_LB" , "Date" : "thedate" , "Time" : "thetime"}'

mqttJson = {
  "Temperature" : "temperature",
  "Humidity" : "humidity",
  "eCO2ppm" : "eCO2",
  "TVOCppb" : "tVOC", 
  "Baseline_HB" : "baseline_HB",
  "Baseline_LB" : "baseline_LB",
  "Date" : "thedate",
  "Time" : "thetime"
  }


def write_i2c_word(): # perform write
   size   = 2
   value  = [0x08, 0x01]
   print('Writing to device 0x%02x, address: 0x%02x, writing: 0x%02x'%(i2c_devAddr, i2c_addr, value[0]))
   val    = i2c.write(i2c_devAddr, i2c_addr, value)
   print('   writeBytes returned: %s'%(val))
   return(val)

def read_i2c_word(i2c_addr, i2c_devAddr): # read two byte value
   size    = 2
   print('Reading from device 0x%02x, address: 0x%02x'%(i2c_devAddr, i2c_addr))
   val     = i2c.readBytes(i2c_devAddr, i2c_addr, size)
   print('   Read returned: %s'%(val))
   return(val)

CLEAN_SESSION=True
logging.basicConfig(level=logging.INFO) #error logging
#logging.basicConfig(level=logging.DEBUG) #error logging
#use DEBUG,INFO,WARNING

def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   print("subscribed with qos",granted_qos, "\n")
   time.sleep(1)
   logging.info("sub acknowledge message id="+str(mid))
   pass

def on_disconnect(client, userdata,rc=0):
    print("DisConnected result code "+str(rc))
    time.sleep(1)
    logging.info("DisConnected result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    print("Connected flags"+str(flags)+"result code "+str(rc))
    time.sleep(1)
    logging.info("Connected flags"+str(flags)+"result code "+str(rc))

def on_message(client, userdata, message):
    msg=str(message.payload.decode("utf-8"))
    print("message received  "  +msg)
    
def on_publish(client, userdata, mid):
    print("message published "  +str(mid))
    time.sleep(1)
    logging.info("message published "  +str(mid))

def on_message_print(client, userdata, message):
    msg = message
    #client.publish(topic1,message.payload)
    #print("%s %s" % (message.topic, message.payload))
    client.publish(topic1,str(msg))
    print("%s %s" % (message.topic, msg))

#client = mqtt.Client(client_id,clean_session=False, userdata=None, protocol="MQTTv311", transport="tcp")       #create client object
client = mqtt.Client(client_id,clean_session=False)       #create client object

client.on_subscribe = on_subscribe   #assign function to callback
client.on_disconnect = on_disconnect #assign function to callback
client.on_connect = on_connect #assign function to callback
#client.on_message = on_message
client.on_message = on_message_print

client.username_pw_set(username, password)  			# define the username and password to use with mqtt
#client.connect(broker,port,keepalive=60, bind_address="")       #establish connection
client.connect(broker,port,keepalive=60)       #establish connection

time.sleep(1)

client.subscribe(topic, QOS)
client.publish(topic,"starting",QOS,retain=False)

client.loop_start()

while True: #runs forever break with CTRL+C
   # check with Arduino - get sensor state
   readi2c = read_i2c_word(i2c_addr, i2c_devAddr)
   readi2c_HB = readi2c[0]       # Low water mark 
   readi2c_LB = readi2c[1]       # High water mark
   print("readi2c_HB = "+str(readi2c_HB))
   print("readi2c_LB = "+str(readi2c_LB))
   if readi2c_HB == 1 and readi2c_LB == 1:    # water level is high let empty it!
       msg='message "dehunidifier is full" from OnionOmega, turning pump on'
       print("publishing to topic %s message is \"%s\"  " % (topic1,msg))
       client.publish(topic1,msg)
       msg="on"                        # turn pump on
       client.publish(topic,msg)
       while readi2c[0] == 1:          # wait until we hit the low water mark
                readi2c = read_i2c_word(i2c_addr, i2c_devAddr)
       msg="off"                       # turn pump off
       client.publish(topic,msg)    
   msg="message " +str(count) + " from OnionOmega - i2C is"+str(readi2c)   # wait for next event
   print("publishing to topic %s messages is \"%s\"  " % (topic1,msg))
   client.publish(topic1,msg)
   count +=1
   time.sleep(delay)

client.disconnect()

client.loop_stop()

