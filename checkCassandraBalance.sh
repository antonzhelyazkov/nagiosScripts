#!/bin/bash

nodetoolBin="nodetool"

hash $nodetoolBin 2>/dev/null || { echo >&2 "I require nodetool but it's not installed. Aborting."; exit 1; }
