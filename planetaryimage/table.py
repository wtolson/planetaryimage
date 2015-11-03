# -*- coding: utf-8 -*-


class Table(object):
    def __init__(self, name, data, meta=None):
        self.name = name
        self.data = data
        self.meta = meta
