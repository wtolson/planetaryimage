# -*- coding: utf-8 -*-
import six
import numpy


CUBE_TO_NUMPY_PIXEL_TYPES = {
    'UnsignedByte': numpy.dtype('uint8'),
    'SignedByte': numpy.dtype('int8'),
    'UnsignedWord': numpy.dtype('uint16'),
    'SignedWord': numpy.dtype('int16'),
    'UnsignedInteger': numpy.dtype('uint32'),
    'SignedInteger': numpy.dtype('int32'),
    'Real': numpy.dtype('float32'),
    'Double': numpy.dtype('float64')
}

NUMPY_TO_CUBE_PIXEL_TYPES = dict((v, k) for k, v in six.iteritems(CUBE_TO_NUMPY_PIXEL_TYPES))
