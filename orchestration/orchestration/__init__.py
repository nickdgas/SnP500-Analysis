from dagster import (
    Definitions,
)
from .assets import (
    all_assets,
)
from .jobs import (
    all_jobs,
)
defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
)
