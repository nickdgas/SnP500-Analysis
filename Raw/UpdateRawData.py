import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging
import xlsxwriter
import sys

def write_out(df: pd.DataFrame, output: str):
    """
    Writes output to excel
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    return

def get_previous(df: pd.DataFrame):
    prev = df['Date'].max()
    next = prev + timedelta(days=1)
    return next.strftime('%Y-%m-%d')

def get_current():
    return datetime.now().strftime('%Y-%m-%d')

def update_historical_data(tickers: list, startDate: str, endDate: str, df_old: pd.DataFrame, df_extraInfo: pd.DataFrame) -> pd.DataFrame:
    """
    Ingest and log historical data for SnP500 
    """
    lastDate = endDate.replace('-', '')
    logPath = r'Logs' + '\\' + lastDate + r'.log'
    temp = []
    logging.basicConfig(filename=logPath, level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
    for tic in tickers:
        try:
            yf_ticker = yf.Ticker(tic)
            df_historical = pd.DataFrame(yf_ticker.history(start= startDate, end= endDate, interval= '1d', auto_adjust= True))
            df_historical.index = df_historical.index.tz_localize(None)
            df_historical.insert(0, 'Symbol', tic)
            temp.append(df_historical)
            logging.info(f'Successfully retrieved {tic} data')
            if len(df_historical) == 0:
                raise Exception('No data found')
        except Exception as e:
            logging.error(f'Error getting data for {tic}: {e}')
            if str(e) == 'No data found':
                logging.error(f'Error: No data received for {tic}: {e}')
    df_new = pd.concat(temp).reset_index()
    df_mergeExtraInfo = pd.merge(df_new, df_extraInfo, on='Symbol')
    df_updated = pd.concat([df_old, df_new]).reset_index(drop=True)
    df_updated = df_updated.sort_values(by='Date')
    return df_updated

def main():
    """
    Read in tickers and call methods to read and write data
    """
    SnP500List = pd.read_html(r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', converters= {'CIK': str})
    filterData = SnP500List[0]
    sortData = filterData.sort_values(by=['Symbol'], ascending=True).astype('string')
    sortData['Symbol'] = sortData['Symbol'].str.replace('.','-', regex=True)
    tickers = sortData['Symbol'].tolist()
    additionalInfo = sortData[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK']]
    oldData = pd.read_excel(r'Raw\RawData.xlsx', converters= {'CIK': str})
    startDate = str(get_previous(oldData))
    endDate = str(get_current())
    df_updatedData = update_historical_data(tickers, startDate, endDate, oldData, additionalInfo)
    write_out(df_updatedData, r'Raw\test.xlsx')

if __name__ == '__main__':
    main()