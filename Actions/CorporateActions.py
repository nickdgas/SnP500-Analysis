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
    #df_Actions = df_RawData[['Source Key', 'Dividends', 'Stock Splits']]
    #df_Actions.insert(0, 'ID', df_Actions.index+1)
    print(df_RawData)
    #write_out(df_Actions, r'Actions\CorporateActions.xlsx')

if __name__ == '__main__':
    main()