#!/bin/bash

read user pass < /$HOME/waterlevel.conf

mqttPort=1883
mqttSRV=192.168.1.1
sensor=PowR2
sensorstat=PowR2stat

Response=`mosquitto_sub -C 1 -h $mqttSRV -p $mqttPort -q 2 -t  cmnd/$sensor/POWER -u $user -P $pass`

if [ ! "$Response" == "ON" ] ; then

	mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -r -m "ON" -t cmnd/$sensor/POWER -u $user -P $pass

	sleep 60

	mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -r -m "POWR2 now ON" -t stat/$sensorstat/ -u $user -P $pass

else

	echo "PowR2 Powered ON"

fi


