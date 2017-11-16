#!/bin/bash
#############################
#
# Create cutom nginx log
#
# log_format nginx_cache '$remote_addr – $upstream_cache_status [$time_local] '
#       '"$request" $status $body_bytes_sent '
#       '"$http_referer" "$http_user_agent" ';
#
#############################


OPTS=$(getopt -o l:w:c:n: --long log:,warning:,critical: -n 'parse-options' -- "$@")
getOptsExitCode=$?
if [ $getOptsExitCode != 0 ]; then
        echo "Failed parsing options." >&2 ;
        exit 1 ;
fi

eval set -- "$OPTS"

numberOfRows=1000

while true; do
        case "$1" in
                --log | -l ) logFile="$2"; shift; shift ;;
                --warning | -w ) warningLevel="$2"; shift; shift ;;
                --critical | -c ) criticalLevel="$2"; shift; shift ;;
                -n ) numberOfRows="$2"; shift; shift ;;
                -- ) shift; break ;;
                * ) break ;;
        esac
done

if [[ ! -e $logFile ]]; then
        echo "File $logFile does not exist"
        exit 1
fi

if [ $warningLevel -lt $criticalLevel ]; then
        echo "Warning value must be greater than critical value"
        exit 1
fi

rowResult=$(tail -n $numberOfRows $logFile | awk '{print $3}' | sort | uniq -c | tr '\n' ' ')
IFS=' ' read -a resultArray <<< "${rowResult}"
arrayLength=${#resultArray[@]}

for (( i=0; i<${arrayLength};  i++ ));
do
        if [[ ${resultArray[$i]} == "HIT" ]]; then
                hitValue=${resultArray[$i-1]}
        elif [[ ${resultArray[$i]} == "MISS" ]]; then
                missValue=${resultArray[$i-1]}
        elif [[ ${resultArray[$i]} == "EXPIRED" ]]; then
                expiredValue=${resultArray[$i-1]}
        elif [[ ${resultArray[$i]} == "UPDATING" ]]; then
                updatingValue=${resultArray[$i-1]}
        fi
done

if [ -z $hitValue ]; then
        hitValue=0
fi
if [ -z $missValue ]; then
        missValue=0
fi
if [ -z $expiredValue ]; then
        expiredValue=0
fi
if [ -z $updatingValue ]; then
        updatingValue=0
fi

if [ $updatingValue -eq 0 ] && [ $expiredValue -eq 0 ] && [ $missValue -eq 0 ] && [ $hitValue -eq 0 ]; then
        echo "CRITICAL - incorrect log file format. Add \"– \$upstream_cache_status\" right after \$remote_addr as follow: log_format nginx_cache '\$remote_addr – \$upstream_cache_status [\$time_local] – '"
        exit 2
fi

allValues=$(( $hitValue + $missValue + $expiredValue + $updatingValue))

hitPercent=$((200*$hitValue/$allValues % 2 + 100*$hitValue/$allValues))
missPercent=$((200*$missValue/$allValues % 2 + 100*$missValue/$allValues))
expiredPercent=$((200*$expiredValue/$allValues % 2 + 100*$expiredValue/$allValues))
updatingPercent=$((200*$updatingValue/$allValues % 2 + 100*$updatingValue/$allValues))

#echo $hitPercent $missPercent $expiredPercent $updatingPercent
if [ $hitPercent -gt $warningLevel ]; then
        echo "OK hit - $hitPercent%; miss - $missPercent%; expired - $expiredPercent%; updating - $updatingPercent% |  hit=$hitPercent% miss=$missPercent% expired=$expiredPercent% updating=$updatingPercent%"
        exit 0
elif [ $hitPercent -le $warningLevel ] && [ $hitPercent -gt $criticalLevel ]; then
        echo "WARNING hit - $hitPercent%; miss - $missPercent%; expired - $expiredPercent%; updating - $updatingPercent% |  hit=$hitPercent% miss=$missPercent% expired=$expiredPercent% updating=$updatingPercent%"
        exit 1
elif [ $hitPercent -le $criticalLevel ]; then
        echo "CRITICAL hit - $hitPercent%; miss - $missPercent%; expired - $expiredPercent%; updating - $updatingPercent% |  hit=$hitPercent% miss=$missPercent% expired=$expiredPercent% updating=$updatingPercent%"
        exit 2
fi
