#!/bin/bash

nodetoolBin="nodetool"

hash $nodetoolBin 2>/dev/null
checkNodetool=$?
if [ $checkNodetool -ne 0 ]; then
	echo "CRITICAL nodetool not found"
	exit 2
fi
