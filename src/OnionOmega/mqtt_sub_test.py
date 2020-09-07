import paho.mqtt.client as mqtt
import time,logging
broker="192.168.1.41"

topic ="notification"
topic1="log"
port=1883
QOS=1
delay=5
client_id="OnionOmega"
mqttVer="MQTTv311"
username ="mqttUser"
password =" "

CLEAN_SESSION=True
logging.basicConfig(level=logging.INFO) #error logging
#use DEBUG,INFO,WARNING

def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
   print("subscribed with qos",granted_qos, "\n")
   time.sleep(1)
   logging.info("sub acknowledge message id="+str(mid))
   pass

def on_disconnect(client, userdata,rc=0):
    logging.info("DisConnected result code "+str(rc))

def on_connect(client, userdata, flags, rc):
    logging.info("Connected flags"+str(flags)+"result code "+str(rc))

def on_message(client, userdata, message):
    msg=str(message.payload.decode("utf-8"))
    print("message received  "  +msg)
    
def on_publish(client, userdata, mid):
    logging.info("message published "  +str(mid))

def on_message_print(client, userdata, message):
    client.publish(topic1,message.payload)
    print("%s %s" % (message.topic, message.payload))

#client = mqtt.Client(client_id,clean_session=False, userdata=None, protocol="MQTTv311", transport="tcp")       #create client object
client = mqtt.Client(client_id,clean_session=False)       #create client object

client.on_subscribe = on_subscribe   #assign function to callback
client.on_disconnect = on_disconnect #assign function to callback
client.on_connect = on_connect #assign function to callback
#client.on_message = on_message
client.on_message = on_message_print

client.username_pw_set(username, password)  			# define the username and password to use with mqtt
#client.connect(broker,port,keepalive=60, bind_address="")       #establish connection
client.connect(broker,port)       #establish connection

time.sleep(1)

client.loop_start()

client.subscribe(topic, QOS)

count=1

while True: #runs forever break with CTRL+C
#   msg="message " +str(count) + " from OnionOmega"
#   print("publishing on topic %s messages is \"%s\"  " % (topic1,msg))
#   client.publish(topic1,msg)
   count +=1
   time.sleep(delay)

client.disconnect()

client.loop_stop()

