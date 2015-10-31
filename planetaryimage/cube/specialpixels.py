# -*- coding: utf-8 -*-
import numpy
from ..specialpixels import SpecialPixles


def _make_num(num, dtype):
    return numpy.fromstring(num, dtype=dtype)[0]


SPECIAL_PIXELS = {
    'UnsignedByte': SpecialPixles(
        min=1,
        null=0,
        lrs=0,
        lis=0,
        his=255,
        hrs=255,
        max=254,
    ),

    'UnsignedWord': SpecialPixles(
        min=3,
        null=0,
        lrs=1,
        lis=2,
        his=65534,
        hrs=65535,
        max=65522,
    ),

    'SignedWord': SpecialPixles(
        min=-32752,
        null=-32768,
        lrs=-32767,
        lis=-32766,
        his=-32765,
        hrs=-32764,
        max=32767,
    ),

    'SignedInteger': SpecialPixles(
        min=-8388614,
        null=-8388613,
        lrs=-8388612,
        lis=-8388611,
        his=-8388610,
        hrs=-8388609,
        max=2147483647,
    ),

    'Real': SpecialPixles(
        min=_make_num(b'\xFF\x7F\xFF\xFA', '>f4'),
        null=_make_num(b'\xFF\x7F\xFF\xFB', '>f4'),
        lrs=_make_num(b'\xFF\x7F\xFF\xFC', '>f4'),
        lis=_make_num(b'\xFF\x7F\xFF\xFD', '>f4'),
        his=_make_num(b'\xFF\x7F\xFF\xFE', '>f4'),
        hrs=_make_num(b'\xFF\x7F\xFF\xFF', '>f4'),
        max=numpy.finfo('f4').max,
    ),

    'Double': SpecialPixles(
        min=_make_num(b'\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFA', '>f8'),
        null=_make_num(b'\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFB', '>f8'),
        lrs=_make_num(b'\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFC', '>f8'),
        lis=_make_num(b'\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFD', '>f8'),
        his=_make_num(b'\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFE', '>f8'),
        hrs=_make_num(b'\xFF\xEF\xFF\xFF\xFF\xFF\xFF\xFF', '>f8'),
        max=numpy.finfo('f8').max,
    ),
}
