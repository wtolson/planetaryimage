# -*- coding: utf-8 -*-
import io
import six

from .files import open_file


class Decoder(object):
    decoders = []

    @classmethod
    def register(cls, decoder):
        cls.decoders.append(decoder)

    def __init__(self, compression='infer', decoder=None):
        self.compression = compression
        self.decoder = decoder

    def decode(self, filename_or_stream, **kwargs):
        if not isinstance(filename_or_stream, six.string_types):
            return self._decode(filename_or_stream, **kwargs)

        with open_file(filename_or_stream) as stream:
            return self._decode(stream, filename=filename_or_stream, **kwargs)

    def _get_decoder(self, stream, filename):
        if self.decoder:
            return self.decoder(stream, filename)

        for decoder in self.decoders:
            decoder = decoder(stream, filename)
            if decoder.accept():
                return decoder
            stream.seek(0)

        raise ValueError('Unknown encoding for %r' % (filename or stream))

    def _decode(self, stream, filename=None, **kwargs):
        try:
            stream.seek(0)
        except (AttributeError, io.UnsupportedOperation):
            stream = io.BytesIO(stream.read())

        return self._get_decoder(stream, filename).decode(**kwargs)
