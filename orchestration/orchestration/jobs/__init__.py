from dagster import (
    AssetSelection,
    define_asset_job,
)
Raw_job = define_asset_job('Update_Raw', selection=AssetSelection.groups('Raw_Assets'))
ERD_job = define_asset_job('Create_Tables', selection=AssetSelection.groups('Actions_Assets', 'Market_Assets', 'Volume_Assets'))
all_jobs = [Raw_job, ERD_job]