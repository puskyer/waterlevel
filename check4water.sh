#!/bin/bash

#opkg update
#opkg install bash coreutils-stty
# mosquitto_pub [-h host] [-k keepalive] [-p port] [-q qos] [-r] {-f file | -l | -n | -m message} -t topic

read user pass < /$HOME/waterlevel.conf

water=no
startTime=$(date +%s)
waitTime=600
mqttPort=1883
mqttSRV=192.168.1.1
cycleCount=0
# sensor = raindrop or waterlevel
sensor=$HOSTNAME

###### Start of functions

redwatersensorP() {
while read line  < /dev/ttyS1 ; do

        nowTime=$(date +%s)
	      cycleCount=$((cycleCount+1))

#	echo -n "nowTime=$nowTime     startTime=$startTime"

        if [ "$line" -ge "20" -a "$water" == "no" ] ; then
                # get the time we started
                startTime=$(date +%s)
                python /$HOME/sendemail.py /$HOME/pasquale.conf
                python /$HOME/sendemail.py /$HOME/jacinthe.conf
                # logger -s -t waterlevel -p 6 "Check water Level via Camera! Level @ $line% Time is `date +%R`"
                water=yes
        # if water is present and its been 5 minutes then lets send another email
        elif [ "$water" == "yes" ] && [ $(expr $nowTime - $startTime) -ge $waitTime ] ; then
                water=no
        # if the water is now gone clear water flag
        elif [ "$line" == "0" -a "$water" == "yes" ] ; then
                water=no
        fi

	if [ "$line" -lt "40" ] && [ "$line" -ge "20" ] ; then
		mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water present @ $line%" -t stat/waterlevel/$sensor -u $user -P $pass
	elif [ "$line" -ge "40" ] ; then
		mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water level RISING now @ $line%" -t stat/waterlevel/$sensor -u $user -P $pass
	fi

	if [ $cycleCount -eq 60 ] ; then
		cycleCount=0
		 if [ "$line" -lt "5" ] ; then
                    mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water NOT present level is $line" -t stat/waterlevel/$sensor -u $user -P $pass
		 fi
	fi

        sleep 60
done

}

raindropsensorP()
{
while read  level line < /dev/ttyS1 ; do

        nowTime=$(date +%s)
	      cycleCount=$((cycleCount+1))

#	echo -n "nowTime=$nowTime     startTime=$startTime"

        if [ "$line" == "LOW" -a "$water" == "no" ] ; then
                # get the time we started
                startTime=$(date +%s)
                python /$HOME/sendemail.py /$HOME/pasquale.conf
                python /$HOME/sendemail.py /$HOME/jacinthe.conf
                # logger -s -t waterlevel -p 6 "Check water Level via Camera! Level is $level Time is `date +%R`"
                water=yes
        # if water is present and its been 5 minutes then lets send another email
        elif [ "$water" == "yes" ] && [ $(expr $nowTime - $startTime) -ge $waitTime ] ; then
                water=no
        # if the water is now gone clear water flag
        elif [ "$line" == "HIGH" -a "$water" == "yes" ] ; then
                water=no
        fi

	if [ "$line" == "AVERAGE" ] ; then
		mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water present level is $level" -t stat/waterlevel/$sensor -u $user -P $pass
	elif [ "$line" == "LOW" ] ; then
		mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water level RISING level is $level" -t stat/waterlevel/$sensor -u $user -P $pass
	fi

	if [ $cycleCount -eq 60 ] ; then
		cycleCount=0
		 if [ "$line" == "HIGH" ] ; then
                    mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water NOT present level is $level" -t stat/waterlevel/$sensor -u $user -P $pass
		 fi
	fi
        sleep 60
done

}

#### start of code


case "$sensor" in
  raindropsensor )
        stty -F /dev/ttyS1 9600 -parity cs8
        mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water Level check started on $sensor at $(date)!" -t stat/waterlevel/$sensor -u $user -P $pass
        raindropsensorP
        ;;
  redwatersensor )
        stty -F /dev/ttyS1 9600 -parity cs8
        mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "Water Level check started on $sensor at $(date)!" -t stat/waterlevel/$sensor -u $user -P $pass
        redwatersensorP
        ;;
 * )
        mosquitto_pub -h $mqttSRV -p $mqttPort -q 0 -m "$HOSTNAME not a sensor" -t stat/waterlevel/ -u $user -P $pass
        ;;
esac
