# -*- coding: utf-8 -*-
import gzip
import bz2


class ContextManagerMixin(object):
    def __enter__(self):
        try:
            return super(ContextManagerMixin, self).__enter__()
        except AttributeError:
            return self

    def __exit__(self, *args):
        try:
            return super(ContextManagerMixin, self).__exit__(*args)
        except AttributeError:
            self.close()


class BZ2File(ContextManagerMixin, bz2.BZ2File):
    pass


class GzipFile(ContextManagerMixin, gzip.GzipFile):
    pass


def open_file(filename, mode='rb', compression='infer'):
    if compression == 'infer':
        if filename.lower().endswith('.gz'):
            compression = 'gzip'

        elif filename.lower().endswith('.bz2'):
            compression = 'bz2'

        else:
            compression = None

    if not compression:
        return open(filename, mode)

    if compression == 'gzip':
        return GzipFile(filename, mode)

    if compression == 'bz2':
        return BZ2File(filename, mode)

    raise ValueError('Unknown compression %r' % compression)
