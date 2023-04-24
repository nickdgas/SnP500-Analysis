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
    df_Act = df_RawData[['Dividends', 'Stock Splits']]
    df_Act['ID'] = df_Act.index+1
    df_Ordered = df_Act[['ID', 'Dividends', 'Stock Splits']]
    write_out(df_Ordered, r'Actions\CorporateActions.xlsx')

if __name__ == '__main__':
    main()