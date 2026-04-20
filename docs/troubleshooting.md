# Common problems

This document collects the most common problems related to running the project locally and with Docker.

---

## 1. Missing login credentials in `.env`

Check:

- whether the file is named exactly **`.env`**
- whether it is located in the project root directory, next to `main.py`
- whether it contains:
  - `ZP_USERNAME`
  - `ZP_PASSWORD`

Example of a valid file:

```env
ZP_USERNAME=your_login
ZP_PASSWORD=your_password
```

---

## 2. Windows: problem creating `.env`

Windows sometimes makes it harder to create files that start with a dot.  
Create the file from the terminal:

```powershell
New-Item -Name ".env" -ItemType "file"
```

Then open it and paste your login credentials.

---

## 3. Input file not found

If you get an error saying the input file is missing:

- check whether the file exists,
- check whether the path you passed is correct,
- make sure you are running the script from the correct directory.

Example:

```bash
python main.py -i team.xlsx --headless
```

---

## 4. Only `.xlsx` files are supported

The project supports Excel files only in this format:

```text
.xlsx
```

If you pass a `.txt`, `.csv`, `.xls`, or any other file type, the script will raise a validation error.

---

## 5. Selenium / Chrome does not start

If the browser does not start correctly:

- update Google Chrome,
- update Selenium:

```bash
pip install -U selenium
```

- run the project without `--headless` so it is easier to see what is happening:

```bash
python main.py
```

---

## 6. Missing power data from the chart

ZwiftPower uses charts rendered in JavaScript (Highcharts).  
If the page structure changes or the selectors no longer match, some data may not be collected.

In that case:

- check `errors.log`,
- check whether the ZwiftPower profile still has the expected structure,
- check whether the selectors used in the scraper still match the page.

---

## 7. The Docker container stops immediately

This is normal.

When run with Docker, the project works as a **one-time job**, not as a long-running background service.  
Once the processing is finished, the container simply exits.

---

## 8. Changes in `Dockerfile` or `requirements.txt` do not show up

Run the project again with a rebuilt image:

```bash
docker compose run --rm --build zp-updater
```

If you still see the old behavior, you can also remove the local image and build it again.

---

## 9. The script is unstable with many profiles

If you see random errors or scraping becomes unstable:

- increase the timeout:

```bash
python main.py --headless --timeout 30
```

- add a longer delay between profiles:

```bash
python main.py --headless --sleep 1.0
```

This can help if the page loads more slowly or needs more time to render the data.

---

## 10. Tests do not pass

Check:

- whether you installed the dependencies from `requirements.txt`,
- whether you are running the tests from the project root directory,
- whether your virtual environment is active.

Run all tests:

```bash
pytest
```

Run a single test:

```bash
pytest tests/test_config.py
```

---

## 11. Where to look for more information

If the problem is related to:

- configuration → see `docs/configuration.md`
- running the project → see `docs/usage.md`
- AWS architecture → see `docs/architecture/lambda-v1.md`