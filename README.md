# ZwiftPower → Excel Updater

Narzędzie w Pythonie, które automatycznie uzupełnia plik Excel (`team.xlsx`) o dane z profili ZwiftPower:

- **Weight (kg)**
- **zFTP (W)**
- **Power 15s / 1min / 5min / 20min (W)**

Skrypt loguje się przez Zwift SSO, pobiera dane ze strony profilu i zapisuje wyniki do nowego pliku Excel.

Projekt można uruchamiać zarówno **lokalnie**, jak i w **kontenerze Docker**.

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
├─ .env.example         # przykładowy szablon konfiguracji
├─ .gitignore           # pliki i katalogi ignorowane przez Git
├─ .dockerignore        # pliki pomijane przy budowaniu obrazu
├─ Dockerfile           # definicja obrazu Docker
├─ compose.yaml         # konfiguracja uruchomienia przez Docker Compose
└─ zp_updater/
   ├─ __init__.py
   ├─ config.py
   ├─ excel_io.py
   ├─ logging_utils.py
   └─ scraper.py
```

---

## Wymagania

### Uruchomienie lokalne
- Python **3.10+**
- Google Chrome (zainstalowany lokalnie)
- Konto Zwift / ZwiftPower (login i hasło)

### Uruchomienie przez Docker
- Docker
- Docker Compose
- Konto Zwift / ZwiftPower (login i hasło)

---

## Instalacja

### 1) Sklonuj repozytorium i przejdź do katalogu projektu

```bash
git clone https://github.com/<twoj-login>/zwiftpower-excel-updater.git
cd zwiftpower-excel-updater
```

### 2) (Zalecane) Utwórz środowisko wirtualne — tylko dla uruchomienia lokalnego

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

### 3) Zainstaluj zależności — tylko dla uruchomienia lokalnego

```bash
pip install -r requirements.txt
```

### 4) Docker — bez lokalnej instalacji Pythona i Chrome

Jeśli uruchamiasz projekt przez Docker, nie musisz lokalnie instalować Pythona ani Google Chrome. Wystarczy poprawnie skonfigurowany Docker / Docker Compose oraz plik `.env`.

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

### Uruchomienie lokalne

Tryb headless (bez okna przeglądarki):

```bash
python main.py --headless
```

Przykład z parametrami:

```bash
python main.py -i team.xlsx -o updated_team.xlsx --headless --timeout 20 --sleep 0.6
```

### Uruchomienie przez Docker

Pierwsze uruchomienie / po zmianach w obrazie:

```bash
docker compose run --rm --build zp-updater
```

Kolejne uruchomienia:

```bash
docker compose run --rm zp-updater
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

### 5) Kontener Docker kończy działanie od razu

To normalne — projekt uruchamiany jest jako jednorazowe zadanie, a nie jako stale działająca usługa.

### 6) Po zmianach w `Dockerfile` lub `requirements.txt` nic się nie zmienia

Uruchom ponownie projekt z opcją `--build`:

```bash
docker compose run --rm --build zp-updater
```

---

## Technologie

Python, Pandas, Selenium, BeautifulSoup4, python-dotenv, openpyxl, Docker, Docker Compose

---

## Roadmap / Dalszy rozwój

Obecna wersja projektu działa zarówno lokalnie, jak i w kontenerze Docker, co daje już prostszy setup oraz bardziej powtarzalne środowisko uruchomieniowe. Kolejne kroki to uporządkowanie warstwy konfiguracyjnej i walidacji, dodanie podstawowych testów dla modułów niezależnych od Selenium oraz przygotowanie projektu pod bardziej automatyczne uruchamianie i wdrażanie.


Planowane kierunki rozwoju:

- [x] Dodanie `Dockerfile` do uruchamiania aplikacji w kontenerze
- [x] Przygotowanie obrazu zawierającego wszystkie wymagane zależności (`Python`, `Selenium`, `Chrome/Chromium`)
- [x] Dodanie `.env.example` jako szablonu konfiguracji
- [x] Dodanie `compose.yaml` do wygodnego uruchamiania projektu przez Docker Compose
- [ ] Uporządkowanie konfiguracji pod bardziej bezobsługowe uruchamianie
- [x] Dodanie podstawowych testów smoke (importy, CLI)
- [x] Dodanie testów dla modułów niezależnych od Selenium
- [x] Rozbudowa walidacji pliku wejściowego i komunikatów błędów
- [x] Dodanie prostego workflow CI (GitHub Actions: test / build obrazu)
- [x] Automatyczna publikacja obrazu na Docker Hub (GitHub Actions)
- [ ] Przygotowanie infrastruktury jako kodu (Terraform)
- [ ] Weryfikacja uruchamiania projektu w AWS (np. jako zadanie uruchamiane okresowo)
- [ ] Opcjonalny eksport danych do CSV


Docelowo projekt ma rozwijać się z prostego skryptu automatyzacyjnego w bardziej kompletne i przenośne narzędzie, które można łatwo uruchomić lokalnie, w Dockerze, a w kolejnym etapie również wdrażać i utrzymywać w środowisku chmurowym z wykorzystaniem Terraform oraz wybranego sposobu uruchamiania zadań.
