#!/usr/bin/python
import paho.mqtt.client as mqtt
import time,logging
from OmegaExpansion import onionI2C
import sys

broker="192.168.1.41"

topic ="OnionOmega/notification"
cmdtopic ="bilgpump/cmnd"
topic1="OnionOmega/info"
port=1883
QOS=1
delay=5
client_id="OnionOmega"
mqttVer="MQTTv311"
DataJson = {
      "APSSID" : "ssid",
      "APpassword" : "ssid_password",
      "STSSID" : "ssid",
      "STpassword" : "ssid_password",
      "mqtt_user" : "User",
      "mqtt_password" : "Pass",
      "email_user" : "name@gmail.com",
      "email_pass" : "password",
      "mailto" : "name@gmail.com"
      }

import json
with open('config.json') as data_file:
    DataJson = json.load(data_file)
    data_file.close
username =  DataJson["wifi"]["mqtt_user"]
password =  DataJson["wifi"]["mqtt_password"]
email_user =  DataJson["wifi"]["email_user"]
email_pass =  DataJson["wifi"]["email_pass"]
mailto =  DataJson["wifi"]["mailto"]

i2c = onionI2C.OnionI2C(0)
# set the i2c verbosity
i2c.setVerbosity(1)
i2c_addr = 0x0
i2c_devAddr = 0x08

readi2c_HB = b'0x0'      # this is the Low mark for water level
readi2c_LB = b'0x0'      # this is the High mark for water level
count = 1
msgCount=0
maxmsgCount=12           # maxmsgCount x delay = 60 sec approximitly
readi2c = bytearray([0,0])
debug = False

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

# Sends the email!
def sendemail(mailto,subject,body):
    import smtplib,re

    
    email_name = 'OnionOmega'                 # Optional - A friendly name for the 'From' field

    

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    # Build an SMTP compatible message from arguments
    if (email_name is not ''):
        msg = "From: " + email_name + " <" + email_user + ">\n"
    else:
        msg = "From: " + email_user + "\n"
    msg += "To: " + mailto + "\n"
    msg += "Subject: " + subject + "\n"
    msg += body

    # Attempt to connect and send the email!
    try:
        smtpObj = ''                  # Declare within this block only.

        # Check for SMTP over SSL by port number and connect accordingly
        if( smtp_port == 465):
            smtpObj = smtplib.SMTP_SSL(smtp_server,smtp_port)
        else:
            smtpObj = smtplib.SMTP(smtp_server,smtp_port)
        smtpObj.ehlo()

        # StartTLS if using the default TLS port number
        if(smtp_port == 587):
            smtpObj.starttls()
            smtpObj.ehlo
        # Login, send and close the connection.
        smtpObj.login(email_user,email_pass)
        smtpObj.sendmail(email_user,mailto,msg)
        smtpObj.close()
        return 0  # Return 0 to denote success!
    except Exception, err:
        # Print error and return 1 on failure.
        print err
        return 1

def write_i2c_word(): # perform write
   size   = 2
   value  = [0x08, 0x01]
   if(debug): 
   	print('Writing to device 0x%02x, address: 0x%02x, writing: 0x%02x'%(i2c_devAddr, i2c_addr, value[0]))
   val    = i2c.write(i2c_devAddr, i2c_addr, value)
   if(debug): 
	print('   writeBytes returned: %s'%(val))
   return(val)

def read_i2c_word(i2c_addr, i2c_devAddr): # read two byte value
   size = 2
   val  = i2c.readBytes(i2c_devAddr, i2c_addr, size)
   if(debug): 
   	print('Reading from device 0x%02x, address: 0x%02x'%(i2c_devAddr, i2c_addr))
	print('   Read returned: %s'%(val))
        print('Here')
   return(val)

CLEAN_SESSION=True
logging.basicConfig(level=logging.ERROR) #error logging
#logging.basicConfig(level=logging.DEBUG) #error logging
#use NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL

def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   print("subscribed with qos",granted_qos, "\n")
   time.sleep(1)
   if(debug): 
   	logging.info("sub acknowledge message id="+str(mid))
   pass

def on_disconnect(client, userdata,rc=0):
    print("DisConnected result code "+str(rc))
    time.sleep(1)
    if(debug): 
	logging.info("DisConnected result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    print("Connected flags"+str(flags)+"result code "+str(rc))
    time.sleep(1)
    if(debug): 
    	logging.info("Connected flags"+str(flags)+"result code "+str(rc))

def on_message(client, userdata, message):
    msg=str(message.payload.decode("utf-8"))
    print("message received  "  +msg)
    
def on_publish(client, userdata, mid):
    print("message published "  +str(mid))
    time.sleep(1)
    if(debug): 
    	logging.info("message published "  +str(mid))

def on_message_print(client, userdata, message):
    msg = message
    #client.publish(topic1,message.payload)
    if(debug): 
	print("%s %s" % (message.topic, message.payload))
    client.publish(topic1,str(msg))
    if(debug): 
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

# Declar email variables...

subject = 'Humidifier status'
body = ' '
# Check email address is valid!
#mailre = re.compile('(.+@.+\..+)',re.M)
#To = mailre.search(mailto)
#if(not To):
#    print "Email recipient value " + mailto + " not a valid email address!"
#    return()
body='message from Onion Omega the "dehunidifier Monitoring started"'
sendemail(mailto,subject,body)

while True: #runs forever break with CTRL+C
   # check with Arduino - get sensor state
   readi2c = read_i2c_word(i2c_addr, i2c_devAddr)
   readi2c_HB = readi2c[0]       # Low water mark 
   readi2c_LB = readi2c[1]       # High water mark
   if msgCount == 0:
      print("readi2c_HB = "+str(readi2c_HB))
      print("readi2c_LB = "+str(readi2c_LB))
   if readi2c_HB == 1 and readi2c_LB == 1:    # water level is high let empty it!
       msg='message "dehunidifier is full" from OnionOmega, turning pump on'
       print("publishing to topic %s message is \"%s\"  " % (topic1,msg))
       client.publish(topic1,msg)
       msg="on"                        # turn pump on
       client.publish(cmdtopic,msg)    
       client.publish(topic,msg)
       body='message from Onion Omega the "dehunidifier is full" turned pump on to empty'
       sendemail(mailto,subject,body)
       msg="off"                       # turn pump off
       while readi2c[0] == 1:          # wait until we hit the low water mark
                readi2c = read_i2c_word(i2c_addr, i2c_devAddr)
       client.publish(cmdtopic,msg)    
       client.publish(topic,msg)    
       body='message from Onion Omega the "dehunidifier is Now Empty" turned pump off'
       sendemail(mailto,subject,body)
   if (msgCount == 0 or debug):
      msg="message " +str(count) + " from OnionOmega - i2C is"+str(readi2c)   # wait for next event
      print("publishing to topic %s messages is \"%s\"  " % (topic1,msg))
      client.publish(topic1,msg)
      count +=1
   msgCount +=1
   if msgCount == maxmsgCount:
      msgCount = 0
   time.sleep(delay)

client.disconnect()

client.loop_stop()

