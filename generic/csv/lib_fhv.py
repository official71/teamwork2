import re

def expiration_date(v):
    if not v: return "EXPIRE_NONE"
    [m, d, y] = v.split('/')
    return "EXPIRE_{}_{}".format(y, m)

def wheelchair_accessible(v):
    if v == "WAV": return "WHEELCHAIR_ACCESS"
    return "WHEELCHAIR_NONE"

def certification_date(v):
    if not v: return "CERTIFICATE_NONE"
    [m, d, y] = v.split('/')
    return "CERTIFICATE_" + y

def hack_up_date(v):
    if not v: return "HACK_UP_NONE"
    [m, d, y] = v.split('/')
    return "HACK_UP_" + y

def base_address(v):
    if not v: return "BASE_POSTCODE_NONE"
    l = v.split(' ')[-1]
    if not re.match(r'^\d{5}$', l):
        return "BASE_POSTCODE_NONE"
    else:
        return "BASE_POSTCODE_" + l

