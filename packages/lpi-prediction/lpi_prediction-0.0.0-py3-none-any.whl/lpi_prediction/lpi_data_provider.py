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

class LPIDataProvider:
    def load(self):
        raise NotImplementedError()

class LPILabelsProvider(LPIDataProvider):
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        labels = []
        with open(self.file_name, 'r') as f:
            for line in f:
                line = line.strip().split()
                labels.append(int(line[2]))

        return labels

class LPIFASTAFileProvider(LPIDataProvider):
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        names, sequences = [], []
        with open(self.file_name) as f:
            for line in f:
                if line[0] == '>':
                    names.append(line[1:].strip())
                    sequences.append('')
                else:
                    sequences[-1] += line.strip()
        return names, sequences
