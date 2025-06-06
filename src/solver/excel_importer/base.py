from abc import ABC, abstractmethod
import re
from typing import Any, Generator, IO

import pandas

class Importer(ABC):

    def _fix_column_names(self, df: pandas.DataFrame) -> None:
        new_cols = [
            next(
                column_name
                for column_name in df.columns
                if not re.match(r"Unnamed: \d+", column_name)
            )
        ]
        for col in df.columns[1:]:
            col = col.strip()
            if re.match(r"Unnamed: \d+", col):
                new_cols.append(new_cols[-1])
            else:
                new_cols.append(col)
        df.columns = new_cols

    def _strip_iterator(self, df: pandas.DataFrame, *columns: tuple[str]) -> Generator[tuple[str | Any] | Any]:
        for row in zip(*(df[col] for col in columns)):
            current = tuple(
                (data.strip() if isinstance(data, str) else data)
                for data in row
            )
            if len(current) == 1:
                yield current[0]
            else:
                yield current

    def _remove_na(self, df: pandas.DataFrame) -> None:
        for _, subdf in df.items():
            subdf.fillna("", inplace=True)

    @abstractmethod
    def import_data(self, readable_buffer: IO[bytes]) -> dict:
        pass
