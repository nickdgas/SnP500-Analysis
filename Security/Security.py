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
    df_RawData = pd.read_excel(r'Raw\RawData.xlsx', converters= {'CIK': str}, usecols=['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK'])
    df_Rename = df_RawData.rename(columns={'Symbol': 'Short Name', 'Security': 'Long Name', 'GICS Sector': 'Industry Sector', 'GICS Sub-Industry': 'Industry Group'})
    df_Rename['ID'] = df_Rename.index +1
    df_Ordered = df_Rename[['ID', 'Short Name', 'Long Name', 'Industry Sector', 'Industry Group', 'CIK']]
    write_out(df_Ordered, r'Security\Security.xlsx')

if __name__ == '__main__':
    main()
