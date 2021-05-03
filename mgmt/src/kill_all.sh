#!/bin/bash
PID_watchdog_UBA1=$(if [[ $(ps -ef | grep -v grep | grep sensor-watchdogUBA1 | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep sensor-watchdogUBA1 | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
PID_watchdog_UBA2=$(if [[ $(ps -ef | grep -v grep | grep sensor-watchdogUBA2 | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep sensor-watchdogUBA2 | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
PID_watchdog_UBA3=$(if [[ $(ps -ef | grep -v grep | grep sensor-watchdogUBA3 | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep sensor-watchdogUBA3 | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
PID_watchdog_UBA4=$(if [[ $(ps -ef | grep -v grep | grep sensor-watchdogUBA4 | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep sensor-watchdogUBA4 | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
PID_watchdog_UBA5=$(if [[ $(ps -ef | grep -v grep | grep sensor-watchdogUBA5 | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep sensor-watchdogUBA5 | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
PID_watchdog_UBA6=$(if [[ $(ps -ef | grep -v grep | grep sensor-watchdogUBA6 | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep sensor-watchdogUBA6 | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
PID_watchdog_UBA7=$(if [[ $(ps -ef | grep -v grep | grep sensor-watchdogUBA7 | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep sensor-watchdogUBA7 | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)
PID_watchdog_UBA=$(if [[ $(ps -ef | grep -v grep | grep general | wc -l) > 0 ]]; then ps -A -o pid,cmd|grep general | grep -v grep |head -n 1 | awk '{print $1}'; else echo down; fi)

if [ "$PID_watchdog_UBA" == "down" ];
then
echo $PID_watchdog_UBA
else 
kill $PID_watchdog_UBA
fi


if [ "$PID_watchdog_UBA1" == "down" ];
then
echo $PID_watchdog_UBA1 
else 
kill $PID_watchdog_UBA1  
fi

if [ "$PID_watchdog_UBA2" == "down" ];
then
echo $PID_watchdog_UBA2 
else 
kill $PID_watchdog_UBA2
fi

if [ "$PID_watchdog_UBA3" == "down" ];
then
echo $PID_watchdog_UBA3 
else 
kill $PID_watchdog_UBA3 
fi

if [ "$PID_watchdog_UBA4" == "down" ];
then
echo $PID_watchdog_UBA4
else 
kill $PID_watchdog_UBA4
fi

if [ "$PID_watchdog_UBA5" == "down" ];
then
echo $PID_watchdog_UBA5
else 
kill $PID_watchdog_UBA5
fi

if [ "$PID_watchdog_UBA6" == "down" ];
then
echo $PID_watchdog_UBA6
else 
kill $PID_watchdog_UBA6
fi

if [ "$PID_watchdog_UBA7" == "down" ];
then
echo $PID_watchdog_UBA7
else 
kill $PID_watchdog_UBA7
fi

exit