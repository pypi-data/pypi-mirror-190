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

class LPIPredictor:
    def __init__(
        self,
        name,
        model,
        encoder,
        data_providers,
        model_file,
        output_file
    ):
        self.name = name
        self.model = model
        self.encoder = encoder
        self.data_providers = data_providers
        self.model_file = model_file
        self.output_file = output_file

    def run(self, mode):
        if mode not in ['train', 'evaluate', 'predict']:
            raise ValueError(f'ERROR: Unknown run mode `{mode}`')
        print(f'Running {self.name}\'s `{mode}` mode...')
        print('Loading input data...')
        data = self._load_data()
        print('Encoding input data...')
        encoded_data = self.encoder.encode(data)
        if mode == 'train':
            self._train(encoded_data)
        elif mode == 'evaluate':
            self._evaluate(encoded_data)
        elif mode == 'predict':
            self._predict(encoded_data)
        else:
            raise ValueError(f'ERROR: Unknown run mode `{mode}`')

    def _train(self, encoded_data):
        print('Training model...')
        self.model.train(encoded_data)
        print(f'Saving model to `{self.output_file}`...')
        self.model.save(self.output_file)

    def _evaluate(self, encoded_data):
        print(f'Loading model from `{self.model_file}`...')
        self.model.load(self.model_file)
        print('Evaluating model...')
        self.model.evaluate(encoded_data)

    def _predict(self, encoded_data):
        print(f'Loading model from `{self.model_file}`...')
        self.model.load(self.model_file)
        print('Predicting interactions...')
        predictions = self.model.predict(encoded_data)
        print(f'Saving predictions to `{self.output_file}`...')
        self._save_predictions(predictions)

    def _save_predictions(self, predictions):
        with open(self.output_file, 'w') as f:
            for prediction in predictions:
                f.write(prediction)

    def _load_data(self):
        data = {}
        for name, provider in self.data_providers.items():
            data[name] = provider.load()
        return data
