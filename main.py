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
        description="Uzupełnia Excel danymi z profili ZwiftPower (Weight, zFTP, moce z wykresu)."
    )
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT, help="Plik wejściowy XLSX (domyślnie team.xlsx)")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Plik wynikowy XLSX (domyślnie updated_team.xlsx)")
    parser.add_argument("--headless", action="store_true", help="Uruchom Chrome w trybie headless")
    parser.add_argument("--timeout", type=int, default=15, help="Timeout (sekundy) dla Selenium wait (domyślnie 15)")
    parser.add_argument("--sleep", type=float, default=0.4, help="Opóźnienie między profilami (sekundy) (domyślnie 0.4)")
    parser.add_argument("--log-file", default="errors.log", help="Plik logów (domyślnie errors.log)")
    parser.add_argument("--id-column-index", type=int, default=1, help="Indeks kolumny z ID (0-based), domyślnie 1 (kolumna B)")

    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout musi być większy od 0")

    if args.sleep < 0:
        parser.error("--sleep nie może być ujemny")

    if args.id_column_index < 0:
        parser.error("--id-column-index nie może być ujemny")

    return args


def validate_input_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku wejściowego: {path}")

    if path.suffix.lower() != ".xlsx":
        raise ValueError("Obsługiwany jest tylko plik .xlsx")


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
        logger.exception("Nie udało się wczytać lub zwalidować pliku wejściowego.")
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

        logger.info("Znaleziono %d ID do przetworzenia.", len(ids))

        for row_idx, profile_id in ids:
            logger.info("Pobieram dane dla ID=%s (wiersz=%s)", profile_id, row_idx)

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
        logger.exception("Wystąpił błąd podczas logowania lub pobierania danych ze ZwiftPower.")
        return 6
    finally:
        if client is not None:
            client.close()

    # zapisz wynik
    try:
        write_team_excel(df, output_path)
    except Exception:
        logger.exception("Nie udało się zapisać pliku wynikowego: %s", output_path)
        return 7

    logger.info("Gotowe! Zapisano: %s", output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())