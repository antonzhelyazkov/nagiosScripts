import argparse
import json
import logging
import os
import sys


class PidFileExists(Exception):
    pass


def add_slash(directory):
    if not directory.endswith("/"):
        dir_return = directory + "/"
    else:
        dir_return = directory
    return dir_return


def process_pid_file(pid_f: str) -> bool:
    if os.path.isfile(pid_f):
        raise PidFileExists
    else:
        try:
            with open(pid_f, "w") as pid:
                pid.write(str(os.getpid()))
                return True
        except IOError as e:
            raise IOError(e)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str, required=True, help="Path to config file", dest='config')
    parser.add_argument('-v', '--verbose', required=False, action='store_true', dest='verbose')

    args_cmd = parser.parse_args()
    config_file = args_cmd.config
    verbose = args_cmd.verbose

    config_open = open(config_file, encoding='utf-8')
    config_data = json.load(config_open)
    script_name = os.path.basename(sys.argv[0]).split(".")
    log_file = f"{add_slash(config_data['log_dir'])}{script_name[0]}.log"

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    if verbose:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    else:
        logger.addHandler(file_handler)

    pid_file = f"{add_slash(config_data['pid_file_path'])}{script_name[0]}.pid"
    nagios_file = f"{add_slash(config_data['pid_file_path'])}{script_name[0]}.nagios"
    try:
        process_pid_file(pid_file)
    except PidFileExists:
        logger.info(f"INFO pid file {pid_file} exists")
        sys.exit(1)
    except OSError as e:
        logger.exception(f"#### {e}")


if __name__ == "__main__":
    main()
