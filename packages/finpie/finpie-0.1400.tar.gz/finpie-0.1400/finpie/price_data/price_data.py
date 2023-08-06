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



import re
import time
import requests
import pandas as pd
import datetime as dt
from tqdm import tqdm
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
from finpie.base import DataBase


def historical_prices( ticker, start = None, end = None):
    '''

    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    if start == None:
        start = -2208988800

    if end == None:
        last_close = (dt.datetime.today() ).strftime("%Y-%m-%d")
        end = int(time.mktime(time.strptime(f'{last_close} 00:00:00', '%Y-%m-%d %H:%M:%S')))

    url = f'https://query2.finance.yahoo.com/v7/finance/download/{ticker}?period1={start}&period2={end}&interval=1d'
    r = requests.get(url, headers = headers).text
    df = pd.read_csv(StringIO(r))
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    df.index = pd.to_datetime(df.date, format = '%Y-%m-%d')
    df.drop('date', inplace=True, axis=1)

    return df


def yahoo_option_chain( ticker ):
    '''

    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    url = f'https://query2.finance.yahoo.com/v7/finance/options/{ticker}?getAllData=True'
    r = requests.get(url, headers = headers).json()
    calls = []
    puts = []
    for o in r['optionChain']['result'][0]['options']:
        calls.append( pd.DataFrame(o['calls']))
        puts.append( pd.DataFrame(o['puts']))
    calls = pd.concat(calls)
    puts = pd.concat(puts)

    calls.columns = [re.sub( r"([A-Z])", r"_\1", col).lower() for col in calls.columns]
    puts.columns = [re.sub( r"([A-Z])", r"_\1", col).lower() for col in puts.columns]

    calls.expiration = pd.to_datetime([dt.datetime.fromtimestamp(x).date() for x in calls.expiration])
    calls.last_trade_date = pd.to_datetime([dt.datetime.fromtimestamp(x) for x in calls.last_trade_date])

    puts.expiration = pd.to_datetime([dt.datetime.fromtimestamp(x).date() for x in puts.expiration])
    puts.last_trade_date = pd.to_datetime([dt.datetime.fromtimestamp(x) for x in puts.last_trade_date])

    calls.reset_index(drop=True, inplace=True)
    puts.reset_index(drop=True, inplace=True)

    return calls, puts


def cboe_option_chain(ticker, head=False):

    '''db = DataBase()
    db.head = head
    url = 'http://www.cboe.com/delayedquote/quote-table-download'
    try:
        driver = db._load_driver(caps = 'none')
        driver.get(url)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id="txtTicker"]')))
        driver.find_element_by_xpath('//input[@id="txtTicker"]').send_keys(ticker)
        driver.find_element_by_xpath('//input[@id="txtTicker"]').send_keys(Keys.ENTER)
        db._downloads_done('quotedata.dat')
        driver.close()
        driver.quit()
    except:
        print('Failed to load data...')
        driver.close()
        driver.quit()
        return None

    df = pd.read_csv(db.download_path + '/quotedata.dat', error_bad_lines=False, warn_bad_lines=False)
    underlying_price = float( df.columns[-2] )
    df = pd.read_csv(db.download_path + '/quotedata.dat', skiprows = [0,1,3], error_bad_lines=False, warn_bad_lines=False)
    df['underlying'] = underlying_price
    os.remove(db.download_path + '/quotedata.dat')

    df.columns = [ col.replace(' ', '_').lower().replace('_date', '') for col in df.columns ]
    puts = df.loc[:, ['expiration', 'puts' ] + [ col for col in df.columns if '.1' in col ] + [ 'strike', 'underlying' ] ]
    puts.columns = [ col.replace('.1', '') for col in puts.columns ]
    calls = df.loc[:, [ col for col in df.columns if '.1' not in col ] ]
    calls.drop('puts', inplace = True, axis = 1)

    return calls, puts'''

    raise ValueError('This function is depreciated due to a change in the CBOE website. Will try to replace this soon.')



def historical_futures_contracts(date_range):
    '''
        Function to retrieve historical futures prices of all available futures contracts,
        including currency, interest rate, energy, meat, metals, softs, grains, soybeans,
        fiber and index futures.

        Notice that the download is not very fast and 20 years of data takes around 2 hours
        to download and contains around 2 million rows.

        input: pandas date range, e.g. pd.date_range('2000-01-01', '2020-01-01')
        output: pandas dataframe with prices for all available futures for the
                specified time period
    '''

    with ThreadPoolExecutor(4) as pool:
        res = list(tqdm( pool.map(_download_prices, date_range), total=len(date_range)))
    df_out = pd.concat([i for i in res if type(i) != type([0]) ], axis=0)
    #df_out.index.name = 'date'
    return df_out


def futures_contracts(date):
    df = _download_prices(date)
    #df.index.name = 'date'
    return df

def _calc_32(l):
    r = '32'
    while len(r) < l:
        r += '0'
    return r

def _download_prices(date):
    '''
    input: datetime object
    output: pandas dataframe with prices for all available futures for the
            specified date
    '''
    db = DataBase()
    errors = []
    if type(date) == type('str'):
        date = pd.to_datetime(date, format='%Y-%m-%d')
    y = str(date.year)
    if len(str(date.month)) == 2:
        m = str(date.month)
    else:
        m = '0' + str(date.month)
    if len(str(date.day)) == 2:
        d = str(date.day)
    else:
        d = '0' + str(date.day)
    try:
        url = f'https://www.mrci.com/ohlc/{y}/{y[-2:]+m+d}.php'
        soup = db._get_session(url)
        df = pd.read_html( str(soup.find('map').find_next('table')) )[0]
        futures_lookup = pd.read_csv(r'finpie/price_data/futures_lookup.csv').name.tolist()
        indices = [ i for i, j in enumerate(df.iloc[:,0]) if j in futures_lookup ]
        columns = ['month', 'date', 'open', 'high', 'low', 'close', 'change', 'volume', 'open_interest', 'change_in_oi' ]
        if len(df.columns) == 11:
            df = df.iloc[indices[0]:-2, :len(df.columns)-1]
        else:
            df = df.iloc[indices[0]:-2, :]
        #session.close()
    except:
        errors.append(date)
        #session.close()
        return errors
    df.columns = columns

    first = True
    for i in range(1, len(indices)):
        temp = df.loc[indices[i-1]+1:indices[i]-2].copy()
        temp['future'] = df.loc[indices[i-1], 'month']
        if first:
            out = temp.copy()
            first = False
        else:
            out = out.append(temp)
    out = out[out.iloc[:,1] != 'Total Volume and Open Interest']
    # out.to_csv('futures.csv')
    out.index = [date] * len(out) #pd.to_datetime( [ f'{i[-2:]}/{i[2:4]}/{i[:2]}' for i in out.date ] )
    out.replace('\+', '', regex = True, inplace = True)
    out.replace('unch', 0, inplace = True)
    cols = ['open', 'high', 'low', 'close', 'change', 'volume', 'open_interest', 'change_in_oi']
    for col in cols:
        out.loc[out[col].str.contains('~') == True, col] = [int(x.split('~')[0])+int(x.split('~')[-1])/int(_calc_32(len(x.split('~')[-1])))
                                                                     for x in out.loc[out[col].str.contains('~') == True, col].values]
    out = out[~out.change_in_oi.str.contains("Weekly", na=False)]
    out.loc[:, cols] = out.loc[:, cols].values.astype('float')
    return out


if __name__ == '__main__':
    p = 1
    #startdate = '2023-01-01'
    #enddate = '2023-02-08'
    #d_range = pd.date_range(startdate, enddate)
    '''    dfs = []
    for d in d_range:
        df = _download_prices(d)
        dfs = dfs.append(df)
        print(d)'''
    #df = historical_futures_contracts(d_range)
