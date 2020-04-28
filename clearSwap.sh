#!/bin/bash

logFile="/var/log/clearSwap.log"

if [ $(swapon -s | grep partition -q; echo $?) -eq 0 ]
then

        swapUsage=$(free | awk '/Swap/{printf("%.0f"), $3/$2*100}')
        swapLimit=2

        if [ $swapUsage -gt $swapLimit ]
        then
                echo $(date "+%Y-%m-%d %H:%M:%S") "WARNING Swap usage is $swapUsage% start swapoff -a" >> $logFile
                swapoff -a
                checkSwapOff=$?
                if [ $checkSwapOff -eq 0 ]
                then
                        echo $(date "+%Y-%m-%d %H:%M:%S") "OK swapoff -a finished" >> $logFile
                else
                        echo $(date "+%Y-%m-%d %H:%M:%S") "WARNING swapoff -a exit with error $checkSwapOff" >> $logFile
                        exit 1
                fi
                swapon -a
                checkSwapOn=$?
                if [ $checkSwapOn -eq 0 ]
                then
                        echo $(date "+%Y-%m-%d %H:%M:%S") "OK swapon -a finished" >> $logFile
                else
                        echo $(date "+%Y-%m-%d %H:%M:%S") "WARNING swapon -a exit with error $checkSwapOn" >> $logFile
                        exit 1
                fi
        else
                echo $(date "+%Y-%m-%d %H:%M:%S") "OK Swap usage is $swapUsage%" >> $logFile
        fi
else
        echo $(date "+%Y-%m-%d %H:%M:%S") "WARNING swap is OFF trying to switch ON" >> $logFile
        swapon -a
        checkSwapOn=$?
        if [ $checkSwapOn -eq 0 ]
        then
                echo $(date "+%Y-%m-%d %H:%M:%S") "OK swapon -a finished" >> $logFile
        else
                echo $(date "+%Y-%m-%d %H:%M:%S") "WARNING swapon -a exit with error $checkSwapOn" >> $logFile
                exit 1
        fi
fi
