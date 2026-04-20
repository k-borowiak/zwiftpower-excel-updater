from __future__ import annotations

import os
from dotenv import load_dotenv


def load_credentials() -> tuple[str, str]:
    """
    Ładuje ZP_USERNAME i ZP_PASSWORD z pliku .env / zmiennych środowiskowych.
    """
    load_dotenv()
    username = os.getenv("ZP_USERNAME")
    password = os.getenv("ZP_PASSWORD")

    if not username or not password:
        raise ValueError("Missing login credentials in .env file (ZP_USERNAME, ZP_PASSWORD)")
    return username, password