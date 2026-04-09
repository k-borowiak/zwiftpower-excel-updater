from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import pandas as pd


REQUIRED_COLUMNS = ["Weight", "zFTP", "Power_15sec", "Power_1min", "Power_5min", "Power_20min"]


def read_team_excel(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, engine="openpyxl")


def ensure_output_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dodaje brakujące kolumny wyjściowe. Niczego nie przemianowuje po indeksie.
    """
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    return df


def extract_profile_ids(df: pd.DataFrame, id_col_index: int = 1) -> List[Tuple[int, int]]:
    """
    Zwraca listę (row_index, profile_id_int) dla poprawnych ID z kolumny `id_col_index`.

    - Czyści wartości do numerów (pd.to_numeric)
    - Pomija NaN
    - Rzutuje do int
    """
    if df.shape[1] <= id_col_index:
        return []

    raw = df.iloc[:, id_col_index]
    numeric = pd.to_numeric(raw, errors="coerce")

    out: List[Tuple[int, int]] = []
    for row_idx, val in numeric.items():
        if pd.isna(val):
            continue
        try:
            out.append((row_idx, int(val)))
        except (ValueError, TypeError):
            continue
    return out


def write_team_excel(df: pd.DataFrame, path: Path) -> None:
    df.to_excel(path, index=False, engine="openpyxl")