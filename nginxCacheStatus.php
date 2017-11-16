<?php
#
# Plugin: nginxCacheStatus.sh
#
#
$opt[1] = "--vertical-label \"Usage\" -b 1024 -l 0 --title \"NGINX cache hitrate for $hostname / $servicedesc\" ";
#hit
$def[1] = "DEF:var1=$rrdfile:$DS[1]:AVERAGE " ;

$def[1] .= "LINE:var1#FF0000:\"hit\" " ;
$def[1] .= "GPRINT:var1:LAST:\"%3.2lf %Sp last\" " ;
$def[1] .= "GPRINT:var1:AVERAGE:\"%3.2lf %Sp avg\" " ;
$def[1] .= "GPRINT:var1:MAX:\"%3.2lf %Sp max\l\" ";

#miss
$def[1] .= "DEF:var2=$rrdfile:$DS[2]:AVERAGE " ;

$def[1] .= "LINE:var2#FF8000:\"miss\" " ;
$def[1] .= "GPRINT:var2:LAST:\"%3.2lf %Sp last\" " ;
$def[1] .= "GPRINT:var2:AVERAGE:\"%3.2lf %Sp avg\" " ;
$def[1] .= "GPRINT:var2:MAX:\"%3.2lf %Sp max\l\" ";

#expired
$def[1] .= "DEF:var3=$rrdfile:$DS[3]:AVERAGE " ;

$def[1] .= "LINE:var3#4B8A08:\"expired\" " ;
$def[1] .= "GPRINT:var3:LAST:\"%3.2lf %Sp last\" " ;
$def[1] .= "GPRINT:var3:AVERAGE:\"%3.2lf %Sp avg\" " ;
$def[1] .= "GPRINT:var3:MAX:\"%3.2lf %Sp max\l\" ";

#updating
$def[1] .= "DEF:var4=$rrdfile:$DS[4]:AVERAGE " ;

$def[1] .= "LINE:var4#2E3B0B:\"updating\" " ;
$def[1] .= "GPRINT:var4:LAST:\"%3.2lf %Sp last\" " ;
$def[1] .= "GPRINT:var4:AVERAGE:\"%3.2lf %Sp avg\" " ;
$def[1] .= "GPRINT:var4:MAX:\"%3.2lf %Sp max\l\" ";

?>
