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
    # read raw data; convert CIK to maintain format
    df_RawData = pd.read_excel(r'data\raw\RawData.xlsx', converters= {'CIK': str})
    # unpivot df from wide to long using price type; drop dupes; insert ID column
    df_Pivot = df_RawData.melt(id_vars='Symbol',value_vars=['Open', 'High', 'Low', 'Close'], var_name='Type')
    df_Drop = df_Pivot.drop_duplicates(subset='Type', keep='first')
    df_Type = df_Drop[['Type']].reset_index(drop=True)
    df_Type.insert(0, 'ID', df_Type.index+1)
    # write to excel
    write_out(df_Type, r'data\processed\Type.xlsx')
    
if __name__ == '__main__':
    main()
