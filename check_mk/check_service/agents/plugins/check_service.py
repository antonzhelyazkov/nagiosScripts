#!/usr/bin/python3

import json
import os
import sys
import subprocess

config_file_name = os.path.basename(sys.argv[0]).split('.')[0]
CONFIG_FILE = f"/etc/check_mk/{config_file_name}"


def check_service(service_name) -> bool:
    cmd = ["systemctl", "is-active", "--quiet", service_name]
    stat = subprocess.call(cmd)
    if stat == 0:
        return True
    else:
        return False


def main():
    print(f'<<<{config_file_name}>>>')
    try:
        config_handler = open(CONFIG_FILE, 'r')
        config_raw = config_handler.read()
    except OSError as err:
        print(f"ERROR miss {err}")
        return False

    try:
        config = json.loads(config_raw)
    except json.decoder.JSONDecodeError as conf_err:
        print(f"ERROR config {conf_err}")
        return False

    service = filter(lambda seq: config[seq]['type'] == 'service', config.keys())

    for item_service in list(service):
        print(f"{config[item_service]['type']} {item_service} {check_service(item_service)}")


if __name__ == "__main__":
    main()
