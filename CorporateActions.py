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
    df_RawData = pd.read_excel(r'Raw\RawData.xlsx', converters= {'CIK': str}, usecols=['Date', 'Symbol', 'Dividends', 'Stock Splits'])
    # normalize data; rename other columns; insert ID column
    df_RawData['Has Actions'] = np.where((df_RawData['Dividends'] != 0) | (df_RawData['Stock Splits'] != 0), 'Yes', 'No')
    df_Drop = df_RawData.loc[df_RawData['Has Actions'] == 'Yes']
    df_Drop.insert(0, 'ID', df_Drop.index+1) 
    print(df_Drop)

    # write to excel


if __name__ == '__main__':
    main()