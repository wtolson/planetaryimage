# -*- coding: utf-8 -*-
import abc
import six


class DecoderPlugin(six.with_metaclass(abc.ABCMeta, object)):
    def __init__(self, stream, filename=None):
        self.stream = stream
        self.filename = filename

    @abc.abstractmethod
    def accept(self):
        return False

    @abc.abstractmethod
    def decode(self):
        pass


class EncoderPlugin(six.with_metaclass(abc.ABCMeta, object)):
    def __init__(self, stream):
        self.stream = stream

    @abc.abstractmethod
    def encode(self, image):
        pass
