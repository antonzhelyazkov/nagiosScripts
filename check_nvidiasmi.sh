#!/bin/bash

OPTS=$(getopt -o wct --long warning:,critical:,tmp: -n 'parse-options' -- "$@")
getOptsExitCode=$?
if [ $getOptsExitCode != 0 ]; then
        echo "Failed parsing options." >&2 ;
        exit 1 ;
fi

eval set -- "$OPTS"

warning="85"
critical="95"
tmpXmlFileName=nvidia.xml
tmpXmlDir=/tmp
HELP=false

while true; do
        case "$1" in
                --warning ) warning="$2"; shift; shift ;;
                --critical ) critical="$2"; shift; shift ;;
                --tmp ) tmpXmlDir="$2"; shift; shift ;;
                -- ) shift; break ;;
                * ) break ;;
        esac
done

tmpDirTrimmed=$(echo $tmpXmlDir | sed 's:/*$::')
tmpXml=$tmpDirTrimmed/$tmpXmlFileName

temperatureWarningTreshold=85
temperatureCriticalTreshold=95
fanWarningTreshold=75
fanCriticalTreshold=85

encoderWarning=0
decoderWarning=0
gpuWarning=0
memoryWarning=0
temperatureWarning=0
fanWarning=0

hash xmlstarlet 2>/dev/null
checkXmlstarlet=$?
if [ $checkXmlstarlet -ne 0 ]; then
        echo "CRITICAL xmlstarlet not found. Try to install xmlstarlet"
        exit 2
fi

hash nvidia-smi 2>/dev/null
checkNvidiaSmi=$?
if [ $checkNvidiaSmi -ne 0 ]; then
        echo "CRITICAL nvidia-smi not found. Try to install nvidia-smi"
        exit 2
fi

nvidia-smi -q -x --filename=$tmpXml
checkXmlCreation=$?
if [ $checkXmlCreation -ne 0 ]; then
        echo "CRITICAL could not create $tmpXml with user $USER"
        exit 2
fi

fanUtil=$(xmlstarlet fo --dropdtd $tmpXml | xmlstarlet sel -t -v nvidia_smi_log/gpu/fan_speed | sed 's/\ \%*$//')
encoderUtil=$(xmlstarlet fo --dropdtd $tmpXml | xmlstarlet sel -t -v nvidia_smi_log/gpu/utilization/encoder_util | sed 's/\ \%*$//')
gpuUtil=$(xmlstarlet fo --dropdtd $tmpXml | xmlstarlet sel -t -v nvidia_smi_log/gpu/utilization/gpu_util | sed 's/\ \%*$//')
memoryUtil=$(xmlstarlet fo --dropdtd $tmpXml | xmlstarlet sel -t -v nvidia_smi_log/gpu/utilization/memory_util | sed 's/\ \%*$//')
decoderUtil=$(xmlstarlet fo --dropdtd $tmpXml | xmlstarlet sel -t -v nvidia_smi_log/gpu/utilization/decoder_util | sed 's/\ \%*$//')
temperature=$(xmlstarlet fo --dropdtd $tmpXml | xmlstarlet sel -t -v nvidia_smi_log/gpu/temperature/gpu_temp | sed 's/\ \%*C//')
temperatureMax=$(xmlstarlet fo --dropdtd $tmpXml | xmlstarlet sel -t -v nvidia_smi_log/gpu/temperature/gpu_temp_max_threshold | sed 's/\ \%*C//')

temperatureTresholdPercent=$(awk "BEGIN { pc=100*${temperature}/${temperatureMax}; i=int(pc); print (pc-i<0.5)?i:i+1 }")

rm -f $tmpXml

#echo $temperatureTresholdPercent $temperatureWarningTreshold

if [ $fanUtil -lt $fanWarningTreshold ] && [ $encoderUtil -lt $warning ] && [ $gpuUtil -lt $warning ] && [ $memoryUtil -lt $warning ] && [ $decoderUtil -lt $warning ] && [ $temperatureTresholdPercent -lt $temperatureWarningTreshold ]; then
        echo "OK GPU - $gpuUtil%; Memory - $memoryUtil%; Encoder - $encoderUtil%; Decoder - $decoderUtil%; Temperature - $temperature; Fan - $fanUtil% | gpu=$gpuUtil% memory=$memoryUtil% encoder=$encoderUtil% decoder=$decoderUtil% temperature=$temperature fan=$fanUtil%"
        exit 0
fi

if [ $encoderUtil -gt $warning ] && [ $encoderUtil -lt $critical ]; then
        encoderWarning=1
fi

if [ $decoderUtil -gt $warning ] && [ $decoderUtil -lt $critical ]; then
        decoderWarning=1
fi

if [ $gpuUtil -gt $warning ] && [ $gpuUtil -lt $critical ]; then
        gpuWarning=1
fi

if [ $memoryUtil -gt $warning ] && [ $memoryUtil -lt $critical ]; then
        memoryWarning=1
fi

if [ $temperatureTresholdPercent -gt $temperatureWarningTreshold ] && [ $temperatureTresholdPercent -lt $temperatureCriticalTreshold ]; then
        temperatureWarning=1
fi

if [ $fanUtil -gt $fanWarningTreshold ] && [ $fanUtil -lt $fanCriticalTreshold ]; then
        fanWarning=1
fi


#echo "enc" $encoderWarning "dec" $decoderWarning "gpu" $gpuWarning "mem" $memoryWarning "temp" $temperatureWarning

if [ $fanWarning -eq 1 ] || [ $encoderWarning -eq 1 ] || [ $decoderWarning -eq 1 ] || [ $gpuWarning -eq 1 ] || [ $memoryWarning -eq 1 ] || [ $temperatureWarning -eq 1 ]; then
        echo "WARNING GPU - $gpuUtil%; Memory - $memoryUtil%; Encoder - $encoderUtil%; Decoder - $decoderUtil%; Temperature - $temperature; Fan - $fanUtil% | gpu=$gpuUtil% memory=$memoryUtil% encoder=$encoderUtil% decoder=$decoderUtil% temperature=$temperature fan=$fanUtil%"
        exit 1
fi

if [ $fanUtil -gt $fanCriticalTreshold ] || [ $encoderUtil -gt $critical ] || [ $gpuUtil -gt $critical ] || [ $memoryUtil -gt $critical ] || [ $decoderUtil -gt $critical ] || [ $temperatureTresholdPercent -gt $temperatureCriticalTreshold ]; then
        echo "CRITICAL GPU - $gpuUtil%; Memory - $memoryUtil%; Encoder - $encoderUtil%; Decoder - $decoderUtil%; Temperature - $temperature; Fan - $fanUtil% | gpu=$gpuUtil% memory=$memoryUtil% encoder=$encoderUtil% decoder=$decoderUtil% temperature=$temperature fan=$fanUtil%"
        exit 2
fi
