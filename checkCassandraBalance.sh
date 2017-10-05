#!/bin/bash

nodetoolBin="nodetool"

hash $nodetoolBin 2>/dev/null
checkNodetool=$?
if [ $checkNodetool -ne 0 ]; then
	echo "CRITICAL nodetool not found"
	exit 2
fi

nodetoolCommand=$($nodetoolBin status | grep UN)

IFS='UN' read -r -a nodes <<< $nodetoolCommand

for line in "${nodes[@]}"
do
	IFS=' ' read -r -a array <<< $line
	nodeData=$(echo ${array[1]} | tr '\n' ' ')
	nagiosLine=$nagiosLine$nodeData
#	echo ${array[2]} | tr '\n' ' '
#	for element in "${array[@]}"
#	do
#		echo $element
#	done
done

echo $nagiosLine
