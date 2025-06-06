from enum import Enum
import re
from typing import Any, Generator

import pandas


def fix_column_names(df: pandas.DataFrame) -> None:
    new_cols = [
        next(
            column_name
            for column_name in df.columns
            if not re.match(r"Unnamed: \d+", column_name)
            and not column_name.strip() == ""
        )
    ]
    for col in df.columns[1:]:
        col = col.strip()
        if re.match(r"Unnamed: \d+", col) or col.strip() == "":
            new_cols.append(new_cols[-1])
        else:
            new_cols.append(col)
    df.columns = new_cols


def strip_iterator(
    df: pandas.DataFrame, *columns: tuple[str]
) -> Generator[tuple[str | Any] | Any]:
    for row in zip(*(df[col] for col in columns)):
        current = tuple(
            (data.strip() if isinstance(data, str) else data) for data in row
        )
        if current == columns:
            continue
        if len(current) == 1:
            yield current[0]
        else:
            yield current


def remove_na(df: pandas.DataFrame) -> None:
    for col in df.columns:
        df[col] = df[col].fillna("")


def make_subdf(
    df: pandas.DataFrame, start_row: int, end_row: int = -1
) -> pandas.DataFrame:
    if end_row == -1:
        end_row = len(df)
    new_cols = df.iloc[start_row].to_list()
    df = df.iloc[start_row + 1 : end_row].copy()
    df.columns = new_cols
    df.reset_index(drop=True, inplace=True)
    return df


class MergeStrategy(Enum):
    FIRST = "first"
    CONCAT = "concat"
    FIRST_NON_EMPTY = "first_non_empty"


def _merge(to_merge: pandas.DataFrame, strategy: MergeStrategy) -> pandas.Series:
    match strategy:
        case MergeStrategy.FIRST:
            return to_merge.bfill(axis=1).iloc[:, 0]
        case MergeStrategy.CONCAT:
            return to_merge.apply(
                lambda row: "".join(
                    str(item) for item in row if item and not pandas.isna(item)
                ),
                axis=1,
            )
        case MergeStrategy.FIRST_NON_EMPTY:
            return to_merge.apply(
                lambda row: next(
                    (
                        item
                        for item in row
                        if not pandas.isna(item)
                        and (not isinstance(item, str) or item.strip()) != ""
                    ),
                    None,
                ),
                axis=1,
            )
        case _:
            raise ValueError(f"Unknown merge strategy: {strategy}")


def merge_duplicated_columns(
    df: pandas.DataFrame, merge_method: MergeStrategy
) -> pandas.DataFrame:
    cols = df.columns.unique()
    if len(cols) == len(df.columns):
        return df.copy()

    newdf = pandas.DataFrame(index=df.index)

    for col in cols:
        to_merge = df.loc[:, df.columns == col]
        merged = _merge(to_merge, merge_method)
        newdf[col] = merged

    return newdf
