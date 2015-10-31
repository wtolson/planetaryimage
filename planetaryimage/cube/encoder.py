# -*- coding: utf-8 -*-
import pvl

from ..encoder import Encoder
from ..plugin import EncoderPlugin

from .byteorder import NUMPY_TO_CUBE_BYTEORDER
from .pixeltypes import NUMPY_TO_CUBE_PIXEL_TYPES


class CubeEncoder(EncoderPlugin):
    label_size = 65536
    label_encoder = pvl.encoder.IsisCubeLabelEncoder

    def get_pixel_type(self, image):
        return NUMPY_TO_CUBE_PIXEL_TYPES[image.bands.dtype.newbyteorder('=')]

    def get_byte_order(self, image):
        return NUMPY_TO_CUBE_BYTEORDER[image.bands.dtype.byteorder]

    def create_label(self, image):
        label = pvl.PVLModule(image.label)

        label['IsisCube'] = pvl.PVLObject({
            'Core': pvl.PVLObject({
                'StartByte': 0,
                'Format': 'BandSequential',

                'Dimensions': pvl.PVLGroup({
                    'Bands': image.bands.shape[0],
                    'Lines': image.bands.shape[1],
                    'Samples': image.bands.shape[2],
                }),

                'Pixels': pvl.PVLGroup({
                    'Type': self.get_pixel_type(image),
                    'ByteOrder': self.get_byte_order(image),
                    'Base': image.base,
                    'Multiplier': image.multiplier,
                })
            })
        })

        label['Label'] = pvl.PVLObject({
            'Bytes': 0,
        })

        return label

    def encode(self, image):
        label_size = self.label_size
        label = self.create_label(image)

        while True:
            label['IsisCube']['Core']['StartByte'] = label_size + 1
            label['Label']['Bytes'] = label_size

            label_data = pvl.dumps(label, cls=self.label_encoder)
            buffer_size = label_size - len(label_data)

            if buffer_size > 0:
                break

            label_chunks = (len(label_data) + 1) % self.label_size
            label_size = (label_chunks + 1) * self.label_size

        self.stream.write(label_data)
        self.stream.write(buffer_size * '\0')
        self.stream.write(image.bands.tostring())

        # TODO: convert nan, inf and -inf to special values
        # TODO: convert pds label?
        # TODO: handle trailing labels


# Register plugin
Encoder.register_extension('cub', CubeEncoder)
Encoder.register_extension('cube', CubeEncoder)
Encoder.register_mime('cube', CubeEncoder)
