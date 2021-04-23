import json
import os
import sys

config_file_name = os.path.basename(sys.argv[0]).split('.')[0]
CONFIG_FILE = f"/etc/check_mk/{config_file_name}"


def main():
    with open(CONFIG_FILE, 'r') as config_handler:
        config_raw = config_handler.read()

    config = json.loads(config_raw)
    print(config)


if __name__ == "__main__":
    main()
