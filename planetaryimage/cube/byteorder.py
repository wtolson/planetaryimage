# -*- coding: utf-8 -*-
import sys


if sys.byteorder == 'little':
    SYS_BYTEORDER = 'Lsb'
else:
    SYS_BYTEORDER = 'Msb'

NUMPY_TO_CUBE_BYTEORDER = {
    '=': SYS_BYTEORDER,  # system
    '<': 'Lsb',          # little-endian
    '>': 'Msb',          # big-endian
}

CUBE_TO_NUMPY_BYTEORDER = {
    'NoByteOrder': '=',  # system
    'Lsb': '<',          # little-endian
    'Msb': '>'           # big-endian
}
