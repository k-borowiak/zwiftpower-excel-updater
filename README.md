# ZwiftPower → Excel Updater

Narzędzie w Pythonie, które automatycznie uzupełnia plik Excel (`team.xlsx`) o dane z profili ZwiftPower:

- **Weight (kg)**
- **zFTP (W)**
- **Power 15s / 1min / 5min / 20min (W)**

Skrypt loguje się przez Zwift SSO, pobiera dane ze strony profilu i zapisuje wyniki do nowego pliku Excel.

> ⚠️ Używaj zgodnie z regulaminem serwisu oraz tylko do legalnych celów (np. własne dane / zgoda zespołu).

---

## Cel projektu

Projekt został stworzony w celu **automatyzacji procesu zbierania i aktualizacji danych zawodników** z serwisu ZwiftPower, tak aby **ułatwić zarządzanie teamem kapitanom oraz osobom odpowiedzialnym za organizację składu**.

W praktyce zarządzanie zespołem często wymaga regularnego sprawdzania parametrów zawodników, takich jak masa ciała, zFTP czy wartości mocy na różnych odcinkach czasu. Ręczne wchodzenie na każdy profil osobno, kopiowanie danych i przenoszenie ich do Excela jest czasochłonne, powtarzalne i podatne na błędy.

Ten skrypt rozwiązuje ten problem poprzez:

- **automatyczne pobieranie danych wszystkich członków teamu**
- **zebranie ich w jednym, uporządkowanym pliku Excel**
- **ułatwienie aktualizacji danych bez ręcznego przepisywania**
- **przyspieszenie pracy kapitanów i managerów zespołu**
- **uproszczenie analizy oraz porównywania zawodników**

Dzięki temu zamiast ręcznie sprawdzać profile jednego po drugim, można w prosty sposób przygotować aktualny arkusz z najważniejszymi danymi całego zespołu. Pozwala to na **łatwiejsze zarządzanie teamem, szybsze podejmowanie decyzji oraz utrzymywanie wszystkich kluczowych informacji w jednym miejscu**.

Projekt został zaprojektowany przede wszystkim jako praktyczne narzędzie wspierające codzienną organizację pracy wokół teamu — szczególnie tam, gdzie liczy się szybki dostęp do aktualnych danych zawodników.

---

## Struktura projektu

```text
.
├─ main.py
├─ team.xlsx
├─ .env                 # plik lokalny z danymi logowania
└─ zp_updater/
   ├─ __init__.py
   ├─ config.py
   ├─ excel_io.py
   ├─ logging_utils.py
   └─ scraper.py
```

---

## Wymagania

- Python **3.10+**
- Google Chrome (zainstalowany lokalnie)
- Konto Zwift / ZwiftPower (login i hasło)

---

## Instalacja

### 1) Sklonuj repozytorium i przejdź do katalogu projektu

```bash
git clone https://github.com/<twoj-login>/zwiftpower-excel-updater.git
cd zwiftpower-excel-updater
```

### 2) (Zalecane) Utwórz środowisko wirtualne

```bash
python -m venv .venv
```

Aktywacja:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3) Zainstaluj zależności

```bash
pip install -r requirements.txt
```

---

## Konfiguracja: plik `.env` (login i hasło)

Skrypt pobiera dane logowania z pliku `.env`, aby nie trzymać sekretów w kodzie.

### Gdzie umieścić `.env`?

Plik `.env` musi znajdować się w **głównym katalogu projektu**, obok `main.py`:

```text
.
├─ main.py
├─ team.xlsx
└─ .env
```

### Jak utworzyć `.env`?

Utwórz plik tekstowy o nazwie dokładnie **`.env`** i wklej:

```env
ZP_USERNAME=twoj_login
ZP_PASSWORD=twoje_haslo
```

Jeśli hasło zawiera spacje lub nietypowe znaki, użyj cudzysłowów:

```env
ZP_USERNAME="twoj_login"
ZP_PASSWORD="hasło ze spacją"
```

### Bezpieczeństwo

- **Nie commituj `.env` do repozytorium**
- Upewnij się, że `.env` jest wpisany w `.gitignore`

**Opcjonalnie (dobra praktyka):** dodaj do repo plik `.env.example` bez sekretów:

```env
ZP_USERNAME=
ZP_PASSWORD=
```

Użytkownik może wtedy skopiować szablon:

**Linux/Mac:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

---

## Przygotowanie Excela (`team.xlsx`)

- Plik wejściowy domyślnie: **`team.xlsx`**
- ID profilu ZwiftPower powinno być w **kolumnie B** (druga kolumna)
- Skrypt dopisuje (jeśli brakuje) i/lub uzupełnia kolumny:

  - `Weight`
  - `zFTP`
  - `Power_15sec`
  - `Power_1min`
  - `Power_5min`
  - `Power_20min`

---

## Uruchomienie

Tryb headless (bez okna przeglądarki):

```bash
python main.py --headless
```

Przykład z parametrami:

```bash
python main.py -i team.xlsx -o updated_team.xlsx --headless --timeout 20 --sleep 0.6
```

Po zakończeniu powstaną:

- `updated_team.xlsx` — plik wynikowy z uzupełnionymi danymi
- `errors.log` — log błędów/wyjątków (jeśli jakiś profil nie przejdzie)

---

## Argumenty (opcjonalne)

- `-i / --input` — plik wejściowy (domyślnie `team.xlsx`)
- `-o / --output` — plik wyjściowy (domyślnie `updated_team.xlsx`)
- `--headless` — uruchom Chrome w tle (bez GUI)
- `--timeout` — timeout Selenium (sekundy)
- `--sleep` — opóźnienie między profilami (sekundy; pomaga stabilności)
- `--log-file` — nazwa pliku logów (domyślnie `errors.log`)
- `--id-column-index` — indeks kolumny z ID (0-based), domyślnie `1` (kolumna B)

---

## Najczęstsze problemy

### 1) „Brakuje danych logowania w .env…”

Sprawdź:

- czy plik nazywa się dokładnie **`.env`** (nie `.env.txt`)
- czy jest obok `main.py`
- czy zawiera `ZP_USERNAME` i `ZP_PASSWORD`

### 2) Windows: problem z utworzeniem `.env`

Windows czasem utrudnia tworzenie plików z kropką na początku nazwy. Utwórz plik przez terminal:

```powershell
New-Item -Name ".env" -ItemType "file"
```

Następnie edytuj go i wklej `ZP_USERNAME` / `ZP_PASSWORD`.

### 3) Selenium/Chrome nie startuje

- zaktualizuj Chrome
- zaktualizuj Selenium:

```bash
pip install -U selenium
```

- uruchom bez headless (diagnostyka):

```bash
python main.py
```

### 4) Brak danych mocy z wykresu

ZwiftPower używa wykresów renderowanych w JS (Highcharts). Skrypt ma fallback, ale jeśli strona zmieni strukturę, selektory mogą wymagać aktualizacji. Szczegóły będą w `errors.log`.

---

## Technologie

Python, Pandas, Selenium, BeautifulSoup4, python-dotenv, openpyxl

---

## Roadmap / Dalszy rozwój

Obecna wersja projektu działa jako lokalne narzędzie automatyzujące pobieranie danych z profili ZwiftPower i aktualizację pliku Excel. Kolejnym krokiem jest rozwój projektu w kierunku łatwiejszego wdrażania, większej powtarzalności środowiska oraz lepszej automatyzacji uruchomienia.

Planowane kierunki rozwoju:

- [ ] Dodanie `Dockerfile` do uruchamiania aplikacji w kontenerze
- [ ] Przygotowanie obrazu zawierającego wszystkie wymagane zależności (`Python`, `Selenium`, `Chrome/Chromium`)
- [x] Dodanie `.env.example` jako szablonu konfiguracji
- [ ] Dodanie testów dla modułów niezależnych od Selenium
- [ ] Rozbudowa walidacji pliku wejściowego i komunikatów błędów
- [ ] Możliwość uruchamiania cyklicznego (np. cron / harmonogram zadań)
- [ ] Opcjonalny eksport danych do CSV

Docelowo projekt ma być rozwijany nie tylko jako skrypt automatyzacyjny, ale jako bardziej kompletne i przenośne narzędzie, które można łatwo uruchomić w różnych środowiskach.
