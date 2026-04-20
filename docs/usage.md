# Running the project

This document describes the available ways to run the project:

- locally,
- with Docker,
- with additional CLI arguments.

---

## Requirements

### Local run
- Python **3.10+**
- Google Chrome (installed locally)
- Zwift / ZwiftPower account
- a properly prepared `.env` file
- a prepared `team.xlsx` file

### Docker run
- Docker
- Docker Compose
- a properly prepared `.env` file
- a prepared `team.xlsx` file

---

## Local run

### Headless mode

```bash
python main.py --headless
```

### Example with additional parameters

```bash
python main.py -i team.xlsx -o updated_team.xlsx --headless --timeout 20 --sleep 0.6
```

### Run with a custom ID column

```bash
python main.py --headless --id-column-index 2
```

---

## Docker run

### First run / after image changes

```bash
docker compose run --rm --build zp-updater
```

### Next runs

```bash
docker compose run --rm zp-updater
```

> When run with Docker, the project works as a **one-time job**, not as a long-running service.

---

## Output

After the run, the script saves:

- `updated_team.xlsx` — the output file with updated data
- `errors.log` — the error / exception log file (if any errors occur)

---

## CLI arguments

Available arguments:

- `-i / --input` — input file (default: `team.xlsx`)
- `-o / --output` — output file (default: `updated_team.xlsx`)
- `--headless` — run Chrome in the background (without GUI)
- `--timeout` — Selenium timeout (seconds)
- `--sleep` — delay between profiles (seconds)
- `--log-file` — log file name (default: `errors.log`)
- `--id-column-index` — column index for the profile ID (0-based), default: `1`

---

## Usage examples

### 1. Default local run
```bash
python main.py --headless
```

### 2. Custom input and output file
```bash
python main.py -i riders.xlsx -o result.xlsx --headless
```

### 3. Higher timeout and longer delay between profiles
```bash
python main.py --headless --timeout 30 --sleep 1.0
```

### 4. Different profile ID column
```bash
python main.py --headless --id-column-index 0
```

### 5. Custom log file name
```bash
python main.py --headless --log-file updater.log
```

---

## Tests

If you want to run the tests locally:

```bash
pytest
```

You can also run a single test, for example:

```bash
pytest tests/test_cli_help.py
```

---

## CI / image publishing

The repository includes GitHub Actions workflows:

- `ci.yml` — the basic CI workflow
- `publish-dockerhub.yml` — Docker Hub image publishing

You can find the workflow files in:

```text
.github/workflows/
```