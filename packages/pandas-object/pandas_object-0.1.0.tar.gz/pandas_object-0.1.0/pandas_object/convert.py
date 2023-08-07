from typing import List, Tuple, Any

from pandas import (
    DataFrame,
    Series,
)

class PandasObjectRow:

    def __init__(
        self,
        mapping
    ):
        self.row = dict()


class PandasObject:

    def __init__(
        self,
        df: DataFrame
    ):
        self.df = df
        self.columns = df.columns
        self.rows = [PandasObjectRow(i) for i in self.df.to_dict('records')]

    def __getattr__(self, name: str):
        try:
            handle = object.__getattribute__(self, name)
        except AttributeError:
            df = object.__getattribute__(self, 'df')
            if hasattr(df, name):
                return getattr(df, name)
        else:
            return handle

        raise AttributeError('Attribute %s not found.' % name)

    def __getitem__(self, index):
        return self.df[index]

    def __iter__(self):
        return self

    def __next__(self):
        for row in self.rows:
            yield row

