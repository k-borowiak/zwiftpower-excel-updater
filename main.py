from __future__ import annotations

import argparse
import time
from pathlib import Path

from zp_updater.config import load_credentials
from zp_updater.excel_io import (
    read_team_excel,
    extract_profile_ids,
    ensure_output_columns,
    validate_input_dataframe,
    write_team_excel,
)
from zp_updater.logging_utils import setup_logging
from zp_updater.scraper import ZwiftPowerClient


DEFAULT_INPUT = "team.xlsx"
DEFAULT_OUTPUT = "updated_team.xlsx"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill an Excel file with data from ZwiftPower profiles (Weight, zFTP, and power values from the chart)."
    )
    parser.add_argument(
        "--input",
        "-i",
        default=DEFAULT_INPUT,
        help="Input XLSX file (default: team.xlsx)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=DEFAULT_OUTPUT,
        help="Output XLSX file (default: updated_team.xlsx)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Selenium wait timeout in seconds (default: 15)",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.4,
        help="Delay between profiles in seconds (default: 0.4)",
    )
    parser.add_argument(
        "--log-file",
        default="errors.log",
        help="Log file path (default: errors.log)",
    )
    parser.add_argument(
        "--id-column-index",
        type=int,
        default=1,
        help="Profile ID column index (0-based), default: 1 (column B)",
    )

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")

    if args.sleep < 0:
        parser.error("--sleep cannot be negative")

    if args.id_column_index < 0:
        parser.error("--id-column-index cannot be negative")

    return args


def validate_input_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() != ".xlsx":
        raise ValueError("Only .xlsx files are supported")


def main() -> int:
    args = parse_args()
    logger = setup_logging(log_file=args.log_file)

    input_path = Path(args.input)
    output_path = Path(args.output)

    # walidacja pliku wejściowego + wczytanie danych
    try:
        validate_input_file(input_path)
        df = read_team_excel(input_path)
        df = ensure_output_columns(df)
        validate_input_dataframe(df, id_col_index=args.id_column_index)
        ids = extract_profile_ids(df, id_col_index=args.id_column_index)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 2
    except ValueError as e:
        logger.error(str(e))
        return 3
    except Exception:
        logger.exception("Failed to load or validate the input file.")
        return 4

    # wczytaj dane logowania
    try:
        username, password = load_credentials()
    except ValueError as e:
        logger.error(str(e))
        return 5

    # zaloguj i scrapuj
    client = None
    try:
        client = ZwiftPowerClient(headless=args.headless, timeout=args.timeout, logger=logger)
        client.login(username=username, password=password)

        logger.info("Found %d profile IDs to process.", len(ids))

        for row_idx, profile_id in ids:
            logger.info("Fetching data for ID=%s (row=%s)", profile_id, row_idx)

            data = client.scrape_profile(profile_id=profile_id)

            df.loc[row_idx, "Weight"] = data.weight
            df.loc[row_idx, "zFTP"] = data.zftp
            df.loc[row_idx, "Power_15sec"] = data.power_15s
            df.loc[row_idx, "Power_1min"] = data.power_1m
            df.loc[row_idx, "Power_5min"] = data.power_5m
            df.loc[row_idx, "Power_20min"] = data.power_20m

            if args.sleep > 0:
                time.sleep(args.sleep)

    except Exception:
        logger.exception("An error occurred while logging in or fetching data from ZwiftPower.")
        return 6
    finally:
        if client is not None:
            client.close()

    # zapisz wynik
    try:
        write_team_excel(df, output_path)
    except Exception:
        logger.exception("Failed to save the output file: %s", output_path)
        return 7

    logger.info("Done! Saved to: %s", output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())