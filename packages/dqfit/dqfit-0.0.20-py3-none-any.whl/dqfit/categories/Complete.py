import pandas as pd
from typing import Any

def score(dim: pd.Series) -> int:
    value = dim['value']
    if dim['conformant'] == 0:
        return None
    elif type(value) == list and len(value) > 0:
        return 1
    elif pd.isna(value):
        return 0
    elif value in ["UNK","unk",""]:
        return 0
    elif len(value) > 0: # primary case?
        return 1
    else:
        return 0