import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
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

def get_historical_data(tickers: list, startDate: str, endDate: str, df_extraInfo: pd.DataFrame) -> pd.DataFrame:
    """
    Ingest and log historical data for SnP500 
    """
    temp = []
    logging.basicConfig(filename=r'Logs/20230417.log', level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
    for tic in tickers:
        try:
            yf_ticker = yf.Ticker(tic)
            df_historicalData = pd.DataFrame(yf_ticker.history(start= startDate, end= endDate, interval= '1d', auto_adjust= True))
            df_historicalData.index = df_historicalData.index.tz_localize(None)
            df_historicalData.insert(0, 'Symbol', tic)
            temp.append(df_historicalData)
            logging.info(f'Successfully retrieved {tic} data')
            if len(df_historicalData) == 0:
                raise Exception('No data found')
        except Exception as e:
            logging.error(f'Error getting data for {tic}: {e}')
            if str(e) == 'No data found':
                logging.error(f'Error: No data received for {tic}: {e}')
    df_allHistoricalData = pd.concat(temp).reset_index()
    df_mergeExtraInfo = pd.merge(df_allHistoricalData, df_extraInfo, on='Symbol')
    return df_mergeExtraInfo

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
    startDate = '2023-01-01'
    endDate = '2023-04-17'
    df_completeData = get_historical_data(tickers, startDate, endDate, additionalInfo)
    write_out(df_completeData, r'Raw\RawData.xlsx')

if __name__ == '__main__':
    main()
