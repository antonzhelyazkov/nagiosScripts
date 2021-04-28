#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import NamedTuple, Optional
from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    HostLabelGenerator,
    StringTable,
    InventoryResult,
)

from .agent_based_api.v1 import (
    Attributes,
    exists,
    HostLabel,
    register,
    Result,
    Service,
    SNMPTree,
    State,
)

from .utils.device_types import is_fibrechannel_switch, SNMPDeviceType


class SNMPInfo(NamedTuple):
    description: str
    status: str


def _parse_string(val):
    return val.strip().replace("\r\n", " ").replace("\n", " ")


def parse_snmp_info(string_table: StringTable) -> Optional[SNMPInfo]:
    if not string_table:
        return None
    snmp_info = [_parse_string(s) for s in string_table[0]]
    return SNMPInfo(*snmp_info)


def host_label_snmp_info(section: SNMPInfo) -> HostLabelGenerator:
    for device_type in SNMPDeviceType:
        if device_type.name in section.description.upper():
            if device_type is SNMPDeviceType.SWITCH and is_fibrechannel_switch(section.description):
                yield HostLabel("cmk/device_type", "fcswitch")
            else:
                yield HostLabel("cmk/device_type", device_type.name.lower())
            return


register.snmp_section(
    name="acronis_info",
    parse_function=parse_snmp_info,
    host_label_function=host_label_snmp_info,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.8072.161.1.1",
        oids=["1.0", "2.0"],
    ),
    detect=exists(".1.3.6.1.2.1.1.1.0"),
)


def discover_snmp_info(section: SNMPInfo) -> DiscoveryResult:
    yield Service()


def check_snmp_info(section: SNMPInfo) -> CheckResult:
    summary_string=f"{section.status}"
    details_string=f"{section.description}, {section.status}"
    if section.status == "healthy":
        yield Result(
            state=State.OK,
            summary=summary_string,
            details=details_string,
        )
    else:
        yield Result(
            state=State.WARN,
            summary=summary_string,
            details=details_string,
        )


register.check_plugin(
    name="acronis_info",
    service_name="Acronis Info",
    discovery_function=discover_snmp_info,
    check_function=check_snmp_info,
)


def inventory_snmp_info(section: SNMPInfo) -> InventoryResult:
    yield Attributes(path=["hardware", "system"],
                     inventory_attributes={
                         "product": section.description,
                     })

    yield Attributes(path=["software", "configuration", "snmp_info"],
                     inventory_attributes={
                         "status": section.status,
                     })


register.inventory_plugin(
    name="acronis_info",
    inventory_function=inventory_snmp_info,
)
