# -*- coding: utf-8 -*-
import six
import pvl
import collections


class Pointer(collections.namedtuple('Pointer', ['filename', 'bytes'])):
    @staticmethod
    def _parse_bytes(value, record_bytes):
        if isinstance(value, six.integer_types):
            return (value - 1) * record_bytes

        if isinstance(value, pvl.Units) and value.units == 'BYTES':
            return value.value

        raise ValueError('Unsupported pointer type')

    @classmethod
    def parse(cls, value, record_bytes):
        """Parses the pointer label.

        Parameters
        ----------
        pointer_data
            Supported values for `pointer_data` are::

                ^PTR = nnn
                ^PTR = nnn <BYTES>
                ^PTR = "filename"
                ^PTR = ("filename")
                ^PTR = ("filename", nnn)
                ^PTR = ("filename", nnn <BYTES>)

        record_bytes
            Record multiplier value

        Returns
        -------
        Pointer object
        """
        if isinstance(value, six.string_types):
            return cls(value, 0)

        if isinstance(value, list):
            if len(value) == 1:
                return cls(value[0], 0)

            if len(value) == 2:
                return cls(value[0], cls._parse_bytes(value[1], record_bytes))

            raise ValueError('Unsupported pointer type')

        return cls(None, cls._parse_bytes(value, record_bytes))
