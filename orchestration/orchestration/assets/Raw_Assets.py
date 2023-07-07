import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging
import xlsxwriter
from urllib import request
import ssl
from dagster import (
    asset,
)
def get_url() -> str:
    """
    Bypase ssl cert verification and retrieve data from html
    """
    url = r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    context = ssl._create_unverified_context()
    response = request.urlopen(url, context=context)
    html = response.read()
    return html

def get_previous(df: pd.DataFrame) -> str:
    prev = df['Date'].max()
    next = prev + timedelta(days=1)
    return str(next.strftime('%Y-%m-%d')
)
def get_current() -> str:
    return str(datetime.now().strftime('%Y-%m-%d'))

@asset(name='Raw_Staging', group_name='Raw_Assets')
def get_historicalData() -> pd.DataFrame:
    """
    Ingest and log historical data for SnP500 
    """
    fundList = pd.read_html(get_url(), converters= {'CIK': str})[0]
    sortList = fundList.sort_values(by=['Symbol'], ascending=True).astype('string')
    sortList['Symbol'] = sortList['Symbol'].str.replace('.','-', regex=True)
    dfSec = sortList[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK']]
    dfOld = pd.read_excel(r'C:\Users\nick.dagostino\Documents\repos\SnP500-Analysis\data\raw\RawData.xlsx', converters= {'CIK': str})
    startDate = get_previous(dfOld)
    endDate = get_current()
    logPath = r'C:\Users\nick.dagostino\Documents\repos\SnP500-Analysis\docs\logs' + '\\' + endDate.replace('-', '') + r'.log'
    temp = []
    logging.basicConfig(filename=logPath, level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
    for symbol, security, sector, sub_industry, cik in zip(dfSec['Symbol'].values, dfSec['Security'].values, dfSec['GICS Sector'].values, dfSec['GICS Sub-Industry'].values, dfSec['CIK'].values):
        try:
            yf_ticker = yf.Ticker(symbol)
            df_historicalData = pd.DataFrame(yf_ticker.history(start= startDate, end= endDate, interval= '1d', auto_adjust= True))
            df_historicalData.index = df_historicalData.index.tz_localize(None)
            df_historicalData['Symbol'] = str(symbol)
            df_historicalData['Security'] = str(security)
            df_historicalData['GICS Sector'] = str(sector)
            df_historicalData['GICS Sub-Industry'] = str(sub_industry)
            df_historicalData['CIK'] = str(cik)
            temp.append(df_historicalData[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK'] + df_historicalData.columns[:-5].tolist()])
            logging.info(f'Successfully retrieved {symbol} data')
            if len(df_historicalData) == 0:
                raise Exception('No data found')
        except Exception as e:
            logging.error(f'Error getting data for {symbol}: {e}')
            if str(e) == 'No data found':
                logging.error(f'Error: No data received for {symbol}: {e}')
    dfNew = pd.concat(temp).reset_index()
    return dfNew

@asset(name='Raw_Data', group_name='Raw_Assets')
def update_Raw(Raw_Staging: pd.DataFrame) -> pd.DataFrame:
    """
    Update/insert historical data for SnP500 
    """
    dfOld = pd.read_excel(r'C:\Users\nick.dagostino\Documents\repos\SnP500-Analysis\data\raw\RawData.xlsx', converters= {'CIK': str})
    dfUpdate = pd.concat([dfOld, Raw_Staging]).reset_index(drop=True)
    dfUpdate = dfUpdate.sort_values(by='Date')
    writer = pd.ExcelWriter(r'C:\Users\nick.dagostino\Documents\repos\SnP500-Analysis\data\raw\RawData.xlsx', engine='xlsxwriter')
    dfUpdate.to_excel(writer, index=False)
    writer.close()
    return dfUpdate
