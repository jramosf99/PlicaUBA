#!/bin/bash
PID_watchdog_UBA1=$(if [[ $(ps -ef | grep -v grep | grep general | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep general | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
if [ "$PID_watchdog_UBA1" == "down" ];
then
echo $PID_watchdog_UBA1 
else 
kill $PID_watchdog_UBA1  
fi
exit


