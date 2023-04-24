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
    df_RawData = pd.read_excel(r'Raw\RawData.xlsx', converters= {'CIK': str}, usecols=['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry', 'CIK']).astype('string')
    df_Security = df_RawData.drop_duplicates(subset='Symbol', keep='first').rename(columns={'Symbol': 'Short Name', 'Security': 'Long Name', 'GICS Sector': 'Industry Sector', 'GICS Sub-Industry': 'Industry Group'})
    df_Security['ID'] = df_Security.index+1
    df_Ordered = df_Security[['ID', 'Short Name', 'Long Name', 'Industry Sector', 'Industry Group', 'CIK']]
    write_out(df_Ordered, r'Security\Security.xlsx')   

if __name__ == '__main__':
    main()
