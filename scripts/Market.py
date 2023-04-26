import pandas as pd
import xlsxwriter
from functools import reduce

# from os import makedirs
# from os.path import join
# def write_out(df: pd.DataFrame, col: str, output_dir: str):
#     """
#     Writes output to Excel files, one file per month in the col column
#     """
#     makedirs(output_dir, exist_ok=True)
#     months = df[col].drop_duplicates().apply(lambda x: str(x)[:6])
#     for month in months:
#         subset = df[df[col].apply(lambda x: str(x)[:6] == month)]
#         output_file = join(output_dir, f'Market_{month}.xlsx')
#         writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
#         subset.to_excel(writer, index=False)
#         writer.close()
#     return

def write_out(df: pd.DataFrame, output: str):
    """
    Writes output to excel
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    return

def merge_dfs(df1: pd.DataFrame, df2: pd.DataFrame, left: str, right: str) -> pd.DataFrame:
    '''
    Merge dataframes on column
    '''
    merged = df1.merge(df2, left_on=left, right_on=right)
    return merged

def main():
    """
    Calls methods to read and write data
    """
    # read data to be refrenced using FKs; use/rename only needed columns
    df_RawData = pd.read_excel(r'data\raw\RawData.xlsx', converters= {'CIK': str})  
    df_Security = pd.read_excel(r'data\processed\Security.xlsx', usecols=['ID', 'Short Name']).rename(columns={'ID': 'SecurityID'})
    df_Date = pd.read_excel(r'data\processed\Date.xlsx').rename(columns={'ID': 'ReportDateID'})
    df_Type = pd.read_excel(r'data\processed\Type.xlsx').rename(columns={'ID': 'TypeID'})
    # group merge on 'Symbol' column; single merge on 'Date' column
    df_SecurityMerge = merge_dfs(df_RawData, df_Security, 'Symbol', 'Short Name')
    df_DateMerge = merge_dfs(df_SecurityMerge, df_Date, 'Date', 'Date')
    # unpivot price types for single merge 
    df_Long = df_DateMerge.melt(id_vars=['SecurityID', 'ReportDateID','Volume', 'Dividends', 'Stock Splits'],value_vars=['Open', 'High', 'Low', 'Close'], var_name='Type', value_name='Price')
    df_TypeMerge = merge_dfs(df_Long, df_Type, 'Type', 'Type')
    # filter columns; insert ID column
    df_Market = df_TypeMerge[['ReportDateID', 'SecurityID', 'TypeID', 'Price', 'Volume', 'Dividends', 'Stock Splits']]
    df_Market.insert(0, 'ID', df_Market.index+1)
    # write to excel
    write_out(df_Market, r'data\processed\Market.xlsx')

if __name__ == '__main__':
    main()