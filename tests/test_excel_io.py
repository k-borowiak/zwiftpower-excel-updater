import pandas as pd
import pytest

from zp_updater.excel_io import (
    REQUIRED_COLUMNS,
    ensure_output_columns,
    extract_profile_ids,
    read_team_excel,
    validate_input_dataframe,
    write_team_excel,
)


def test_adds_missing_output_columns():
    df = pd.DataFrame({
        "Name": ["Alice"],
        "Power_1min": [300],
    })

    result = ensure_output_columns(df.copy())

    for col in REQUIRED_COLUMNS:
        assert col in result.columns

    assert result.loc[0, "Power_1min"] == 300
    assert pd.isna(result.loc[0, "Weight"])


def test_skips_invalid_profile_ids():
    df = pd.DataFrame({
        "Name": ["A", "B", "C", "D", "E"],
        "ProfileID": ["101", "abc", None, 202.0, "303"],
    })

    result = extract_profile_ids(df, id_col_index=1)

    assert result == [(0, 101), (3, 202), (4, 303)]


def test_handles_missing_id_column():
    df = pd.DataFrame({
        "OnlyColumn": ["x", "y", "z"],
    })

    result = extract_profile_ids(df, id_col_index=1)

    assert result == []


def test_excel_roundtrip(tmp_path):
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "ProfileID": [111, 222],
    })

    output_path = tmp_path / "team.xlsx"

    write_team_excel(df, output_path)
    loaded = read_team_excel(output_path)

    assert output_path.exists()
    pd.testing.assert_frame_equal(loaded, df, check_dtype=False)


def test_fails_when_id_column_is_missing():
    df = pd.DataFrame({
        "OnlyColumn": ["x", "y"],
    })

    with pytest.raises(ValueError, match="Brakuje kolumny z ID profilu"):
        validate_input_dataframe(df, id_col_index=1)


def test_fails_when_no_valid_ids():
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "ProfileID": ["abc", None],
    })

    with pytest.raises(ValueError, match="Nie znaleziono żadnego poprawnego ID profilu"):
        validate_input_dataframe(df, id_col_index=1)


def test_accepts_valid_dataframe():
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "ProfileID": ["123", "456"],
    })

    validate_input_dataframe(df, id_col_index=1)