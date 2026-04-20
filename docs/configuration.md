# Configuration

This document describes the basic project configuration:

- login credentials in the `.env` file,
- preparation of the input file `team.xlsx`,
- the expected input and output layout.

---

## `.env` file

The script reads login credentials from the `.env` file so secrets do not have to be stored in the code.

The `.env` file must be located in the **project root directory**, next to `main.py`:

```text
.
├─ main.py
├─ team.xlsx
└─ .env
```

### Example content

```env
ZP_USERNAME=your_login
ZP_PASSWORD=your_password
```

If the password contains spaces or unusual characters, use quotation marks:

```env
ZP_USERNAME="your_login"
ZP_PASSWORD="password with spaces"
```

---

## `.env.example`

The repository includes an example `.env.example` file that can be copied as a base for local configuration:

**Linux/Mac**
```bash
cp .env.example .env
```

**Windows (PowerShell)**
```powershell
Copy-Item .env.example .env
```

Then fill in the `ZP_USERNAME` and `ZP_PASSWORD` values.

---

## Security

- **Do not commit `.env` to the repository**
- Make sure `.env` is listed in `.gitignore`
- Do not store login credentials directly in the code or in run scripts

---

## Input file `team.xlsx`

The default input file is:

```text
team.xlsx
```

### File requirements

- the file must be in **`.xlsx`** format
- by default, the ZwiftPower profile ID should be in **column B**
- this matches the argument:

```text
--id-column-index 1
```

> Note: the column index is **0-based**, which means:
> - `0` = column A
> - `1` = column B
> - `2` = column C

If your file has the ID in a different column, use the `--id-column-index` argument.

### Example

```bash
python main.py --id-column-index 2
```

---

## Columns updated by the script

The script adds (if missing) and/or updates the following columns:

- `Weight`
- `zFTP`
- `Power_15sec`
- `Power_1min`
- `Power_5min`
- `Power_20min`

---

## Output file

The default output file is:

```text
updated_team.xlsx
```

You can set a different output file name with the `-o / --output` argument.

Example:

```bash
python main.py -o result.xlsx --headless
```

---

## Log file

By default, errors and exceptions are written to:

```text
errors.log
```

The log file name can be changed with the following argument:

```text
--log-file
```

Example:

```bash
python main.py --log-file updater.log --headless
```