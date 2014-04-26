# -*- coding: utf-8 -*-

# Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
# See COPYING for license details.

from _pywfdb import *
import ecgcodes
EcgCodes = ecgcodes.EcgCodes
del ecgcodes

__all__ = ['EcgCodes']  + _pywfdb.__all__