#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2016             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

def nvidia_smi_parse(info):

    data = {}
    for i, line in enumerate(info):
        if len(line) != 4:
            continue # Skip unexpected lines
        pool_name, pm_type, metric, value = line
        if value == 'None':
            continue
        item = '%s [%s]' % (pool_name, pm_type)
        if item not in data:
            data[item] = {}

        data[item][metric] = int(value)

    return data


def inventory_nvidia_smi(info):
    data = nvidia_smi_parse(info)
    inv = []
    for item in data.keys():
        inv.append((item, {}))
    return inv


def check_nvidia_smi(item, params, info):
    if params is None:
        params = {}

    all_data = nvidia_smi_parse(info)
    if item not in all_data:
        return 3, 'Unable to find instance in agent output'
    data = all_data[item]

    perfkeys = [
        'gpu_utilization', 'memory_util', 'temperature',
        'graphics_clock', 'msm_clock', 'sm_clock',
        'gpu_fb_memory_usage_used'
    ]
    # Add some more values, derived from the raw ones...
    this_time = int(time.time())
    # for key in ['accepted_conn', 'max_children_reached', 'slow_requests']:
    #    per_sec = get_rate("nginx_status.%s" % key, this_time, data[key])
    #    data['%s_per_sec' % key] = per_sec
    #    perfkeys.append('%s_per_sec' % key)

    perfdata = []
    for i, key in enumerate(perfkeys):
        try:
            reading = data[key]
            perfdata.append( (key, data[key]) )
        except KeyError:
            pass
    perfdata.sort()

    worst_state = 0

    try:
        proc_warn, proc_crit = params.get('gpu_utilization', (None, None))
        proc_txt = ''
        if proc_crit is not None and data['gpu_utilization'] > proc_crit:
            worst_state = max(worst_state, 2)
            proc_txt = ' (!!)'
        elif proc_warn is not None and data['gpu_utilization'] > proc_warn:
            worst_state = max(worst_state, 1)
            proc_txt = ' (!)'
    except KeyError:
        worst_state = 0
        proc_txt = ''

    # output = [
    #    'Active: %d%s (%d idle, %d waiting)' % (
    #        data['gpu_utilization'], proc_txt, data['gpu_fb_memory_usage_used'], data['temperature'],
    #    ),
    #    'Started %s ago' % (get_age_human_readable(data['graphics_clock'])),
    #    'Requests: %0.2f/s' % (data['msm_clock']),
    # ]

    if 'gpu_utilization' in data and 'gpu_fb_memory_usage_used' in data and 'temperature' in data:
        mem_used_MiB = data['gpu_fb_memory_usage_used'] / (1024*1024)
        mem_total_MiB = data['gpu_fb_memory_usage_total'] / (1024*1024)
        output = [
            'GPU util: %d%%%s, memory used: %d MiB of %d MiB, temperature %dC' % (
                data['gpu_utilization'], proc_txt, mem_used_MiB, mem_total_MiB, data['temperature'],
            ),
        ]
    else:
        output = [ 'Too few data from nvidia-smi, assuming GPU is OK', ]

    return worst_state, ', '.join(output), perfdata

check_info['nvidia_smi'] = {
    "check_function" :      check_nvidia_smi,
    "inventory_function" :  inventory_nvidia_smi,
    "service_description" : "GPU nVidia Status %s",
    "has_perfdata" :        True,
    "group" :               "nvidia_smi"
}

