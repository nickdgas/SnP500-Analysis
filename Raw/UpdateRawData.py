import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging
import xlsxwriter

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

def update_historical_data(df_addInfo: pd.DataFrame, df_old: pd.DataFrame, startDate: str, endDate: str) -> pd.DataFrame:
    """
    Ingest and log historical data for SnP500 
    """
    logPath = r'Logs' + '\\' + endDate.replace('-', '') + r'.log'
    temp = []
    logging.basicConfig(filename=logPath, level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
    for symbol, security, sector, sub_industry, cik in zip(df_addInfo['Symbol'].values, df_addInfo['Security'].values, df_addInfo['GICS Sector'].values, df_addInfo['GICS Sub-Industry'].values, df_addInfo['CIK'].values):
        try:
            yf_ticker = yf.Ticker(symbol)
            df_historicalData = pd.DataFrame(yf_ticker.history(start= startDate, end= endDate, interval= '1d', auto_adjust= True))
            df_historicalData.index = df_historicalData.index.tz_localize(None)
            df_historicalData['Symbol'] = symbol
            df_historicalData['Security'] = security
            df_historicalData['GICS Sector'] = sector
            df_historicalData['GICS Sub-Industry'] = sub_industry
            df_historicalData['CIK'] = cik
            temp.append(df_historicalData[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK'] + df_historicalData.columns[:-5].tolist()])
            logging.info(f'Successfully retrieved {symbol} data')
            if len(df_historicalData) == 0:
                raise Exception('No data found')
        except Exception as e:
            logging.error(f'Error getting data for {symbol}: {e}')
            if str(e) == 'No data found':
                logging.error(f'Error: No data received for {symbol}: {e}')
    df_new = pd.concat(temp).reset_index()
    df_updated = pd.concat([df_old, df_new]).reset_index(drop=True)
    df_updated = df_updated.sort_values(by='Date')
    return df_updated

def main():
    """
    Read in tickers and call methods to read and write data
    """
    SnP500List = pd.read_html(r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', converters= {'CIK': str})[0]
    sortData = SnP500List.sort_values(by=['Symbol'], ascending=True).astype('string')
    sortData['Symbol'] = sortData['Symbol'].str.replace('.','-', regex=True)
    additionalInfo = sortData[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK']]
    oldData = pd.read_excel(r'Raw\RawData.xlsx', converters= {'CIK': str})
    startDate = str(get_previous(oldData))
    endDate = str(get_current())
    df_updatedData = update_historical_data(additionalInfo, oldData, startDate, endDate)
    write_out(df_updatedData, r'Raw\RawData.xlsx')

if __name__ == '__main__':
    main()