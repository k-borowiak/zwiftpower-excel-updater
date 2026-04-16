import pandas as pd

from zp_updater.excel_io import (
    REQUIRED_COLUMNS,
    ensure_output_columns,
    extract_profile_ids,
    read_team_excel,
    write_team_excel,
)


def test_ensure_output_columns_adds_missing_columns():
    df = pd.DataFrame({
        "Name": ["Alice"],
        "Power_1min": [300],
    })

    result = ensure_output_columns(df.copy())

    for col in REQUIRED_COLUMNS:
        assert col in result.columns

    # istniejąca kolumna nie może zostać nadpisana
    assert result.loc[0, "Power_1min"] == 300

    # nowo dodana kolumna powinna być pusta
    assert pd.isna(result.loc[0, "Weight"])


def test_extract_profile_ids_returns_only_valid_ids():
    df = pd.DataFrame({
        "Name": ["A", "B", "C", "D", "E"],
        "ProfileID": ["101", "abc", None, 202.0, "303"],
    })

    result = extract_profile_ids(df, id_col_index=1)

    assert result == [(0, 101), (3, 202), (4, 303)]


def test_extract_profile_ids_returns_empty_list_when_column_missing():
    df = pd.DataFrame({
        "OnlyColumn": ["x", "y", "z"],
    })

    result = extract_profile_ids(df, id_col_index=1)

    assert result == []


def test_write_and_read_team_excel_roundtrip(tmp_path):
    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "ProfileID": [111, 222],
    })

    output_path = tmp_path / "team.xlsx"

    write_team_excel(df, output_path)
    loaded = read_team_excel(output_path)

    assert output_path.exists()
    pd.testing.assert_frame_equal(loaded, df, check_dtype=False)