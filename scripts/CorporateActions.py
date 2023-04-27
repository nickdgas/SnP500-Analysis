import pandas as pd
import numpy as np
import datetime
import xlsxwriter

def write_out(df: pd.DataFrame, output: str):
    """
    Writes output to excel
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    return

def main():
    """
    Calls methods to read and write data
    """    
    # read security data as type string
    df_RawData = pd.read_excel(r'data\raw\RawData.xlsx', converters= {'CIK': str}, usecols=['Date', 'Symbol', 'Dividends', 'Stock Splits'])
    # normalize data; rename other columns; insert ID column
    df_RawData['Is Current'] = np.where((df_RawData['Dividends'] != 0) | (df_RawData['Stock Splits'] != 0), 1, 0)
    current = pd.Timestamp.max.strftime('%Y-%m-%d')
    df_Drop = df_RawData.loc[df_RawData['Is Current'] == 1] 
    df_Filter = df_Drop[['Symbol', 'Dividends', 'Stock Splits', 'Is Current', 'Date']].rename(columns={'Date': 'Start Date'})
    df_Filter['Is Current'] = (df_Filter.groupby('Symbol')['Start Date'].transform('last') == df_Filter['Start Date']).astype(int)
    df_Filter['End Date'] = df_Filter.groupby('Symbol')['Start Date'].transform('last')
    df_Filter.loc[df_Filter['Is Current'] == 1, 'End Date'] = current
    # write to excel
    write_out(df_Filter, r'data\processed\CorporateActions.xlsx')

if __name__ == '__main__':
    main()