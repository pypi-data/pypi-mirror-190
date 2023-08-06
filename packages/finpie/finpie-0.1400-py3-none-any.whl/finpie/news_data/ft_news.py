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

import time
import numpy as np
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from finpie.news_data.news import CleanNews

class FTNews(CleanNews):
    def __init__(self, ticker, keywords, head=False, verbose=False):
        CleanNews.__init__(self)
        self.ticker = ticker
        self.keywords = keywords
        self.verbose = verbose
        self.head = head

    def ft(self, datestop=False):
        '''
        
        '''
        source = 'ft'
        y = str(dt.datetime.today().year)
        if len(str(dt.datetime.today().month)) < 2:
            m = '0' + str(dt.datetime.today().month)
        else:
            m = str(dt.datetime.today().month)
        if len(str(dt.datetime.today().day)) < 2:
            d = '0' + str(dt.datetime.today().day)
        else:
            d = str(dt.datetime.today().day)
        url = 'https://www.ft.com/search?q=' + self.keywords.replace(' ', '%20') + '&dateTo=' + y + '-' + m + '-' + d + '&sort=date&expandRefinements=true'
        driver = self._load_driver()    
        try:
            # Set and retrive url
            driver.get(url)
            time.sleep(10) # make implicit wait
            co = 0
            # _delete_elements(driver)
            # driver.find_elements(By.XPATH, '//a[@data-trackable="sort-item"]')[1].click()
            # Cant get more than 1000 results and need to change date filter when it gives an error
            contents = []
            contents.append(bs(driver.page_source, "lxml").find_all('div', class_='o-teaser__content'))
            co += 1
            max_articles = np.ceil(int(driver.find_element(By.XPATH, '//h2[@class="o-teaser-collection__heading o-teaser-collection__heading--half-width"]').text.split('of ')[-1].strip()) / 25)
            while co < int(max_articles):
                try:
                    max = int(driver.find_element(By.XPATH, '//span[@class="search-pagination__page"]').text.replace('Page 1 of ', '') )
                    for i in range(max):
                        driver.find_element(By.XPATH, '//a[@class="search-pagination__next-page o-buttons o-buttons--secondary o-buttons-icon o-buttons-icon--arrow-right o-buttons--big o-buttons-icon--icon-only"]').click()
                        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//head')))
                        self._delete_elements(driver)
                        contents.append(bs(driver.page_source, "lxml").find_all('div', class_='o-teaser__content'))
                        co += 1
                        dte = driver.find_elements(By.XPATH, '//div[@class="o-teaser__timestamp"]')[-1].text
                        if datestop:
                            if pd.to_datetime(dte) < pd.to_datetime(datestop):
                                co = int(max_articles) + 10
                                break
                except:
                    try:
                        m = driver.find_elements(By.XPATH, '//time[@class="o-teaser__timestamp-date"]')[-1].text.lower()[:3]
                        d = driver.find_elements(By.XPATH, '//time[@class="o-teaser__timestamp-date"]')[-1].text.split(' ')[1].replace(',', '')
                        y = driver.find_elements(By.XPATH, '//time[@class="o-teaser__timestamp-date"]')[-1].text.split(',')[-1].strip()
                        if len(str(m)) < 2:
                            m = '0' + str(m)
                        else:
                            m = str(m)
                        if len(str(d)) < 2:
                            d = '0' + str(d)
                        else:
                            d = str(d)
    
                        dte = pd.to_datetime(d + ' ' + m.capitalize() + ' ' + y) + dt.timedelta(1)
                        if datestop:
                            if dte < pd.to_datetime(datestop):
                                co = int(max_articles) + 10
                        y, m, d = self._format_date(dte)
                        url = 'https://www.ft.com/search?q=' + self.keywords.replace(' ', '%20') + '&dateTo=' + y + '-' + m + '-' + d + '&sort=date&expandRefinements=true'
                        driver.get(url)
                        # driver.find_elements(By.XPATH, '//a[@data-trackable="sort-item"]')[1].click()
                        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//head')))
                        self._delete_elements(driver)
                        contents.append(bs(driver.page_source, "lxml" ).find_all('div', class_ = 'o-teaser__content' ) )
                        co += 1
                    except:
                        break
            driver.close()
            driver.quit()
        except:
            print('Failed to load data...\n')
            driver.quit()
            return None
    
        headline, link, date, description, author, tag = [], [], [], [], [], []
        headline, link, date, description, author, tag = self._get_articles(contents, headline, link, date, description, author, tag)
    
        contents = None
    
        data = pd.DataFrame(
            {
                'link': link,
                'headline': headline,
                'date': date,
                'description': description,
                'tag': tag
            }
        )
        data['date_retrieved'] = dt.datetime.today()
        data['ticker'] = self.ticker
        data['comments'] = 'nan'
        data['author'] = 'nan'
        data['newspaper'] = 'FT'
        data['search_term'] = self.keywords
        data['id'] = data['newspaper'] +  data['headline'] + data['link']
        columns = ['link', 'headline', 'date', 'description', 'date_retrieved', 'author', 'tag', 'newspaper', 'comments', 'ticker', 'search_term', 'id' ]
        for col in columns:
            if col not in data.columns:
                data[col] = 'nan'
        headline, link, date, description, author, tag = [], [], [], [], [], []
        data['source'] = source
        data.drop_duplicates(inplace=True)
        data.index = pd.to_datetime(data.date)
        data.index.name = 'date'
        data.drop('date', axis=1, inplace=True)
        if self.verbose:
            print('-' * 78)
            print(source.upper(), 'done.', len(data), 'articles collected.')
            print('-' * 78)
        return data
        
    def _delete_elements(self, driver):
        element = driver.find_element(By.TAG_NAME, 'head')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

        element = driver.find_element(By.XPATH, '//div[@class="n-layout__row n-layout__row--header"]')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

        elements = driver.find_elements(By.CLASS_NAME, 'o-teaser__image-placeholder')
        for element in elements:
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

        element = driver.find_element(By.TAG_NAME, 'nav')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

        element = driver.find_element(By.ID, 'o-header-drawer')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

        element = driver.find_element(By.TAG_NAME, 'footer')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

    def _get_articles(self, contents, headline, link, date, description, author, tag):
        for articles in contents:
            # soup  = bs( content, "lxml" )
            # articles  = soup.find_all('div', class_ = 'o-teaser__content' )
            for article in articles:
                tag.append(article.find('a').text)
                headline.append(
                    article.find('div', class_='o-teaser__heading').text.replace('\t', ' ').replace('\n', ' ').strip())
                link.append(article.find('div', class_='o-teaser__heading').find('a').get('href'))
                try:
                    description.append(
                        article.find('p', class_='o-teaser__standfirst').text.replace('\t', ' ').replace('\n', ' ').strip())
                except:
                    description.append('nan')
                try:
                    date.append(article.find('div', class_='o-teaser__timestamp').text)
                except:
                    date.append('nan')
        return headline, link, date, description, author, tag


if __name__ == '__main__':
    p = 1
    # quick test
    #ft = FTNews('XOM', 'exxon oil')
    #print(ft.ft(datestop='2022-12-01'))