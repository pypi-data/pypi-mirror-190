#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2023 Iñaki Amatria-Barral
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from lpi_prediction.lpi_model import LPIModel

from lpi_prediction.lpi_predictor import LPIPredictor

from lpi_prediction.lpi_data_encoder import LPIDataEncoder

from lpi_prediction.lpi_data_provider import LPIDataProvider
from lpi_prediction.lpi_data_provider import LPILabelsProvider
from lpi_prediction.lpi_data_provider import LPIFASTAFileProvider

from lpi_prediction.__about__ import __package_name__
from lpi_prediction.__about__ import __title__
from lpi_prediction.__about__ import __description__
from lpi_prediction.__about__ import __version__
from lpi_prediction.__about__ import __date__
from lpi_prediction.__about__ import __license__
from lpi_prediction.__about__ import __copyright__
from lpi_prediction.__about__ import __author__
from lpi_prediction.__about__ import __email__

__all__ = [
    'LPIModel',
    'LPIPredictor',
    'LPIDataEncoder',
    'LPIDataProvider',
    'LPILabelsProvider',
    'LPIFASTAFileProvider',
    '__package_name__',
    '__title__',
    '__description__',
    '__version__',
    '__date__',
    '__license__',
    '__copyright__',
    '__author__',
    '__email__'
]
