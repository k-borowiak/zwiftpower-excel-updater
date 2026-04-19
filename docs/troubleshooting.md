# Najczęstsze problemy

Ten dokument zbiera najczęstsze problemy związane z uruchamianiem projektu lokalnie i przez Docker.

---

## 1. Brakuje danych logowania w `.env`

Sprawdź:

- czy plik nazywa się dokładnie **`.env`**
- czy znajduje się w głównym katalogu projektu, obok `main.py`
- czy zawiera:
  - `ZP_USERNAME`
  - `ZP_PASSWORD`

Przykład poprawnego pliku:

```env
ZP_USERNAME=twoj_login
ZP_PASSWORD=twoje_haslo
```

---

## 2. Windows: problem z utworzeniem `.env`

Windows czasem utrudnia tworzenie plików z kropką na początku nazwy.  
Utwórz plik przez terminal:

```powershell
New-Item -Name ".env" -ItemType "file"
```

Następnie otwórz go i wklej dane logowania.

---

## 3. Nie znaleziono pliku wejściowego

Jeśli pojawia się błąd informujący o braku pliku wejściowego:

- sprawdź, czy plik istnieje,
- sprawdź, czy przekazana ścieżka jest poprawna,
- upewnij się, że uruchamiasz skrypt z właściwego katalogu.

Przykład:

```bash
python main.py -i team.xlsx --headless
```

---

## 4. Obsługiwany jest tylko plik `.xlsx`

Projekt obsługuje wyłącznie pliki Excela w formacie:

```text
.xlsx
```

Jeśli podasz plik `.txt`, `.csv`, `.xls` lub inny, pojawi się błąd walidacji.

---

## 5. Selenium / Chrome nie startuje

Jeśli przeglądarka nie uruchamia się poprawnie:

- zaktualizuj Google Chrome,
- zaktualizuj Selenium:

```bash
pip install -U selenium
```

- uruchom projekt bez `--headless`, żeby łatwiej zobaczyć, co się dzieje:

```bash
python main.py
```

---

## 6. Brak danych mocy z wykresu

ZwiftPower używa wykresów renderowanych w JavaScript (Highcharts).  
Jeśli strona zmieni strukturę lub selektory przestaną pasować, część danych może nie zostać pobrana.

W takim przypadku:

- sprawdź `errors.log`,
- sprawdź, czy profil ZwiftPower nadal ma oczekiwaną strukturę,
- sprawdź, czy nie zmieniły się selektory używane w scraperze.

---

## 7. Kontener Docker kończy działanie od razu

To normalne.

Projekt uruchamiany przez Docker działa jako **jednorazowe zadanie**, a nie jako usługa działająca w tle.  
Po zakończeniu przetwarzania kontener po prostu się zamyka.

---

## 8. Po zmianach w `Dockerfile` lub `requirements.txt` nic się nie zmienia

Uruchom projekt ponownie z przebudowaniem obrazu:

```bash
docker compose run --rm --build zp-updater
```

Jeśli nadal widzisz stare zachowanie, możesz dodatkowo usunąć lokalny obraz i zbudować go ponownie.

---

## 9. Skrypt działa niestabilnie przy wielu profilach

Jeśli pojawiają się losowe błędy lub scraping jest niestabilny:

- zwiększ timeout:

```bash
python main.py --headless --timeout 30
```

- dodaj większe opóźnienie między profilami:

```bash
python main.py --headless --sleep 1.0
```

To może pomóc, jeśli strona ładuje się wolniej lub wymaga więcej czasu na renderowanie danych.

---

## 10. Testy nie przechodzą

Sprawdź:

- czy masz zainstalowane zależności z `requirements.txt`,
- czy uruchamiasz testy z głównego katalogu projektu,
- czy środowisko wirtualne jest aktywne.

Uruchomienie wszystkich testów:

```bash
pytest
```

Uruchomienie pojedynczego testu:

```bash
pytest tests/test_config.py
```

---

## 11. Gdzie szukać dalszych informacji?

Jeśli problem dotyczy:

- konfiguracji → zobacz `docs/configuration.md`
- uruchamiania → zobacz `docs/usage.md`
- architektury AWS → zobacz `docs/architecture/lambda-v1.md`
``