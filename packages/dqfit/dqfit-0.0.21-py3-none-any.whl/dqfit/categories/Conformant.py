import pandas as pd
from dqfit.services import Query

struct_paths = Query.ig_struct_query()['path']

def score(dim: pd.Series) -> int:
    path  = dim['path']
    if path in list(struct_paths):
        return 1
    else:
        return 0