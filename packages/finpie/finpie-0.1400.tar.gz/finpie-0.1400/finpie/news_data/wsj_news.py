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

import re
import time
import random
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from finpie.news_data.news import CleanNews
import dateparser

class WSJNews(CleanNews):
    def __init__(self, ticker, keywords, head=False, verbose=False):
        CleanNews.__init__(self)
        self.ticker = ticker
        self.keywords = keywords
        self.verbose = verbose
        self.head = head

    def wsj(self, datestop=False):
        '''

        '''
        source = 'wsj'
        # change to date today
        td_1 = dt.datetime.today() - dt.timedelta(days=320)
        y, m, d = self._format_date(td_1)
        start_date = y + '%2F' + m + '%2F' + d
        td_2 = dt.datetime.today()
        y, m, d = self._format_date(td_2)
        end_date = y + '%2F' + m + '%2F' + d
        url = 'https://www.wsj.com/search?&query=' + self.keywords.replace(' ', '%20') + '&sort=date-desc&duration=4y&startDate=' + start_date + '&endDate=' + end_date + '&source=wsjie%2Cblog%2Cwsjvideo%2Cinteractivemedia%2Cwsjsitesrch%2Cwsjpro%2Cautowire%2Capfeed'
        driver = self._load_driver()
        try:
            # Set and retrieve url
            driver.get(url)
            time.sleep(5)
            try:
                element = driver.find_element(By.XPATH, '//iframe[@title="SP Consent Message"]')
                driver.switch_to.frame(element)
                xPath = '//button[@title="YES, I AGREE"]'
                driver.find_element(By.XPATH, xPath).click()
                driver.switch_to.default_content()
            except:
                pass
            driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Next Page")]')))
            bool2 = True
            contents = []
            max = int(driver.find_element(By.XPATH, '//span[@class="WSJTheme--total-pages--3FkCtMxZ "]').text.replace('of ',''))
            contents.append(driver.page_source)
            for i in range(max - 1):
                try:
                    time.sleep(random.randint(0, 2))
                    driver.get(url + f'&page={i + 2}')
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Next Page")]')))
                    contents.append(driver.page_source)
                except:
                    try:
                        driver.get(url + f'&page={i + 2}')
                        element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Next Page")]')))
                        contents.append(driver.page_source)
                    except:
                        driver.get(url + f'&page={i + 2}')
                        time.sleep(5)
                        contents.append(driver.page_source)
                if datestop:
                    try:
                        d = driver.find_elements(By.XPATH, '//p[contains(@class, "WSJTheme--timestamp")]')[-1].text
                        d = pd.to_datetime(' '.join(d.split(' ')[:3]))
                        if d < pd.to_datetime(datestop):
                            bool2 = False
                            break
                    except:
                        d = driver.find_elements(By.XPATH, '//p[contains(@class, "WSJTheme--timestamp")]')[-1].text
                        pass
            if bool2:
                bool = True
            else:
                bool = False
            contents.append(driver.page_source)
    
            while bool:
                try:
                    td_2 = td_1
                    y, m, d = self._format_date(td_2)
                    start_date = y + '/' + m + '/' + d
                    td_1 = td_1 - dt.timedelta(days=320)
                    y, m, d = self._format_date(td_1)
                    end_date = y + '/' + m + '/' + d
                    url = 'https://www.wsj.com/search?&query=' + self.keywords.replace(' ', '%20') + '&sort=date-desc&duration=4y&startDate=' + start_date + '&endDate=' + end_date + '&source=wsjie%2Cblog%2Cwsjvideo%2Cinteractivemedia%2Cwsjsitesrch%2Cwsjpro%2Cautowire%2Capfeed'
                    driver.get(url)
                    element = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Next Page")]')))
                    max = int(driver.find_element(By.XPATH, '//span[@class="WSJTheme--total-pages--3FkCtMxZ "]').text.replace('of ', ''))
                    contents.append(driver.page_source)
                    for i in range(max - 1):
                        try:
                            time.sleep(random.randint(0, 2))
                            driver.get(url + f'&page={i + 2}')
                            element = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Next Page")]')))
                            contents.append(driver.page_source)
                        except:
                            try:
                                driver.get(url + f'&page={i + 2}')
                                element = WebDriverWait(driver, 15).until(
                                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Next Page")]')))
                                contents.append(driver.page_source)
                            except:
                                driver.get(url + f'&page={i + 2}')
                                contents.append(driver.page_source)
                        if datestop:
                            d = driver.find_elements(By.XPATH, '//p[contains(@class, "WSJTheme--timestamp")]')[-1].text
                            d = pd.to_datetime(' '.join(d.split(' ')[:3]))
                            if d > pd.to_datetime(datestop):
                                bool = False
                except:
                    bool = False
    
            driver.close()
            driver.quit()
        except:
            print('Failed to load data...\n')
            driver.quit()
            return None
        headline, link, date, description, author, tag = [], [], [], [], [], []
        for content in contents:
            soup = bs(content, "lxml")
            # articles  = soup.find_all('div', class_ = 'headline-item' )
            articles = soup.find_all('article')
            for article in articles:
                try:
                    date.append(article.find('p', class_=re.compile('^WSJTheme--timestamp')).text)
                except:
                    continue
                headline.append(article.find('h3').text.strip())
                link.append(article.find('h3').find('a').get('href'))
                try:
                    tag.append(article.find('li', class_=re.compile('^WSJTheme--type')).text)
                except:
                    tag.append('nan')
                # date.append( article.find('time').text )
                try:
                    # author.append( article.find('li', class_ = 'byline').text.replace('By', '').strip() )
                    author.append(article.find('p', class_=re.compile('^WSJTheme--byline')).text.strip())
                except:
                    author.append('nan')
                try:
                    description.append(article.find('p', class_=re.compile('^WSJTheme--summary')).text.strip())
                except:
                    description.append('nan')
        data = pd.DataFrame(
            {
                'link': link,
                'headline': headline,
                'date': date,
                'description': description,
                'author': author,
                'tag': tag
            }
        )
        data['date_retrieved'] = dt.datetime.today()
        data['ticker'] = self.ticker
        data['newspaper'] = 'WSJ'
        data['search_term'] = self.keywords
        data['id'] = data['newspaper'] + data['headline'] + data['link']
        columns = ['link', 'headline', 'date', 'description', 'date_retrieved', 'author', 'tag', 'newspaper', 'comments',
                   'ticker', 'search_term', 'id']
        for col in columns:
            if col not in data.columns:
                data[col] = 'nan'
        data['source'] = source
        data.date = pd.to_datetime([dateparser.parse(d) for d in data.date], utc=True)
        data.date = data.date.apply(lambda x: dt.datetime(x.year, x.month, x.day))
        data.index = data.date
        data.index.name = 'date'
        data.drop('date', axis=1, inplace=True)

        if self.verbose:
            print('-' * 78)
            print(source.upper(), 'done.', len(data), 'articles collected.')
            print('-' * 78)
    
        return data

if __name__ == '__main__':
    p = 1
    # quick test
    #wsj = WSJNews('AAPL', 'AAPL')
    #data = wsj.wsj(datestop='2022-12-01')
    #print(data)