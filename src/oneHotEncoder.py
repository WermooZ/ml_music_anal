#!/usr/bin/env python
# coding: utf-8

import pandas as pd

class OneHotEncoder():
    def to_list(self, textdata):
        return ''.join(textdata.lower().split()).split(',')

    def generate_dummies(self, df, column):
        series = df[column]
        return  pd.get_dummies(series.apply(self.to_list).apply(pd.Series).stack()).sum(level=0)