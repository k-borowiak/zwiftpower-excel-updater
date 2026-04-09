from __future__ import annotations

import argparse
import time
from pathlib import Path

from zp_updater.config import load_credentials
from zp_updater.excel_io import (
    read_team_excel,
    extract_profile_ids,
    ensure_output_columns,
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logger = setup_logging(log_file=args.log_file)

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        logger.error("Nie znaleziono pliku wejściowego: %s", input_path)
        return 2

    # 1) wczytaj dane i przygotuj ramkę
    df = read_team_excel(input_path)
    df = ensure_output_columns(df)

    # 2) wyciągnij ID profili z wybranej kolumny (domyślnie B)
    ids = extract_profile_ids(df, id_col_index=args.id_column_index)
    if not ids:
        logger.error("Nie znaleziono żadnych poprawnych ID profili w kolumnie index=%s", args.id_column_index)
        return 3

    # 3) wczytaj dane logowania
    username, password = load_credentials()

    # 4) zaloguj i scrapuj
    client = ZwiftPowerClient(headless=args.headless, timeout=args.timeout, logger=logger)

    try:
        client.login(username=username, password=password)

        logger.info("Znaleziono %d ID do przetworzenia.", len(ids))

        for row_idx, profile_id in ids:
            logger.info("Pobieram dane dla ID=%s (wiersz=%s)", profile_id, row_idx)

            data = client.scrape_profile(profile_id=profile_id)

            # zapis po NAZWACH kolumn (odporniejsze niż iat)
            df.loc[row_idx, "Weight"] = data.weight
            df.loc[row_idx, "zFTP"] = data.zftp
            df.loc[row_idx, "Power_15sec"] = data.power_15s
            df.loc[row_idx, "Power_1min"] = data.power_1m
            df.loc[row_idx, "Power_5min"] = data.power_5m
            df.loc[row_idx, "Power_20min"] = data.power_20m

            if args.sleep > 0:
                time.sleep(args.sleep)

    finally:
        client.close()

    # 5) zapisz wynik
    write_team_excel(df, output_path)
    logger.info("Gotowe! Zapisano: %s", output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())