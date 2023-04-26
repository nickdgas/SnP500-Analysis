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
    df_RawData['Has Actions'] = np.where((df_RawData['Dividends'] != 0) | (df_RawData['Stock Splits'] != 0), 'Yes', 'No')
    df_RawData.insert(0, 'ID', df_RawData.index+1) 
    group_Data = df_RawData.groupby('Symbol')
    df_groupDupes = group_Data.filter(lambda x: x['Symbol'].duplicated().any())
    df_filterDupes = df_groupDupes[['Date','Symbol']]
    df_PivotDupes = pd.pivot_table(df_filterDupes, values='Date', index='Symbol', aggfunc=['min', 'max'])
    df_PivotDupes.columns = [f'{col[1]}{col[0]}' for col in df_PivotDupes.columns]
    df_PivotDupes = df_PivotDupes.reset_index()
    df_MergeDupes = df_RawData.merge(df_PivotDupes, left_on='Symbol', right_on='Symbol')
    df_MergeDupes.loc[df_MergeDupes['Has Actions'] == 'No', ['Datemin', 'Datemax']] = None
    df_filterCols = df_MergeDupes[['ID', 'Symbol', 'Dividends', 'Stock Splits', 'Has Actions', 'Datemin', 'Datemax']].rename(columns={'Has Actions':'Is Active', 'Datemin': 'Start Date', 'Datemax': 'End Date'})
    #df_Actions = df_filterCols.loc[df_filterCols['Is Active'] == 'Yes']
    # write to excel
    write_out(df_filterCols, r'data\processed\CorporateActions.xlsx')

if __name__ == '__main__':
    main()