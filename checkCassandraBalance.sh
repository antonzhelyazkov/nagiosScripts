#!/bin/bash

nodetoolBin="nodetool"
bcBin="bc"

hash $nodetoolBin 2>/dev/null
checkNodetool=$?
if [ $checkNodetool -ne 0 ]; then
	echo "CRITICAL nodetool not found"
	exit 2
fi

hash $bcBin 2>/dev/null
checkBC=$?
if [ $checkBC -ne 0 ]; then
        echo "CRITICAL bc not found. Try to install bc"
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
	nodeDataDimension=$(echo ${array[2]} | sed -e 's/^[ \t]*//')
	nodePct=$(echo ${array[4]} | sed -e 's/^[ \t]*//' | sed 's/.$//')
	if [ ! -z $nodeIP ] || [ ! -z $nodeData ];then
		if [[ $nodeDataDimension =~ ^MiB$ ]]; then
			nodeData=$( echo "scale=2; $nodeData / 1024" | bc | sed 's/^\./0./' )
		fi
		if [ $counter -eq 0 ]; then
                        nagiosLine="$nodeIP=$nodeData"
			nagiosLineDataPNP="$nodeIP"_data"=$nodeData;"
			nagiosLinePctPNP="$nodeIP"_pct"=$nodePct;"
                else
                        nagiosLine=$nagiosLine" $nodeIP=$nodeData"
			nagiosLineDataPNP=$nagiosLineDataPNP" $nodeIP"_data"=$nodeData;"
			nagiosLinePctPNP=$nagiosLinePctPNP" $nodeIP"_pct"=$nodePct;"
                fi
	((counter++))
	fi
done

echo "$nagiosLine | $nagiosLineDataPNP $nagiosLinePctPNP"
exit 0
