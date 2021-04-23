import os
import sys

CONFIG_FILE = f"/etc/check_mk/{os.path.basename(sys.argv[0])}"


def main():
    with open(CONFIG_FILE, 'r') as config_handler:
        config_raw = config_handler.read()

    print(config_raw)


if __name__ == "__main__":
    main()
