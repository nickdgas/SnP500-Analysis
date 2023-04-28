import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import logging
import xlsxwriter
from urllib import request
import ssl

def write_out(df: pd.DataFrame, output: str):
    """
    Writes output to excel
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    return

def get_url(link: str):
    """
    Bypase ssl cert verification and retrieve data from html
    """
    url = link
    context = ssl._create_unverified_context()
    response = request.urlopen(url, context=context)
    html = response.read()
    return html

def get_historical_data(df_addInfo: pd.DataFrame, startDate: str, endDate: str) -> pd.DataFrame:
    """
    Ingest and log historical data for SnP500 
    """
    temp = []
    logging.basicConfig(filename=r'docs\logs\20230417.log', level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
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
    new_df = pd.concat(temp).reset_index()
    return new_df

def main():
    """
    Read in tickers and call methods to read and write data
    """
    html = get_url(r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    SnP500List = pd.read_html(html, converters= {'CIK': str})[0]
    sortData = SnP500List.sort_values(by=['Symbol'], ascending=True).astype('string')
    sortData['Symbol'] = sortData['Symbol'].str.replace('.','-', regex=True)
    additionalInfo = sortData[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK']]
    startDate = '2023-01-01'
    endDate = '2023-04-17'
    test = get_historical_data(additionalInfo, startDate, endDate)
    write_out(test, r'data\raw\RawData.xlsx')

if __name__ == '__main__':
    main()