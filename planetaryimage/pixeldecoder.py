# -*- coding: utf-8 -*-
import numpy
from six.moves import range


class BandSequentialDecoder(object):
    def __init__(self, dtype, shape):
        self.dtype = dtype
        self.shape = shape

    def decode(self, stream):
        if hasattr(stream, 'readinto'):
            data = numpy.empty(self.shape, dtype=self.dtype)
            stream.readinto(data.data)
        else:
            size = numpy.product(self.shape) * self.dtype.itemsize
            data = numpy.fromstring(stream.read(size), dtype=self.dtype)
            data = data.reshape(self.shape)

        return data


class TileDecoder(object):
    def __init__(self, dtype, shape, tile_shape):
        self.dtype = dtype
        self.shape = shape
        self.tile_shape = tile_shape

    def decode(self, stream):
        bands, lines, samples = self.shape
        tile_lines, tile_samples = self.tile_shape
        tile_size = tile_lines * tile_samples * self.dtype.itemsize
        data = numpy.empty(self.shape, dtype=self.dtype)

        for band in data:
            for line in range(0, lines, tile_lines):
                for sample in range(0, samples, tile_samples):
                    sample_end = sample + tile_samples
                    line_end = line + tile_lines
                    chunk = band[line:line_end, sample:sample_end]

                    tile_data = stream.read(tile_size)
                    tile = numpy.fromstring(tile_data, dtype=self.dtype)
                    tile = tile.reshape((tile_lines, tile_samples))

                    chunk_lines, chunk_samples = chunk.shape
                    chunk[:] = tile[:chunk_lines, :chunk_samples]

        return data
