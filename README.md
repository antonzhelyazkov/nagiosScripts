# nagiosScripts
## Cassandra monitoring scripts

## check nvidia GPU utilization
This plugin needs nvidia-smi and xmlstarlet
/usr/local/bin/check_nvidiasmi.sh

OK GPU - 32%; Memory - 12%; Encoder - 53%; Decoder - 23% | gpu=32% memory=12% encoder=53[cuda]

pnp4nagios template,
check_nvidiasmi.php

#### nvidia-smi installation

vi /etc/yum.repos.d/cuda.repo

[cuda]
name=cuda
baseurl=http://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64
enabled=1
gpgcheck=1
gpgkey=http://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/7fa2af80.pub

yum install cuda
