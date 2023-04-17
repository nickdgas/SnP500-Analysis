import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import logging

# from os.path import isfile

# def get_historical_data(tickers: list, startDate= None, endDate= None) -> pd.DataFrame:
#     df_historicalData = pd.DataFrame()
#     for tic in tickers:
#         historicalData = pd.DataFrame()
#         yf_ticker = yf.Ticker(tic)
#         if(startDate != None and endDate != None):
#             historicalData = yf_ticker.history(start= startDate, end= endDate, interval= '1d', auto_adjust= True)
#         else:
#             historicalData = yf_ticker.history(period= 'max', interval= '1d', auto_adjust= True)
#         historicalData.insert(0, 'Symbol', tic)
#         df_historicalData = df_historicalData.append(historicalData)
#     df_historicalData.set_index(['Date', 'Symbol'], inplace= True)
#     return df_historicalData

# def get_last_recorded_date(sourcefile: str) -> str and pd.DataFrame:
#     df_previousData = pd.read_csv(sourcefile)
#     df_previousData['Date'] = pd.to_datetime(df_previousData['Date'])
#     previousDate = max(df_previousData['Date'])
#     df_previousData.set_index(['Date', 'Symbol'], inplace= True)
#     return previousDate, df_previousData

# if __name__ == '__main__':
#     SnP500 = pd.read_csv(r'S&P 500\S&P500.csv')
#     tickers = SnP500['Symbol'].tolist()
#     currentDate = dt.datetime.today()
#     nextDate = currentDate - dt.timedelta(days=1)
#     rawData = r'Raw\RawData.csv'
#     if isfile(rawData):
#         previousDate, df_previousData = get_last_recorded_date(rawData)
#         df_newData = get_historical_data(tickers, previousDate, nextDate)
#         df_Final = df_previousData.append(df_newData)
#         df_Final.reset_index(inplace= True)
#         df_Final = df_Final.drop_duplicates(subset=['Date', 'Symbol'], keep='first')
#         df_Final.set_index(["Date", "Symbol"], inplace=True)
#     else:
#         df_newData = get_historical_data(tickers)
#         df_Final = df_newData

#     print(df_Final)

def get_historical_data(tickers: list, startDate: str, endDate: str) -> pd.DataFrame:
    temp = []
    for tic in tickers:
        logging.basicConfig(filename='/IngestLog/IngestData.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger=logging.getLogger(__name__)
        try:
            yf_ticker = yf.Ticker(tic)
            df_historicalData = pd.DataFrame(yf_ticker.history(start= startDate, end= endDate, interval= '1d', auto_adjust= True))
            df_historicalData.insert(0, 'Symbol', tic)
            temp.append(df_historicalData)
            print(f'Successfully retrieved {tic} data')
        except:
            print(f'Error getting data for {tic}')
    df_alldata = pd.concat(temp).reset_index()

    return df_alldata

if __name__ == '__main__':
    SnP500 = pd.read_csv(r'S&P 500\S&P500.csv')
    tickers = SnP500['Symbol'].tolist()
    tickers = [spc.replace(' ', '') for spc in tickers]
    startDate = '2023-01-01'
    endDate = '2023-04-17'
    df_alldata = get_historical_data(tickers, startDate, endDate)

