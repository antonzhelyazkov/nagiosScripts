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

counter=0
for line in "${nodes[@]}"
do
	IFS=' ' read -r -a array <<< $line
	nodeIP=$(echo ${array[0]} | sed -e 's/^[ \t]*//')
	nodeData=$(echo ${array[1]} | sed -e 's/^[ \t]*//')

	if [ ! -z $nodeIP ] || [ ! -z $nodeData ];then
		if [ $counter -eq 0 ]; then
                        nagiosLine="$nodeIP=$nodeData"
			nagiosLinePNP="$nodeIP=$nodeData;"
                else
                        nagiosLine=$nagiosLine" $nodeIP=$nodeData"
			nagiosLinePNP=$nagiosLinePNP" $nodeIP=$nodeData;"
                fi
	((counter++))
	fi
done

echo "$nagiosLine | $nagiosLinePNP"
exit 0
