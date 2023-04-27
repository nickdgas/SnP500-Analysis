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
    # read raw and actions data
    df_RawData = pd.read_excel(r'data\raw\RawData.xlsx', converters= {'CIK': str}, usecols=['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK']).astype('string')
    df_Actions = pd.read_excel(r'data\processed\CorporateActions.xlsx').rename(columns={'Symbol': 'Short Name'})
    # normalize raw data; rename other columns; insert ID column
    df_Drop = df_RawData.drop_duplicates(subset='Symbol', keep='first')\
                        .rename(columns={'Symbol': 'Short Name', 'Security': 'Long Name', 'GICS Sector': 'Industry Sector', 'GICS Sub-Industry': 'Industry Group'})
    df_Drop.insert(0, 'ID', df_Drop.index+1)
    df_Security = df_Drop[['ID', 'Short Name', 'Long Name', 'Industry Sector', 'Industry Group', 'CIK']]
    # filter and merge actions data
    df_Filter = df_Actions.loc[df_Actions['Is Current'] == 1]
    df_Merge = df_Security.merge(df_Filter, on='Short Name', how='left')
    df_Merge['Is Current'] = df_Merge['Is Current'].astype('Int64')
    # write to excel
    write_out(df_Merge, r'data\processed\Security.xlsx')  

if __name__ == '__main__':
    main()
