<?php

$colors = [ '164fbf','ff2e00','337c4f','164fbf','60e060','60c0c0','6060e0','e060e0','c0c0c0' ];

##########################################################################################
#error_log("names: ". join(" ",array_keys($NAME) ) );
#error_log("values: ". join(" ",array_values($NAME) ) );


$nodes = count(array_keys($NAME))/2;

$opt[1] = "--vertical-label \"Load\" -l 0 --title \"cassandra $hostname / $servicedesc\" ";

$counter1=0;

        for ( $i=1; $i<=$nodes; $i++) {
        if ( $counter1 == 0 ) {
                $def[1] = "DEF:var$i=$rrdfile:$DS[$i]:AVERAGE " ;
        } else {
                $def[1] .= "DEF:var$i=$rrdfile:$DS[$i]:AVERAGE " ;
        }
        $color = $colors[$counter1];
        error_log("color ". $color);
        $def[1] .= "LINE$i:var$i#$color:\"$NAME[$i]\" " ;
        $def[1] .= "GPRINT:var$i:LAST:\"%6.2lf last\" " ;
        $def[1] .= "GPRINT:var$i:MAX:\"%6.2lf max\l\" " ;
        $counter1++;
        }

$opt[2] = "--vertical-label \"Owns\" -l 0 --title \"cassandra $hostname / $servicedesc\" ";

$counter2=0;

        for ( $i=($nodes + 1); $i<=($nodes * 2); $i++) {
        if ( $counter2 == 0 ) {
                $def[2] = "DEF:var$i=$rrdfile:$DS[$i]:AVERAGE " ;
        } else {
                $def[2] .= "DEF:var$i=$rrdfile:$DS[$i]:AVERAGE " ;
        }
        $color = $colors[$counter2];
        error_log("color ". $color);
        $def[2] .= "LINE$i:var$i#$color:\"$NAME[$i]\" " ;
        $def[2] .= "GPRINT:var$i:LAST:\"%6.2lf last\" " ;
        $def[2] .= "GPRINT:var$i:MAX:\"%6.2lf max\l\" " ;
        $counter2++;
        }
?>
