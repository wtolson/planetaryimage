# -*- coding: utf-8 -*-
import numpy

from .decoder import Decoder
from .encoder import Encoder
from .specialpixels import DEFAULT_SPECIAL_PIXLES


class Image(object):
    @classmethod
    def open(cls, filename_or_stream, compression='infer', decoder=None, **kwargs):
        """ Read an image file from disk

        Parameters
        ----------
        filename : string
            Name of file to read as an image file.  This file may be gzip
            (``.gz``) or bzip2 (``.bz2``) compressed.
        """
        return Decoder(compression, decoder).decode(filename_or_stream, **kwargs)

    def save(self, filename_or_stream, overwrite=False, compression='infer',
             encoder=None, **kwargs):
        return Encoder(overwrite, compression, encoder).encode(self, filename_or_stream, **kwargs)

    def __init__(self, bands, label=None, filename=None, base=0, multiplier=1,
                 specials=DEFAULT_SPECIAL_PIXLES):
        """Create an Image object.

        Parameters
        ----------

        stream
            file object to read as an image file

        filename : string
            an optional filename to attach to the object
        """

        #: A numpy array representing the image bands
        self.bands = bands

        # TODO: rename to header and add footer?
        #: The parsed label header in dictionary form.
        self.label = label

        #: The filename if given, otherwise none.
        self.filename = filename

        #: An additive factor by which to offset pixel DN.
        self.base = base

        #: A multiplicative factor by which to scale pixel DN.
        self.multiplier = multiplier

        #: Special pixel values.
        self.specials = specials

    def __repr__(self):
        if self.filename:
            return '<%s %r>' % (type(self).__name__, self.filename)
        return super(Image, self).__repr__()

    @property
    def pixels(self):
        """An Image like array of ``self.bands`` convenient for image processing tasks

        * 2D array for single band, grayscale image data
        * 3D array for three band, RGB image data

        Enables working with ``self.bands`` as if it were a PIL image::

         >>> from planetaryimage import PDS3Image
         >>> import matplotlib.pyplot as plt
         >>> testfile = 'tests/mission_data/2p129641989eth0361p2600r8m1.img'
         >>> image = PDS3Image.open(testfile)
         >>> _ = plt.imshow(image.image, cmap='gray')
        """
        if len(self.bands) == 1:
            return self.bands[0]

        if len(self.bands) in (3, 4):
            return numpy.dstack(self.bands)

        # TODO: what about multiband images with 2, and 5+ bands?
        raise ValueError('pixel axis only valid for 1, 3 or 4 bands')

    def apply_scaling(self, copy=True):
        """Scale pixel values to there true DN.

        :param copy: whether to apply the scaling to a copy of the pixel data
            and leave the original unaffected

        :returns: a scaled version of the pixel data
        """
        if copy:
            return self.multiplier * self.bands + self.base

        if self.multiplier != 1:
            self.bands *= self.multiplier

        if self.base != 0:
            self.bands += self.base

        return self.bands

    def convert_specials(self, copy=True):
        """Convert special pixel values to numpy special pixel values.

            =======  =======
             Type     Numpy
            =======  =======
            null     nan
            lrs      -inf
            lis      -inf
            his      inf
            hrs      inf
            =======  =======

        :param copy: whether to apply the new special values to a copy of the
            pixel data and leave the original unaffected

        :returns: a numpy array with special values converted to numpy's nan,
            inf and -inf
        """
        if copy:
            data = self.bands.astype(numpy.float64)

        elif self.bands.dtype != numpy.float64:
            data = self.bands = self.bands.astype(numpy.float64)

        else:
            data = self.bands

        data[data == self.specials.null] = numpy.nan
        data[data < self.specials.min] = numpy.NINF
        data[data > self.specials.max] = numpy.inf

        return data

    def specials_mask(self):
        """Create a pixel map for special pixels.

        :returns: an array where the value is `False` if the pixel is special
            and `True` otherwise
        """
        mask = self.bands >= self.specials.min
        mask &= self.bands <= self.specials.max
        return mask
