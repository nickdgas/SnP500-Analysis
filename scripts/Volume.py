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
    # read raw and security data
    df_RawData = pd.read_excel(r'data\raw\RawData.xlsx', converters= {'CIK': str}, usecols=['Date', 'Symbol', 'Volume'])
    df_Security = pd.read_excel(r'data\processed\Security.xlsx', usecols=['ID', 'Short Name']).rename(columns={'ID': 'SecurityID'})
    df_Date = pd.read_excel(r'data\processed\Date.xlsx').rename(columns={'ID': 'ReportDateID'})
    # normalize data, insert columns; merge using Security ID
    df_SecurityMerge = df_RawData.merge(df_Security, left_on='Symbol', right_on='Short Name')
    df_DateMerge = df_SecurityMerge.merge(df_Date, left_on='Date', right_on='Date')
    df_Filter = df_DateMerge[['ReportDateID', 'SecurityID', 'Volume']]
    # write to excel
    write_out(df_Filter, r'data\processed\Volume.xlsx')

if __name__ == '__main__':
    main()