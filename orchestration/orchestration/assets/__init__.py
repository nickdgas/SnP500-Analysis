from dagster import (
    load_assets_from_modules,
)
from . import (
    Raw_Assets,
    ERD_Assets,
)
all_assets = load_assets_from_modules([Raw_Assets, ERD_Assets])