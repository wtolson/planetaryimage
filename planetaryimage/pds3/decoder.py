# -*- coding: utf-8 -*-
import os.path

import numpy
import pvl

from ..decoder import Decoder
from ..deocorators import cached_property
from ..files import open_file
from ..image import Image
from ..pixeldecoder import BandSequentialDecoder
from ..plugin import DecoderPlugin

from .pointer import Pointer


class PDS3Decoder(DecoderPlugin):
    SAMPLE_TYPES = {
        'MSB_INTEGER': '>i',
        'INTEGER': '>i',
        'MAC_INTEGER': '>i',
        'SUN_INTEGER': '>i',

        'MSB_UNSIGNED_INTEGER': '>u',
        'UNSIGNED_INTEGER': '>u',
        'MAC_UNSIGNED_INTEGER': '>u',
        'SUN_UNSIGNED_INTEGER': '>u',

        'LSB_INTEGER': '<i',
        'PC_INTEGER': '<i',
        'VAX_INTEGER': '<i',

        'LSB_UNSIGNED_INTEGER': '<u',
        'PC_UNSIGNED_INTEGER': '<u',
        'VAX_UNSIGNED_INTEGER': '<u',

        'IEEE_REAL': '>f',
        'FLOAT': '>f',
        'REAL': '>f',
        'MAC_REAL': '>f',
        'SUN_REAL': '>f',

        'IEEE_COMPLEX': '>c',
        'COMPLEX': '>c',
        'MAC_COMPLEX': '>c',
        'SUN_COMPLEX': '>c',

        'PC_REAL': '<f',
        'PC_COMPLEX': '<c',

        'MSB_BIT_STRING': '>S',
        'LSB_BIT_STRING': '<S',
        'VAX_BIT_STRING': '<S',
    }

    @cached_property
    def label(self):
        return pvl.load(self.stream)

    @property
    def dtype(self):
        return numpy.dtype('%s%d' % (self._sample_type, self._sample_bytes))

    @property
    def shape(self):
        return (self.bands, self.lines, self.samples)

    @property
    def bands(self):
        return self.label['IMAGE'].get('BANDS', 1)

    @property
    def lines(self):
        return self.label['IMAGE']['LINES']

    @property
    def samples(self):
        return self.label['IMAGE']['LINE_SAMPLES']

    @property
    def format(self):
        return self.label['IMAGE'].get('format', 'BAND_SEQUENTIAL')

    @property
    def start_byte(self):
        return self._image_pointer.bytes

    @property
    def data_filename(self):
        return self._image_pointer.filename

    @property
    def record_bytes(self):
        """Number of bytes for fixed length records."""
        return self.label.get('RECORD_BYTES', 0)

    @property
    def _image_pointer(self):
        return Pointer.parse(self.label['^IMAGE'], self.record_bytes)

    @property
    def _sample_type(self):
        sample_type = self.label['IMAGE']['SAMPLE_TYPE']
        try:
            return self.SAMPLE_TYPES[sample_type]
        except KeyError:
            raise ValueError('Unsupported sample type: %r' % sample_type)

    @property
    def _sample_bytes(self):
        # get bytes to match NumPy dtype expressions
        return int(self.label['IMAGE']['SAMPLE_BITS'] / 8)

    @property
    def _decoder(self):
        if self.format == 'BAND_SEQUENTIAL':
            return BandSequentialDecoder(self.dtype, self.shape)

        raise ValueError('Unkown format (%s)' % self.format)

    def _decode(self, stream):
        stream.seek(self.start_byte)
        return self._decoder.decode(stream)

    def _decode_detached_data(self, filename):
        if self.filename:
            dirpath = os.path.dirname(self.filename)
            filename = os.path.abspath(os.path.join(dirpath, filename))

        with open_file(filename, 'rb') as stream:
            return self._decode(stream)

    def decode_bands(self):
        if self.data_filename:
            return self._decode_detached_data(self.data_filename)
        return self._decode(self.stream)

    def accept(self):
        try:
            return self.label['PDS_VERSION_ID'] == 'PDS3'
        except:  # TODO: log errors
            return False

    def decode(self):
        return Image(
            bands=self.decode_bands(),
            label=self.label,
            filename=self.filename,
        )


# Register plugin
Decoder.register(PDS3Decoder)
