#!/bin/bash

read user pass < /$HOME/waterlevel.conf

mqttPort=1883
mqttSRV=192.168.1.1
sensor=PowR2
sensorstat=PowR2stat

reply1="ping: www.google.com: Name or service not known"
reply2="1 packets transmitted, 1 received, 0% packet loss, time 0ms"

CkPing1=`ping -4 -q -c 1 www.google.com | grep "$reply1"`
CkPing2=`ping -4 -q -c 1 www.google.com | grep "$reply2"`

Response=`mosquitto_sub -C 1 -h $mqttSRV -p $mqttPort -q 2 -t  cmnd/$sensor/POWER -u $user -P $pass`

PowR2_ON() {

	# turn on PowR2
	mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -r -m "ON" -t cmnd/$sensor/POWER -u $user -P $pass
	sleep 60
	# Publish that we turned PowR2 on
	mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -r -m "PoWR2 now ON" -t stat/$sensorstat/ -u $user -P $pass
}


if [ "$CkPing1" == "$reply1" ] ; then
	# DNS issues
	if [ "$Response" == "OFF" ; then	# if PowR2 is off turn it on
		PowR2_ON
	fi
elif [ "$CkPing2" == "$reply2" ]
	then
	# ping worked so Internet is up lets quit
	echo "`date` PowR2 Powered ON"
	exit 0
else
	# if the PowR2 is OFF lets turn it on.
        if [ "$Response" == "OFF" ; then        # if PowR2 is off turn it on
                PowR2_ON
	else
		# if we got here then not sure what the issue is
		# lets print out some info...
		echo "`date`"
		echo "$CkPing1"
		echo "$CkPing2"
		echo "$Response"
        fi
fi

