# ZwiftPower Rider Data Pipeline

A Python-based automation project for collecting rider performance data from ZwiftPower and updating a structured Excel dataset for team management and analysis.

The project is built as a practical data workflow: scrape → transform → export. It is designed to be easy to run locally, reproducible in Docker, and ready for future cloud execution.

---

## Overview

Managing a Zwift team often means checking multiple rider profiles by hand and copying key metrics into a spreadsheet. That process is repetitive, slow, and easy to get wrong.

This project automates that workflow.

It logs into ZwiftPower through Zwift SSO, collects rider statistics, processes the results, and writes them into a clean Excel output file that can be used for team organization, comparison, and decision-making.

---

## What problem does it solve?

ZwiftPower does not provide a simple way to export structured rider performance data for team-wide use.

In practice, that usually means:

- opening rider profiles one by one,
- copying values manually,
- updating spreadsheets by hand,
- repeating the same work every time the data needs refreshing.

This project removes that manual step and turns it into a repeatable workflow.

---

## What the project does

The pipeline works like this:

```text
ZwiftPower → Scraper → Processing → Excel output
```

### Current workflow
1. Log in through Zwift SSO
2. Open ZwiftPower rider profiles
3. Extract rider data
4. Normalize and update the dataset
5. Save results to Excel

### Collected data
For each rider, the project collects:

- **Weight (kg)**
- **zFTP (W)**
- **Power metrics**
  - 15s
  - 1min
  - 5min
  - 20min

---

## Why this project matters

This is more than a one-off script.

The project is structured as a small but complete automation system with:

- modular Python code,
- input validation,
- reproducible Docker execution,
- automated tests,
- CI workflows,
- and a planned AWS runtime architecture.

It is a practical example of combining:
- scripting and scraping,
- data processing,
- packaging and delivery,
- and cloud-oriented system design.

---

## Quick start

### Local run

```bash
git clone <repo>
cd zwiftpower-excel-updater
cp .env.example .env
# fill in credentials

python main.py --headless
```

### Docker run

```bash
docker compose run --rm --build zp-updater
```

The output file will be saved as:

```text
updated_team.xlsx
```

> Full configuration, usage examples, and troubleshooting are documented in the `docs/` directory.

---

## Documentation

Detailed documentation is available here:

- Configuration → `docs/configuration.md`
- Usage → `docs/usage.md`
- Troubleshooting → `docs/troubleshooting.md`
- Architecture sketch → `docs/architecture/lambda-v1.png`
- Architecture note → `docs/architecture/lambda-v1.md`

---

## Architecture

The project is intentionally structured in layers:

- **Ingestion layer** → Selenium + BeautifulSoup
- **Processing layer** → Pandas
- **Output layer** → Excel (current)
- **Execution layer** → CLI / Docker
- **Planned cloud layer** → AWS Lambda-based scheduled execution

### Planned AWS architecture
- container image stored in **Amazon ECR**
- scheduled execution via **EventBridge Scheduler**
- input/output handled through **Amazon S3**
- secrets stored in **AWS Systems Manager Parameter Store**
- logs written to **Amazon CloudWatch Logs**

Architecture files:

- `docs/architecture/lambda-v1.drawio`
- `docs/architecture/lambda-v1.png`
- `docs/architecture/lambda-v1.md`

---

## Testing

The project includes basic automated tests covering:

- CLI help output,
- configuration loading,
- Excel read/write logic,
- module imports.

Run all tests with:

```bash
pytest
```

---

## Tech stack

### Application
- Python
- Pandas
- Selenium
- BeautifulSoup4
- python-dotenv
- openpyxl

### Delivery and automation
- Docker
- Docker Compose
- GitHub Actions
- Docker Hub

### Planned cloud layer
- AWS Lambda
- Amazon S3
- Amazon ECR
- Amazon EventBridge Scheduler
- AWS Systems Manager Parameter Store
- Amazon CloudWatch Logs
- Terraform

---

## Roadmap

### Completed
- core data extraction workflow
- Excel export
- Dockerized runtime
- CI workflow for tests and image build
- basic automated test coverage
- modular project structure
- AWS runtime architecture drafted

### Next steps
- infrastructure as code with Terraform
- AWS deployment for scheduled execution
- cloud-based input/output flow
- stronger runtime validation and error handling
- further improvement of automation and portability

---

## Disclaimer

Use this project in accordance with Zwift / ZwiftPower terms of service.

Only collect and use data that you are authorized to access, for example your own data or data used with team consent.

---

## Repository structure

```text
.
├─ .github/
│  └─ workflows/
│     ├─ ci.yml
│     └─ publish-dockerhub.yml
├─ docs/
│  ├─ configuration.md
│  ├─ usage.md
│  ├─ troubleshooting.md
│  └─ architecture/
│     ├─ lambda-v1.drawio
│     ├─ lambda-v1.md
│     └─ lambda-v1.png
├─ tests/
│  ├─ test_cli_help.py
│  ├─ test_config.py
│  ├─ test_excel_io.py
│  └─ test_imports.py
├─ zp_updater/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ excel_io.py
│  ├─ logging_utils.py
│  └─ scraper.py
├─ .dockerignore
├─ .env.example
├─ .gitignore
├─ Dockerfile
├─ README.md
├─ compose.yml
├─ main.py
├─ requirements.txt
└─ team.xlsx
```