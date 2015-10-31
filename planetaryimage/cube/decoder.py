# -*- coding: utf-8 -*-
import os.path
import pvl

from ..decoder import Decoder
from ..deocorators import cached_property
from ..files import open_file
from ..image import Image
from ..pixeldecoder import BandSequentialDecoder, TileDecoder
from ..plugin import DecoderPlugin

from .byteorder import CUBE_TO_NUMPY_BYTEORDER
from .pixeltypes import CUBE_TO_NUMPY_PIXEL_TYPES
from .specialpixels import SPECIAL_PIXELS


class CubeDecoder(DecoderPlugin):
    """A Isis Cube file reader."""

    @cached_property
    def label(self):
        return pvl.load(self.stream)

    @property
    def shape(self):
        return (self.bands, self.lines, self.samples)

    @property
    def bands(self):
        return self.label['IsisCube']['Core']['Dimensions']['Bands']

    @property
    def lines(self):
        return self.label['IsisCube']['Core']['Dimensions']['Lines']

    @property
    def samples(self):
        return self.label['IsisCube']['Core']['Dimensions']['Samples']

    @property
    def format(self):
        return self.label['IsisCube']['Core']['Format']

    @property
    def start_byte(self):
        return self.label['IsisCube']['Core']['StartByte'] - 1

    @property
    def dtype(self):
        return self._pixel_type.newbyteorder(self._byte_order)

    @property
    def base(self):
        return self.label['IsisCube']['Core']['Pixels']['Base']

    @property
    def multiplier(self):
        return self.label['IsisCube']['Core']['Pixels']['Multiplier']

    @property
    def tile_lines(self):
        if self.format != 'Tile':
            return None
        return self.label['IsisCube']['Core']['TileLines']

    @property
    def tile_samples(self):
        if self.format != 'Tile':
            return None
        return self.label['IsisCube']['Core']['TileSamples']

    @property
    def tile_shape(self):
        if self.format != 'Tile':
            return None
        return (self.tile_lines, self.tile_samples)

    @property
    def _byte_order(self):
        return CUBE_TO_NUMPY_BYTEORDER[self._pixels_group['ByteOrder']]

    @property
    def _pixels_group(self):
        return self.label['IsisCube']['Core']['Pixels']

    @property
    def _pixel_type(self):
        return CUBE_TO_NUMPY_PIXEL_TYPES[self._pixels_group['Type']]

    @property
    def specials(self):
        pixel_type = self._pixels_group['Type']
        return SPECIAL_PIXELS[pixel_type]

    @property
    def data_filename(self):
        """Return detached filename else None."""
        return self.label['IsisCube']['Core'].get('^Core')

    @property
    def _decoder(self):
        if self.format == 'BandSequential':
            return BandSequentialDecoder(self.dtype, self.shape)

        if self.format == 'Tile':
            return TileDecoder(self.dtype, self.shape, self.tile_shape)

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
            return bool(self.label['IsisCube'])
        except:  # TODO: log errors
            return False

    def decode(self):
        return Image(
            bands=self.decode_bands(),
            label=self.label,
            filename=self.filename,
            base=self.base,
            multiplier=self.multiplier,
            specials=self.specials,
        )


# Register plugin
Decoder.register(CubeDecoder)
