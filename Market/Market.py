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
    #df_Type = pd.read_excel(r'Type\Type.xlsx').rename(columns={'ID': 'TypeID'})
    df_SecurityMerge = df_RawData.merge(df_Security, left_on='Symbol', right_on='Short Name')
    df_DateMerge = df_SecurityMerge.merge(df_Date, left_on='Date', right_on='Date')
    #df_TypeMerge = df_DateMerge.merge(df_Type)
    df_Market = df_DateMerge[['SecurityID', 'ReportDateID', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']]
    df_Market.insert(0, 'ID', df_Market.index+1)
    #write_out(df_Market, r'Market\Market.xlsx')
    #print(df_Type)

if __name__ == '__main__':
    main()