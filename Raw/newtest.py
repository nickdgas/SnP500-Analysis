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

def get_historical_data(df):
    temp = []
    for ind, column in enumerate(df.columns):
        for value in df['Symbol'].values:
            yf_ticker = yf.Ticker(value)
            df_historicalData = pd.DataFrame(yf_ticker.history(start= startDate, end= endDate, interval= '1d', auto_adjust= True))
            temp.append(df_historicalData)
    df = pd.concat(temp, axis=0)
    return df

SnP500List = pd.read_html(r'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', converters= {'CIK': str})
filterData = SnP500List[0]
sortData = filterData.sort_values(by=['Symbol'], ascending=True).astype('string')
additionalInfo = sortData[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK']]
startDate = '2023-01-01'
endDate = '2023-04-17'
test = get_historical_data(additionalInfo)
print(test)