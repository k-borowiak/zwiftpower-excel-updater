from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str = "errors.log") -> logging.Logger:
    """
    Konfiguracja loggera:
    - INFO na konsolę
    - DEBUG/ERROR do pliku rotowanego
    """
    logger = logging.getLogger("zp_updater")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger  # unikamy podwójnych handlerów przy wielokrotnych uruchomieniach

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # konsola
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # plik (rotacja)
    fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
