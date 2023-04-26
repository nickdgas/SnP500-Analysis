import pandas as pd
import numpy as np
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
    current = df_RawData['Date'].max()
    df_Drop = df_RawData.loc[df_RawData['Is Current'] == 1] 
    df_Filter = df_Drop[['Symbol', 'Is Current', 'Date']].sort_values(by='Symbol')
    df_Pivot = pd.pivot_table(df_Filter, values='Date', index='Symbol', aggfunc=['min','max'])
    df_Pivot.columns = [f'{col[1]}{col[0]}' for col in df_Pivot.columns]
    df_Pivot = df_Pivot.reset_index()
    # write to excel
    #write_out(df_filterDupes, r'data\processed\CorporateActions.xlsx')
    print(df_Pivot)

if __name__ == '__main__':
    main()