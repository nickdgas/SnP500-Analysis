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
    df_RawData = pd.read_excel(r'Raw\RawData.xlsx')
    df_Drop = df_RawData[['Symbol','Dividends', 'Stock Splits']]
    df_Drop.insert(0, 'ID', df_Drop.index+1)
    df_Act = df_Drop[['ID', 'Symbol', 'Dividends', 'Stock Splits']]
    write_out(df_Act, r'Actions\CorporateActions.xlsx')

if __name__ == '__main__':
    main()