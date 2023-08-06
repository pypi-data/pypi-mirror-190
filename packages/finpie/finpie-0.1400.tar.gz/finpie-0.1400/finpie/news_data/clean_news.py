#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# finpie - a simple library to download some financial data
# https://github.com/peterlacour/finpie
#
# Copyright (c) 2020 Peter la Cour
#
# Licensed under the MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import pandas as pd
from finpie.base import DataBase

class CleanNews(DataBase):

    def __init__(self):
        DataBase.__init__(self)
        self.months = { 'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', \
                       'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
        self.weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.dayz = ['Today', 'Yesterday']
        self.filterz = [' ']

    def _format_date(self, date):
        '''

        '''
        date = pd.to_datetime(date)
        y = str(date.year)
        if len(str(date.month)) < 2:
            m = '0' + str(date.month)
        else:
            m = str(date.month)
        if len(str(date.day)) < 2:
            d = '0' + str(date.day)
        else:
            d = str(date.day)
        return y, m, d

    def _clean_duplicates(self, data):
        '''

        '''
        columns = [ col for col in data.columns if col != 'date_retrieved' ]
        data.drop_duplicates(columns, inplace = True)
        data.reset_index(drop = True, inplace = True)
        return data

    def filter_data(self, data, filter='both'):
        '''
        filter options = 'headline', 'description', 'both'

        '''

        filtered = []
        for i, n in enumerate(data.headline):
            for f in self.filterz:
                if f in n.lower() and filter in ['headline', 'both']:
                    filtered.append( data.id.iloc[i] )
                elif f in data.description.iloc[i].lower() and filter in ['description', 'both']:
                    filtered.append(data.id.iloc[i])
                else:
                    continue

        data = data[ data.id.isin(filtered) ]
        #data.reset_index(drop = True, inplace = True)
        return data
