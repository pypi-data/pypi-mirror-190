#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# finpie - a simple library to download some financial data
# https://github.com/peterlacour/finpie
#
# Copyright (c) 2023 Peter la Cour
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

from finpie.news_data.clean_news import CleanNews
from finpie.news_data.ft_news import FTNews
from finpie.news_data.wsj_news import WSJNews
from finpie.news_data.cnbc_news import CNBCNews

class NewsData(CleanNews):
    def __init__(self, ticker, keywords, head=False, verbose=False):
        CleanNews.__init__(self)
        self.ticker = ticker
        self.keywords = keywords
        self.verbose = verbose
        self.head = head

    def ft(self, datestop=False):

        newsClass = FTNews(self.ticker, self.keywords, self.head, verbose=self.verbose)
        data = newsClass.ft(datestop)

        return data

    '''    def wsj( self, datestop=False):

        newsClass = WSJNews(self.ticker, self.keywords, self.head, verbose=self.verbose)
        data = newsClass.wsj(datestop)
        return data
    '''
    def cnbc(self, datestop=False):

        newsClass = CNBCNews(self.ticker, self.keywords, self.head, verbose=self.verbose)
        data = newsClass.cnbc(datestop)
        return data

if __name__ == '__main__':
    p = 1
    news = NewsData('XOM', 'exxon oil')
    data = news.wsj(datestop='2022-12-01')
    print(data)