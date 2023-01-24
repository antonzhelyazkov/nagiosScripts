# nagiosScripts
## Cassandra monitoring scripts

## check nvidia GPU utilization
This plugin needs nvidia-smi and xmlstarlet
```
/usr/local/bin/check_nvidiasmi.sh
```
OK GPU - 32%; Memory - 12%; Encoder - 53%; Decoder - 23% | gpu=32% memory=12% encoder=53[cuda]

#### pnp4nagios template installation
place check_nvidiasmi.php in pnp4nagios template directory

```
curl -o /usr/share/nagios/html/pnp4nagios/templates/check_nvidiasmi.php  https://raw.githubusercontent.com/antonzhelyazkov/nagiosScripts/master/check_nvidiasmi.php
```

#### nvidia-smi installation

```
vi /etc/yum.repos.d/cuda.repo
```

```
[cuda]
name=cuda
baseurl=http://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64
enabled=1
gpgcheck=1
gpgkey=http://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/7fa2af80.pub
```
yum install cuda

#### NGINX cache hitrate

Create cutom nginx log

```
log_format nginx_cache '$remote_addr – $upstream_cache_status [$time_local] '
       '"$request" $status $body_bytes_sent '
       '"$http_referer" "$http_user_agent" ';
```

log file must looks like

```
12.34.56.78 – MISS [11/Nov/2017:09:38:32 +0100] – "GET /qws/qwel/qwe.html HTTP/1.1" 200 1036448 "http://www.example.com/content" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0" "-" – "-" – "-" – "-" – "-"
```


# check_log
count error codes 500 in nginx log file

```
python3 /opt/nagiosScripts/check_log/check_log.py -l /path/to/log/access.log -w 1000 -c 2000 -s 200
```