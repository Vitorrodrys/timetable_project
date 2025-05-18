from abc import ABC, abstractmethod
from typing import IO
import re
import pandas

class ExcelImporter(ABC):
    """
    Abstract base class for Excel importers.
    """

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

    def _remove_na(self, df: pandas.DataFrame) -> None:
        for _, subdf in df.items():
            subdf.fillna("", inplace=True)

    @abstractmethod
    def import_data(self, readbable_buffer: IO[bytes]) -> tuple[bool, str]:
        """
        Import data from an Excel file-like to database.

        Raises:
            ValueError: if some misformated data is found in the file.
        """
