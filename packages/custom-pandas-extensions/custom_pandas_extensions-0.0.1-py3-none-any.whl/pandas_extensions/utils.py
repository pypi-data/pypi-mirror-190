import pandas as pd
import pandas_flavor as pf

def _set_keys(df: pd.DataFrame, keys: list=None):
    if keys is None:
        keys = list(df.columns)
    
    return keys
    
@pf.register_dataframe_method
def levelsof(df: pd.DataFrame, keys: list=None) -> list[tuple]:
    keys = _set_keys(df, keys)

    levels = (
        df.drop_duplicates(subset=keys)
            .dropna(subset=keys)
            .itertuples(index=False)
    )

    return list(levels)

@pf.register_dataframe_method
def isid(df: pd.DataFrame, keys: list=None) -> bool:
    keys = _set_keys(df, keys)

    return df.set_index(keys).index.is_unique

@pf.register_dataframe_method
def group(df: pd.DataFrame, keys: list=None) -> bool:
    pass


