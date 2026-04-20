# ZwiftPower → Excel Updater

A Python tool that automatically fills an Excel file (`team.xlsx`) with data from ZwiftPower rider profiles:

- **Weight (kg)**
- **zFTP (W)**
- **Power 15s / 1min / 5min / 20min (W)**

The script logs in through Zwift SSO, collects data from the rider profile page, and saves the results to a new Excel file.

The project can be run both **locally** and in a **Docker container**.

> ⚠️ Use this tool in line with the service terms and only for legal purposes (for example, your own data or data used with team consent).

---

## Quick start

### Local run
1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your login details
3. Prepare the `team.xlsx` file
4. Run:

```bash
python main.py --headless
```

### Docker run
```bash
docker compose run --rm --build zp-updater
```

After the run, the script will save `updated_team.xlsx`.

---

## Project purpose

This project was created to automate the process of collecting and updating rider data from ZwiftPower, so it is easier to manage a team and prepare an up-to-date spreadsheet with rider data.

In practice, the script:

- collects data for all team members listed in the Excel file,
- gathers everything into one organized file,
- removes the need for manual copying,
- speeds up the work of team captains and managers,
- makes it easier to analyze and compare riders.

Instead of opening profiles one by one by hand, you can quickly prepare an up-to-date spreadsheet with the most important data for the whole team.

---

## Documentation

Detailed information has been split into separate files:

- configuration: `docs/configuration.md`
- running the project: `docs/usage.md`
- common problems: `docs/troubleshooting.md`
- AWS architecture sketch: `docs/architecture/lambda-v1.png`
- architecture note: `docs/architecture/lambda-v1.md`

---

## Requirements

### Local run
- Python **3.10+**
- Google Chrome (installed locally)
- Zwift / ZwiftPower account (login and password)

### Docker run
- Docker
- Docker Compose
- Zwift / ZwiftPower account (login and password)

---

## Project structure

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

---

## AWS architecture (initial sketch)

![Lambda architecture](docs/architecture/lambda-v1.png)

- diagram source: `docs/architecture/lambda-v1.drawio`
- architecture note: `docs/architecture/lambda-v1.md`

Assumptions:
- the container image is stored in ECR
- the job is triggered by EventBridge Scheduler
- the input and output files are stored in S3
- login credentials are stored in Parameter Store
- logs are written to CloudWatch Logs

---

## Technologies

### Application
Python, Pandas, Selenium, BeautifulSoup4, python-dotenv, openpyxl

### Running and delivery
Docker, Docker Compose, GitHub Actions, Docker Hub

### Tests
pytest

### Planned / designed cloud layer
AWS Lambda, Amazon ECR, Amazon S3, Amazon EventBridge Scheduler, AWS Systems Manager Parameter Store, Amazon CloudWatch Logs, Terraform

---

## Roadmap / Further development

The current version of the project works both locally and in Docker. The next steps focus on infrastructure, running the project in AWS, and extending export options.

Planned next steps:

- [x] Add a `Dockerfile` to run the application in a container
- [x] Prepare an image with all required dependencies (`Python`, `Selenium`, `Chrome/Chromium`)
- [x] Add `.env.example` as a configuration template
- [x] Add `compose.yml` for convenient Docker Compose runs
- [x] Clean up configuration and input validation for more hands-off usage
- [x] Add basic smoke tests (imports, CLI)
- [x] Add tests for modules independent from Selenium
- [x] Extend input file validation and error messages
- [x] Add a simple CI workflow (GitHub Actions: test / image build)
- [x] Add automatic Docker Hub image publishing (GitHub Actions)
- [ ] Prepare infrastructure as code (Terraform)
- [ ] Verify running the project in AWS (for example as a scheduled job)