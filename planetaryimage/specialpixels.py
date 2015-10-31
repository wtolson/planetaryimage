# -*- coding: utf-8 -*-
import collections
import numpy


SpecialPixles = collections.namedtuple('SpecialPixles', [
    'min',   # The minimum valid value for a pixel.
    'null',  # Pixel has no data available.
    'lrs',   # Pixel was lower bound saturated on the instrument.
    'lis',   # Pixel was higher bound saturated on the instrument.
    'his',   # Pixel was lower bound saturated during a computation.
    'hrs',   # Pixel was higher bound saturated during a computation.
    'max',   # The maximum valid value for a pixel.
])


DEFAULT_SPECIAL_PIXLES = SpecialPixles(
    min=numpy.NINF,
    null=numpy.nan,
    lrs=numpy.NINF,
    lis=numpy.NINF,
    his=numpy.inf,
    hrs=numpy.inf,
    max=numpy.inf,
)
