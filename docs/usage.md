# Uruchamianie

Ten dokument opisuje sposoby uruchamiania projektu:

- lokalnie,
- przez Docker,
- z dodatkowymi argumentami CLI.

---

## Wymagania

### Uruchomienie lokalne
- Python **3.10+**
- Google Chrome (zainstalowany lokalnie)
- Konto Zwift / ZwiftPower
- poprawnie przygotowany plik `.env`
- przygotowany plik `team.xlsx`

### Uruchomienie przez Docker
- Docker
- Docker Compose
- poprawnie przygotowany plik `.env`
- przygotowany plik `team.xlsx`

---

## Uruchomienie lokalne

### Tryb headless

```bash
python main.py --headless
```

### Przykład z dodatkowymi parametrami

```bash
python main.py -i team.xlsx -o updated_team.xlsx --headless --timeout 20 --sleep 0.6
```

### Uruchomienie z własną kolumną ID

```bash
python main.py --headless --id-column-index 2
```

---

## Uruchomienie przez Docker

### Pierwsze uruchomienie / po zmianach w obrazie

```bash
docker compose run --rm --build zp-updater
```

### Kolejne uruchomienia

```bash
docker compose run --rm zp-updater
```

> Projekt uruchamiany przez Docker działa jako **jednorazowe zadanie**, a nie jako stale działająca usługa.

---

## Wynik działania

Po zakończeniu skrypt zapisuje:

- `updated_team.xlsx` — plik wynikowy z uzupełnionymi danymi
- `errors.log` — plik logów błędów / wyjątków (jeśli wystąpiły)

---

## Argumenty CLI

Dostępne argumenty:

- `-i / --input` — plik wejściowy (domyślnie `team.xlsx`)
- `-o / --output` — plik wyjściowy (domyślnie `updated_team.xlsx`)
- `--headless` — uruchom Chrome w tle (bez GUI)
- `--timeout` — timeout Selenium (sekundy)
- `--sleep` — opóźnienie między profilami (sekundy)
- `--log-file` — nazwa pliku logów (domyślnie `errors.log`)
- `--id-column-index` — indeks kolumny z ID (0-based), domyślnie `1`

---

## Przykładowe użycie

### 1. Domyślne uruchomienie lokalne
```bash
python main.py --headless
```

### 2. Własny plik wejściowy i wyjściowy
```bash
python main.py -i zawodnicy.xlsx -o wynik.xlsx --headless
```

### 3. Większy timeout i większe opóźnienie między profilami
```bash
python main.py --headless --timeout 30 --sleep 1.0
```

### 4. Inna kolumna z ID profilu
```bash
python main.py --headless --id-column-index 0
```

### 5. Własna nazwa pliku logów
```bash
python main.py --headless --log-file updater.log
```

---

## Testy

Jeśli chcesz uruchomić testy lokalnie:

```bash
pytest
```

Możesz też uruchomić pojedynczy test, np.:

```bash
pytest tests/test_cli_help.py
```

---

## CI / publikacja obrazu

W repo znajdują się workflow GitHub Actions:

- `ci.yml` — podstawowy workflow CI
- `publish-dockerhub.yml` — publikacja obrazu na Docker Hub

Szczegóły działania workflowów można znaleźć w katalogu:

```text
.github/workflows/
```
``