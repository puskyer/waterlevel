#!/bin/bash /etc/rc.common

#START=99


start() {        
        echo start
        # commands to launch application
	/root/check4water.sh &
	pidof check4water.sh >/var/run/check4water.pid
}                 
 
stop() {          
        echo stop
        # commands to kill application 
	kill -9 $(cat /var/run/check4water.pid)
}
