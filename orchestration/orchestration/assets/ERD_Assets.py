import pandas as pd
import numpy as np
from dagster import (
    asset,
    multi_asset,
    AssetOut,
)
def merge_dfs(df1: pd.DataFrame, df2: pd.DataFrame, left: str, right: str) -> pd.DataFrame:
    '''
    Merge dataframes on column
    '''
    merged = df1.merge(df2, left_on=left, right_on=right)
    return merged

@asset(name='Volume_Staging', group_name='Volume_Assets')
def stage_Volume(Raw_Data: pd.DataFrame) -> pd.DataFrame:
    dfRaw = Raw_Data
    dfRaw = dfRaw[['Date', 'Symbol', 'Volume']]
    return dfRaw

@asset(name='Actions_Staging', group_name='Actions_Assets')
def stage_Actions(Raw_Data: pd.DataFrame) -> pd.DataFrame:
    dfRaw = Raw_Data
    dfRaw = dfRaw[['Date', 'Symbol', 'Dividends', 'Stock Splits']]
    return dfRaw

@asset(name='Market_Staging', group_name='Market_Assets')
def stage_Market(Raw_Data: pd.DataFrame) -> pd.DataFrame: 
    dfRaw = Raw_Data
    return dfRaw

@multi_asset(name='ERD_Initialize', group_name='Market_Assets', outs={'Security': AssetOut(), 'Date': AssetOut(), 'Type': AssetOut()})
def create_Tables(Raw_Data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dfRaw = Raw_Data
    # security table
    dfSec = dfRaw.drop_duplicates(subset='Symbol', keep='first').rename(columns={'Symbol': 'Short Name', 'Security': 'Long Name', 'GICS Sector': 'Industry Sector', 'GICS Sub-Industry': 'Industry Group'})
    dfSec.insert(0, 'ID', dfSec.index+1)
    dfSec = dfSec[['ID', 'Short Name', 'Long Name', 'Industry Sector', 'Industry Group', 'CIK']]
    # date table
    dfDate = pd.DataFrame()
    dfDate['Date'] = dfRaw['Date'].drop_duplicates(keep='first')
    dfDate['ID'] = dfDate['Date'].astype('string').str.replace('-','', regex=True).astype('int64')
    dfDate = dfDate[['ID', 'Date']]
    # type table
    dfType = dfRaw.melt(id_vars='Symbol',value_vars=['Open', 'High', 'Low', 'Close'], var_name='Type')
    dfType = dfType.drop_duplicates(subset='Type', keep='first')
    dfType = dfType[['Type']].reset_index(drop=True)
    dfType.insert(0, 'ID', dfType.index+1)
    return dfSec, dfDate, dfType

@asset(name='Volume', group_name='Volume_Assets')
def update_Volume(Volume_Staging: pd.DataFrame, Security: pd.DataFrame, Date: pd.DataFrame) -> pd.DataFrame:
    dfSecurity = Security
    dfSecurity = dfSecurity[['ID', 'Short Name']].rename(columns={'ID': 'SecurityID'})
    dfDate = Date
    dfDate = dfDate.rename(columns={'ID': 'ReportDateID'})
    dfVolume = Volume_Staging.merge(dfSecurity, left_on='Symbol', right_on='Short Name')
    dfVolume = dfVolume.merge(dfDate, left_on='Date', right_on='Date')
    dfVolume = dfVolume[['ReportDateID', 'SecurityID', 'Volume']]
    return dfVolume

@asset(name='Actions', group_name='Actions_Assets')
def update_Actions(Actions_Staging: pd.DataFrame, Security: pd.DataFrame) -> pd.DataFrame:
    dfSecurity  = Security
    dfSecurity = dfSecurity[['ID', 'Short Name']].rename(columns={'ID': 'SecurityID'})
    # normalize data, insert columns; merge using Security ID
    dfActions = Actions_Staging.merge(dfSecurity, left_on='Symbol', right_on='Short Name')
    dfActions['Is Current'] = np.where((dfActions['Dividends'] != 0) | (dfActions['Stock Splits'] != 0), 1, 0)
    current = pd.Timestamp.max.strftime('%Y-%m-%d')
    dfActions = dfActions.loc[dfActions['Is Current'] == 1] 
    dfActions = dfActions[['SecurityID', 'Dividends', 'Stock Splits', 'Is Current', 'Date']].rename(columns={'Date': 'Start Date'})
    dfActions['Is Current'] = (dfActions.groupby('SecurityID')['Start Date'].transform('last') == dfActions['Start Date']).astype(int)
    dfActions['End Date'] = dfActions.groupby('SecurityID')['Start Date'].transform('last')
    dfActions.loc[dfActions['Is Current'] == 1, 'End Date'] = current
    return dfActions

@asset(name='Market', group_name='Market_Assets')
def update_Market(Market_Staging: pd.DataFrame, Security: pd.DataFrame, Date: pd.DataFrame, Type: pd.DataFrame) -> pd.DataFrame:
    dfSecurity = Security 
    dfSecurity = dfSecurity[['ID', 'Short Name']].rename(columns={'ID': 'SecurityID'})
    dfDate = Date
    dfDate = dfDate.rename(columns={'ID': 'ReportDateID'})
    dfType = Type
    dfType = dfType.rename(columns={'ID': 'TypeID'})
    # group merge on 'Symbol' column; single merge on 'Date' column
    dfMarket = merge_dfs(Market_Staging, dfSecurity, 'Symbol', 'Short Name')
    dfMarket = merge_dfs(dfMarket, dfDate, 'Date', 'Date')
    # unpivot price types for single merge 
    dfMarket = dfMarket.melt(id_vars=['SecurityID', 'ReportDateID'],value_vars=['Open', 'High', 'Low', 'Close'], var_name='Type', value_name='Price')
    dfMarket = merge_dfs(dfMarket, dfType, 'Type', 'Type')
    # filter columns; insert ID column
    dfMarket = dfMarket[['ReportDateID', 'SecurityID', 'TypeID', 'Price']]
    dfMarket.insert(0, 'ID', dfMarket.index+1)
    return dfMarket