# Konfiguracja

Ten dokument opisuje podstawową konfigurację projektu:

- dane logowania w pliku `.env`,
- przygotowanie pliku wejściowego `team.xlsx`,
- oczekiwany układ danych wejściowych i wyjściowych.

---

## Plik `.env`

Skrypt pobiera dane logowania z pliku `.env`, aby nie trzymać sekretów w kodzie.

Plik `.env` musi znajdować się w **głównym katalogu projektu**, obok `main.py`:

```text
.
├─ main.py
├─ team.xlsx
└─ .env
```

### Przykład zawartości

```env
ZP_USERNAME=twoj_login
ZP_PASSWORD=twoje_haslo
```

Jeśli hasło zawiera spacje lub nietypowe znaki, użyj cudzysłowów:

```env
ZP_USERNAME="twoj_login"
ZP_PASSWORD="hasło ze spacją"
```

---

## `.env.example`

W repo znajduje się przykładowy plik `.env.example`, który można skopiować jako bazę do lokalnej konfiguracji:

**Linux/Mac**
```bash
cp .env.example .env
```

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env
```

Następnie uzupełnij wartości `ZP_USERNAME` i `ZP_PASSWORD`.

---

## Bezpieczeństwo

- **Nie commituj `.env` do repozytorium**
- Upewnij się, że `.env` znajduje się w `.gitignore`
- Nie przechowuj danych logowania bezpośrednio w kodzie ani w skryptach uruchomieniowych

---

## Plik wejściowy `team.xlsx`

Domyślny plik wejściowy to:

```text
team.xlsx
```

### Wymagania dotyczące pliku

- plik musi być w formacie **`.xlsx`**
- domyślnie ID profilu ZwiftPower powinno znajdować się w **kolumnie B**
- odpowiada to argumentowi:

```text
--id-column-index 1
```

> Uwaga: indeks kolumny jest **0-based**, czyli:
> - `0` = kolumna A
> - `1` = kolumna B
> - `2` = kolumna C

Jeśli w Twoim pliku ID znajduje się w innej kolumnie, użyj argumentu `--id-column-index`.

### Przykład

```bash
python main.py --id-column-index 2
```

---

## Kolumny uzupełniane przez skrypt

Skrypt dopisuje (jeśli brakuje) i/lub uzupełnia następujące kolumny:

- `Weight`
- `zFTP`
- `Power_15sec`
- `Power_1min`
- `Power_5min`
- `Power_20min`

---

## Plik wyjściowy

Domyślny plik wynikowy to:

```text
updated_team.xlsx
```

Możesz wskazać inną nazwę pliku wyjściowego za pomocą argumentu `-o / --output`.

Przykład:

```bash
python main.py -o wynik.xlsx --headless
```

---

## Plik logów

Domyślnie błędy i wyjątki są zapisywane do pliku:

```text
errors.log
```

Nazwę pliku logów można zmienić przez argument:

```text
--log-file
```

Przykład:

```bash
python main.py --log-file updater.log --headless
```