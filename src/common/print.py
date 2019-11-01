# Print utilities
#
# src.common.print
#

import pprint
import src.common.semval as sm
import src.common.synval as sn
import src.common.synsem as ss

def GetPrintable(obj):

    if isinstance(obj, dict):
        return {k:GetPrintable(v) for (k,v) in obj.items()}
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [GetPrintable(x) for x in obj]
    elif isinstance(obj, set):
        return {GetPrintable(x) for x in obj}
    elif hasattr(obj, "ToPrint"):
        return obj.ToPrint()
    else:
        return obj

def p(obj):

    printable = GetPrintable(obj)
    pprint.pprint(printable)
