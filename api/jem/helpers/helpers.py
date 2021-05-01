"""helpers.py
Desc: General functions used to help with the rest of Jem code

"""

def get_bit_value(bit):
    """Shift 1 to the right according to bits value"""
    return 1 << (bit)

def to_int16(value):
    return hex(value & 0xffff)

def constrain(x, a, b):
    if x < a:
        return a
    elif b < x:
        return b
    else:
        return x
