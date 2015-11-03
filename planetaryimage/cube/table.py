# -*- coding: utf-8 -*-
import numpy
import pvl

from ..table import Table
from .byteorder import CUBE_TO_NUMPY_BYTEORDER


FIELD_TYPES = {
    'Text': 'S',
    'Integer': 'i4',
    'Real': 'f4',
    'Double': 'f8',
}


class Field(object):
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size

    @property
    def dtype(self):
        try:
            fixed_dtype = FIELD_TYPES[self.type]
        except AttributeError:
            raise ValueError('Invalid field type %r.' % self.type)

        return (self.name.encode('utf-8'), fixed_dtype, self.size)


class TableDecoder(object):
    required_keys = (
        u'Name',
        u'StartByte',
        u'Bytes',
        u'Records',
        u'ByteOrder',
        u'Field',
    )

    def __init__(self, label, stream):
        self.label = label
        self.stream = stream

    @property
    def name(self):
        return self.label['Name']

    @property
    def meta(self):
        meta = [(k, v) for k, v in self.label if k not in self.required_keys]
        return pvl.PVLObject(meta)

    @property
    def byte_order(self):
        return CUBE_TO_NUMPY_BYTEORDER[self.label['ByteOrder']]

    @property
    def dtype(self):
        columns = [field.dtype for field in self.get_fields()]
        return numpy.dtype(columns).newbyteorder(self.byte_order)

    def get_fields(self):
        # TODO: get byte order (ByteOrder)
        for field in self.label.getlist('Field'):
            yield Field(
                name=field['Name'],
                type=field['Type'],
                size=field['Size'],
            )

    def decode_data(self):
        self.stream.seek(self.label['StartByte'] - 1)
        raw_data = self.stream.read(self.label['Bytes'])
        return numpy.fromstring(raw_data, dtype=self.dtype)

    def decode(self):
        return Table(
            name=self.name,
            data=self.decode_data(),
            meta=self.meta,
        )
