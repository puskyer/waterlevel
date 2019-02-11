#!/bin/bash /etc/rc.common

START=99

start() {
  # commands to launch application
  if [ ! $(pgrep -f check4water.sh) ] ; then
      echo start
      /root/check4water.sh &
      pidof check4water.sh >/var/run/check4water.pid
  else
      echo "check4water.sh  already running pid $(pidof check4water.sh) !"
  fi
}

stop() {
  echo stop
  # commands to kill application
  kill -9 $(cat /var/run/check4water.pid)
}

restart() {
  echo restarting
  # commands to kill application
  /root/startC4W.sh stop
  # commands to start application
  /root/startC4W.sh start
}
