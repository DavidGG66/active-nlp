# Print utilities
#
# src.common.print
#

import pprint

def get_printable(obj):

    if isinstance(obj, dict):
        return {k:get_printable(v) for (k,v) in obj.items()}
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [get_printable(x) for x in obj]
    elif isinstance(obj, set):
        return {get_printable(x) for x in obj}
    elif hasattr(obj, "to_print"):
        return obj.to_print()
    else:
        return obj

def p(obj):

    printable = get_printable(obj)
    pprint.pprint(printable)
