import json
import os
import sys
import subprocess

config_file_name = os.path.basename(sys.argv[0]).split('.')[0]
CONFIG_FILE = f"/etc/check_mk/{config_file_name}"


def get_services(in_json: dict):
    services = []
    for key in in_json:
        print(in_json[key]['type'])
    #     if key['type'] == 'service':
    #         services.append(key)
    #
    # return services


def main():
    with open(CONFIG_FILE, 'r') as config_handler:
        config_raw = config_handler.read()

    try:
        config = json.loads(config_raw)
    except json.decoder.JSONDecodeError as conf_err:
        print(f"ERROR config {conf_err}")
        return False

    get_services(config)


if __name__ == "__main__":
    main()
