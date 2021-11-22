from .agent_based_api.v1 import *
import pprint


def discover_nvidia(section):
    for sector, used, slots in section:
        yield Service(item=sector)


def check_nvidia(item, section):
    for sector, used, slots in section:
        if sector == item:
            used = int(used)    # convert string to int
            slots = int(slots)  # convert string to int
            if used == slots:
                s = State.CRIT
            elif slots - used <= 10:
                s = State.WARN
            else:
                s = State.OK
            yield Result(
                state = s,
                summary = f"used {used} of {slots}")
            yield Metric('gpumem', used, levels=(90, None), boundaries=(0,100))
            return


register.check_plugin(
    name = "nvidia_gpu",
    service_name = "GPU %s",
    discovery_function = discover_nvidia,
    check_function = check_nvidia,
)
