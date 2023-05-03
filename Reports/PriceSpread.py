import pandas as pd
import numpy as np
import xlsxwriter

def read(input: str, columns: list) -> pd.DataFrame:
    """
    Reads input to dataframe
    """
    df = pd.read_excel(input, usecols=columns)
    return df

def write(df: pd.DataFrame, output: str) -> None:
    """
    Writes output to excel
    """
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.close()
    return

def main():
    """
    Perform calculations
    """
    df_Market = read(r'data\processed\Market.xlsx', ['ReportDateID', 'SecurityID', 'TypeID', 'Price']).groupby(by=['ReportDateID', 'SecurityID'], group_keys=True)[['TypeID', 'Price']].apply(lambda x: x).droplevel(2)
    open = df_Market.loc[df_Market['TypeID']==1]
    close = df_Market.loc[df_Market['TypeID']==4]
    high = df_Market.loc[df_Market['TypeID']==2]
    low = df_Market.loc[df_Market['TypeID']== 3]
    spread = pd.DataFrame({'Open\Close': open['Price'] - close['Price'], 'High\Low': high['Price'] - low['Price']})
    print(spread)

if __name__ == '__main__':
    main()