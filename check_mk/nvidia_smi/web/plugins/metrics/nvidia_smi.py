# Colors:
#
#                   red
#  magenta                       orange
#            11 12 13 14 15 16
#         46                   21
#         45                   22
#   blue  44                   23  yellow
#         43                   24
#         42                   25
#         41                   26
#            36 35 34 33 32 31
#     cyan                       yellow-green
#                  green
#
# Special colors:
# 51  gray
# 52  brown 1
# 53  brown 2
#
# For a new metric_info you have to choose a color. No more hex-codes are needed!
# Instead you can choose a number of the above color ring and a letter 'a' or 'b
# where 'a' represents the basic color and 'b' is a nuance/shading of the basic color.
# Both number and letter must be declared!
#
# Example:
# "color" : "23/a" (basic color yellow)
# "color" : "23/b" (nuance of color yellow)
#
# As an alternative you can call indexed_color with a color index and the maximum
# number of colors you will need to generate a color. This function tries to return
# high contrast colors for "close" indices, so the colors of idx 1 and idx 2 may
# have stronger contrast than the colors at idx 3 and idx 10.

metric_info["gpu_utilization"] = {
    "title" : _("GPU utilization"),
    "unit"  : "%",
    "color" : "31/a",
}

graph_info.append({
    "title"   : _("GPU utilization"),
    "metrics" : [
        ( "gpu_utilization", "area" ),
    ],
})

metric_info["temperature"] = {
    "title" : _("Temperature(C)"),
    "unit"  : "",
    "color" : "41/b",
}

graph_info.append({
    "title"   : _("Temperature(C)"),
    "metrics" : [
        ( "temperature", "line" ),
    ],
})

metric_info["memory_util"] = {
    "title" : _("Memory utilization"),
    "unit"  : "%",
    "color" : "21/b",
}

graph_info.append({
    "title"   : _("Memory utilization"),
    "metrics" : [
        ( "memory_util", "line" ),
    ],
})

metric_info["gpu_fb_memory_usage_used"] = {
    "title" : _("Memory used"),
    "unit"  : "bytes",
    "color" : "21/b",
}

graph_info.append({
    "title"   : _("Memory used"),
    "metrics" : [
        ( "gpu_fb_memory_usage_used", "line" ),
    ],
})

metric_info["sm_clock"] = {
    "title" : _("SM Clock"),
    "unit"  : "",
    "color" : "21/b",
}

metric_info["msm_clock"] = {
    "title" : _("MSM Clock"),
    "unit"  : "",
    "color" : "31/b",
}

metric_info["graphics_clock"] = {
    "title" : _("Graphics Clock"),
    "unit"  : "",
    "color" : "45/a",
}

graph_info.append({
    "title"   : _("Clocks"),
    "metrics" : [
        ( "msm_clock", "line" ),
        ( "graphics_clock", "line" ),
        ( "sm_clock", "line" ),
    ],
})

