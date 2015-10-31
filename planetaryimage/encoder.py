# -*- coding: utf-8 -*-
import six
import os.path

from .files import open_file


class Encoder(object):
    encoders_by_extension = {}
    encoders_by_mime = {}

    @classmethod
    def register_extension(cls, extension, encoder):
        cls.encoders_by_extension[extension] = encoder

    @classmethod
    def register_mime(cls, mime, encoder):
        cls.encoders_by_mime[mime] = encoder

    def __init__(self, overwrite=False, compression='infer', encoder=None):
        self.overwrite = overwrite
        self.compression = compression

        if isinstance(encoder, six.string_types):
            try:
                self.encoder = self.encoders_by_mime[encoder]
            except KeyError:
                raise ValueError('Unknown encoder type %r' % encoder)
        else:
            self.encoder = encoder

    def encode(self, image, filename_or_stream, **kwargs):
        if not isinstance(filename_or_stream, six.string_types):
            return self._encode(image, filename_or_stream, **kwargs)

        if not self.overwrite and os.path.isfile(filename_or_stream):
            raise IOError('file %r already exists' % filename_or_stream)

        with open_file(filename_or_stream, 'wb') as stream:
            return self._encode(image, stream, filename=filename_or_stream, **kwargs)

    def _get_encoder(self, stream, filename):
        if self.encoder:
            return self.encoder(stream)

        if not filename:
            raise ValueError('filename required to detect encoder')

        for extension in reversed(os.path.basename(filename).split('.')):
            try:
                decoder = self.encoders_by_extension[extension]
            except KeyError:
                continue

            return decoder(stream)

        raise ValueError('Unknown encoding for %r' % filename)

    def _encode(self, image, stream, filename=None, **kwargs):
        return self._get_encoder(stream, filename).encode(image, **kwargs)
