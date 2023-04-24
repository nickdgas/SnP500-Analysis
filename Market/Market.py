import pandas as pd
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
    df_RawData = pd.read_excel(r'Raw\RawData.xlsx', converters= {'CIK': str})  
    df_Security = pd.read_excel(r'Security\Security.xlsx', usecols=['ID', 'Short Name']).rename(columns={'ID': 'SecurityID'})
    df_Date = pd.read_excel(r'Date\Date.xlsx').rename(columns={'ID': 'ReportDateID'})
    df_SecurityMerge = df_RawData.merge(df_Security, left_on='Symbol', right_on='Short Name')
    df_DateMerge = df_SecurityMerge.merge(df_Date, left_on='Date', right_on='Date')
    df_Market = df_DateMerge[['SecurityID', 'ReportDateID', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']]
    df_Market.insert(0, 'ID', df_Market.index+1)
    write_out(df_Market, r'Market\Market.xlsx')

if __name__ == '__main__':
    main()