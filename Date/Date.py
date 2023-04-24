import pandas as pd
import numpy as np
from datetime import datetime
import xlsxwriter

def write_out(df: pd.DataFrame, output: str):
    """
    Writes output to excel
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    return

def get_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieve and format date information
    """
    df_Date = pd.DataFrame()
    df_Date['Date'] = df['Date'].drop_duplicates(keep='first')
    df_Date['ID'] = df_Date['Date'].astype('string').str.replace('-','', regex=True).astype('int64')
    return df_Date[['ID', 'Date']]

def main():
    """
    Calls methods to read and write data
    """
    df_RawData = pd.read_excel(r'Raw\RawData.xlsx')
    df_Date = get_date(df_RawData)
    write_out(df_Date, r'Date\Date.xlsx')

if __name__ == '__main__':
    main()