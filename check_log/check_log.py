import datetime
import argparse
import os
import re


TMP_BASE = '/tmp'

class CheckPhpLog:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--log', type=str, required=True, help="Path to log file", dest='log_file')
        parser.add_argument('-s', '--size', type=int, required=True, help="number of rows to process", dest='chunk_size')
        parser.add_argument('-w', '--warning', type=int, required=True, help="warning count", dest='warning')
        parser.add_argument('-c', '--critical', type=int, required=True, help="critical count", dest='critical')

        args_cmd = parser.parse_args()

        log_file = args_cmd.log_file
        chunk_size = args_cmd.chunk_size
        warning_count = args_cmd.warning
        critical_count = args_cmd.critical

        if warning_count > critical_count:
            print(f"ERROR warning must be less than critical {warning_count} {critical_count}")

        if not os.path.isfile(log_file):
            print(f"WARNING log file not found {log_file}")
            exit(1)

        tmp_log = os.path.join(TMP_BASE, os.path.basename(log_file))

        if os.path.isfile(tmp_log):
            with open(tmp_log, 'r') as tmp_log_handler:
                last_exec = tmp_log_handler.read()

            if not re.match(r'\d{10}', last_exec):
                last_exec = None
        else:
            last_exec = None

        with open(log_file, 'r', errors='ignore') as log_handler:
            log_read = log_handler.read()

        log_array = log_read.split('\n')
        regex_string = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s-\s-\s\[(\d{2}\/\w{3}\/\d{4}\:\d{2}\:\d{2}\:\d{2})\s\+\d{4}\]\s\".*\"\s(\d{3})')
        len_arr = len(log_array)

        i = True
        
        if len_arr < chunk_size:
            chunk_size = len_arr - 1

        if last_exec is None:
            row_position = 0
        else:
            chunk_size_base = chunk_size
            while i:
                item_l = len_arr - chunk_size
                # print(item_l, len_arr, chunk_size)
                date_object = regex_string.search(log_array[item_l])
                if date_object is None:
                    continue
                else:
                    row_date = date_object.group(1)
                    return_code = date_object.group(2)

                timestamp = int(datetime.datetime.strptime(row_date, "%d/%b/%Y:%H:%M:%S").timestamp())

                # print(row_date, timestamp, int(last_exec), datetime.datetime.fromtimestamp(int(last_exec)), return_code)
                if int(timestamp) > int(last_exec):
                    chunk_size += chunk_size_base
                else:
                    i = False
                    row_position = item_l
                
                if chunk_size > len_arr:
                    i = False
                    row_position = item_l

        # print(row_position, len_arr)

        count_500 = 0
        count_404 = 0
        count_403 = 0
        count_other = 0
        last_timestamp = None

        for item_r in range(row_position, len_arr):
            
            date_object = regex_string.search(log_array[item_r])
            if date_object is None:
                continue
            else:
                row_date = date_object.group(1)
                return_code = date_object.group(2)

            timestamp = int(datetime.datetime.strptime(row_date, "%d/%b/%Y:%H:%M:%S").timestamp())

            if int(return_code) == 500:
                count_500 += 1
            elif int(return_code) == 404:
                count_404 += 1
            elif int(return_code) == 403:
                count_403 += 1
            else:
                count_other += 1
            
            last_timestamp = timestamp

        # print(count_500, count_404, count_403, count_other, last_timestamp)
        
        with open(tmp_log, 'w') as write_timestamp:
            write_timestamp.write(str(last_timestamp))

        last_exec_date = datetime.datetime.fromtimestamp(last_timestamp)

        if count_500 < warning_count:
            print(f"OK no fatal errors found since {last_exec_date} | r500={count_500}; r404={count_404}; r403={count_403}")
            exit(0)
        elif warning_count <= count_500 < critical_count:
            print(f"WARNING {count_500} errors found since {last_exec_date} | r500={count_500}; r404={count_404}; r403={count_403}")
            exit(1)
        elif critical_count <= count_500:
            print(f"CRITICAL {count_500} errors found since {last_exec_date} | r500={count_500}; r404={count_404}; r403={count_403}")
            exit(2)
        else:
            print(f"UNKNOWN")
            exit(2)


if __name__ == '__main__':
    encoder = CheckPhpLog()

