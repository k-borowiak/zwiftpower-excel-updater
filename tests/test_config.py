import pytest
import zp_updater.config as config


def test_fails_without_credentials(monkeypatch):
    # Blokuje ładowanie .env
    monkeypatch.setattr(config, "load_dotenv", lambda: None)

    # Usuwa zmienne środowiskowe, jeśli istnieją
    monkeypatch.delenv("ZP_USERNAME", raising=False)
    monkeypatch.delenv("ZP_PASSWORD", raising=False)

    with pytest.raises(ValueError, match="Brakuje danych logowania"):
        config.load_credentials()


def test_reads_credentials_from_env(monkeypatch):
    # Blokuje ładowanie .env
    monkeypatch.setattr(config, "load_dotenv", lambda: None)

    monkeypatch.setenv("ZP_USERNAME", "test_user")
    monkeypatch.setenv("ZP_PASSWORD", "test_pass")

    username, password = config.load_credentials()

    assert username == "test_user"
    assert password == "test_pass"