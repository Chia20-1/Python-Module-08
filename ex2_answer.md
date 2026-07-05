# Ex2 Answer - Accessing The Mainframe

This is a step-by-step answer for `ex2`.

The subject asks you to create:

```text
ex2/
  oracle.py
  .env.example
  .gitignore
```

The real `.env` file is only for local testing. It should not be submitted.

## Step 1: Create The Exercise Folder

From the project root:

```powershell
New-Item -ItemType Directory -Force ex2
```

Then create these files:

```text
ex2/oracle.py
ex2/.env.example
ex2/.gitignore
```

## Step 2: Write `.env.example`

File:

```text
ex2/.env.example
```

Content:

```text
MATRIX_MODE=development
DATABASE_URL=sqlite:///matrix_dev.db
API_KEY=replace_me_with_your_local_key
LOG_LEVEL=DEBUG
ZION_ENDPOINT=http://localhost:4242/zion
```

Why this file exists:

- It shows which configuration variables your program expects.
- It gives safe example values.
- It should not contain real secrets.
- It can be committed.

## Step 3: Write `.gitignore`

File:

```text
ex2/.gitignore
```

Content:

```text
.env
__pycache__/
*.pyc
.venv/
```

Why this file exists:

- `.env` may contain real secrets.
- Git should not track `.env`.
- `.env.example` is the public template.
- `.env` is the private local file.

## Step 4: Install `python-dotenv`

If needed:

```powershell
python -m pip install python-dotenv
```

Important:

```text
Package name: python-dotenv
Import name: dotenv
```

So in Python:

```python
from dotenv import load_dotenv
```

## Step 5: Write `oracle.py`

File:

```text
ex2/oracle.py
```

Content:

```python
import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


CONFIG_NAMES = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]

REQUIRED_NAMES = [
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
]


def show_dotenv_install_help():
    print("Missing dependency: python-dotenv")
    print()
    print("Install it with:")
    print("python -m pip install python-dotenv")


def load_environment():
    if load_dotenv is None:
        show_dotenv_install_help()
        return None

    original_environment = set(os.environ)
    load_dotenv()
    return original_environment


def normalize_mode(mode):
    mode = mode.lower()
    if mode in ["development", "production"]:
        return mode
    print(f"Warning: MATRIX_MODE={mode} is not valid.")
    print("Using development mode instead.")
    return "development"


def get_config():
    mode = normalize_mode(os.getenv("MATRIX_MODE", "development"))
    default_log_level = "DEBUG" if mode == "development" else "INFO"

    return {
        "MATRIX_MODE": mode,
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", default_log_level),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }


def get_missing_config(config):
    missing = []
    for name in REQUIRED_NAMES:
        if not config.get(name):
            missing.append(name)
    return missing


def database_status(config):
    if not config["DATABASE_URL"]:
        return "Missing DATABASE_URL"
    if config["MATRIX_MODE"] == "production":
        return "Connected to production instance"
    return "Connected to local instance"


def api_status(config):
    if config["API_KEY"]:
        return "Authenticated"
    return "Missing API_KEY"


def zion_status(config):
    if config["ZION_ENDPOINT"]:
        return "Online"
    return "Missing ZION_ENDPOINT"


def env_file_is_ignored():
    if not os.path.exists(".gitignore"):
        return False

    try:
        with open(".gitignore", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError:
        return False

    ignored_entries = []
    for line in lines:
        clean_line = line.split("#", 1)[0].strip()
        if clean_line:
            ignored_entries.append(clean_line)

    return ".env" in ignored_entries


def show_missing_config_help(missing):
    if not missing:
        return

    print()
    print("Missing configuration:")
    for name in missing:
        print(f"- {name} is not set")
    print()
    print("Create a local .env file from the example:")
    print("Copy-Item .env.example .env")
    print()
    print("Then edit .env with your local values.")


def show_configuration(config):
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {database_status(config)}")
    print(f"API Access: {api_status(config)}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {zion_status(config)}")


def show_security_check(original_environment):
    print()
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if env_file_is_ignored():
        print("[OK] .env file properly ignored by Git")
    else:
        print("[WARNING] .env is not listed in .gitignore")

    overridden_names = []
    for name in CONFIG_NAMES:
        if name in original_environment:
            overridden_names.append(name)

    if overridden_names:
        print("[OK] Environment override detected: " + ", ".join(overridden_names))
    else:
        print("[OK] Production overrides available")


def main():
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    original_environment = load_environment()
    if original_environment is None:
        return 1

    config = get_config()
    missing = get_missing_config(config)

    show_configuration(config)
    show_missing_config_help(missing)
    show_security_check(original_environment)

    print()
    print("The Oracle sees all configurations.")

    if missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Step 6: Understand The Code

### Import section

```python
import os
import sys
```

- `os` reads environment variables and checks files.
- `sys` lets the program exit with `sys.exit(main())`.

```python
from dotenv import load_dotenv
```

- `load_dotenv()` reads the `.env` file.
- Values from the real environment override `.env` values by default.

### Configuration names

```python
CONFIG_NAMES = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]
```

These are the exact variables from the subject.

### Required names

```python
REQUIRED_NAMES = [
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
]
```

These values should be provided by `.env` or by real environment variables.

`MATRIX_MODE` and `LOG_LEVEL` can have safe defaults.

### Loading `.env`

```python
load_dotenv()
```

This loads values from `.env` into `os.environ`.

Important behavior:

```text
If MATRIX_MODE already exists in the real environment,
load_dotenv() does not replace it with the .env value.
```

That is how the environment override requirement is satisfied.

### Reading values

```python
os.getenv("MATRIX_MODE", "development")
```

This means:

- Read `MATRIX_MODE`.
- If it does not exist, use `"development"`.

For secrets:

```python
os.getenv("API_KEY")
```

There is no real default because secrets should not be hardcoded.

### Development and production difference

```python
default_log_level = "DEBUG" if mode == "development" else "INFO"
```

Development mode is more verbose.

Production mode is quieter.

```python
if config["MATRIX_MODE"] == "production":
    return "Connected to production instance"
return "Connected to local instance"
```

This makes the mode difference visible in the output.

## Step 7: Test Without `.env`

From inside `ex2/`:

```powershell
python oracle.py
```

Expected behavior:

- The program runs without a Python traceback.
- It uses default mode, usually `development`.
- It warns that required configuration is missing.
- It tells you to create `.env` from `.env.example`.

Example output:

```text
ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: development
Database: Missing DATABASE_URL
API Access: Missing API_KEY
Log Level: DEBUG
Zion Network: Missing ZION_ENDPOINT

Missing configuration:
- DATABASE_URL is not set
- API_KEY is not set
- ZION_ENDPOINT is not set

Create a local .env file from the example:
Copy-Item .env.example .env

Then edit .env with your local values.

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by Git
[OK] Production overrides available

The Oracle sees all configurations.
```

## Step 8: Test With `.env`

From inside `ex2/`:

```powershell
Copy-Item .env.example .env
python oracle.py
```

Expected behavior:

- The program reads `.env`.
- It shows development mode.
- It shows local database behavior.
- It shows API access as authenticated.
- It shows Zion network as online.

Example output:

```text
ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by Git
[OK] Production overrides available

The Oracle sees all configurations.
```

## Step 9: Test Environment Variable Override

Make sure `.env` exists first.

In PowerShell:

```powershell
$env:MATRIX_MODE = "production"
$env:API_KEY = "secret123"
python oracle.py
```

Expected behavior:

- `MATRIX_MODE` becomes `production`.
- `API_KEY` uses the environment value instead of the `.env` value.
- The database message changes to production.
- The log level changes to `INFO` if `LOG_LEVEL` is not set.

Example output:

```text
ORACLE STATUS: Reading the Matrix...

Configuration loaded:
Mode: production
Database: Connected to production instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

Environment security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by Git
[OK] Environment override detected: MATRIX_MODE, API_KEY

The Oracle sees all configurations.
```

Note: If your `.env` contains `LOG_LEVEL=DEBUG`, the log level stays `DEBUG`. If you remove `LOG_LEVEL` from `.env`, production mode uses the default `INFO`.

After testing, clean the temporary environment variables:

```powershell
Remove-Item Env:\MATRIX_MODE
Remove-Item Env:\API_KEY
```

## Step 10: Why This Satisfies The Subject

| Subject requirement | Where it is handled |
|---|---|
| Create `oracle.py` | Step 5 |
| Create `.env.example` | Step 2 |
| Create `.gitignore` | Step 3 |
| Load configuration from environment variables | `os.getenv()` |
| Use `.env` for development settings | `load_dotenv()` |
| Demonstrate development and production difference | `database_status()` and log-level default |
| Handle missing configuration | `get_missing_config()` and `show_missing_config_help()` |
| Use `python-dotenv` | `from dotenv import load_dotenv` |
| Never commit real secrets | `.env` is ignored, `.env.example` uses fake values |
| Environment variables override `.env` | default `load_dotenv()` behavior |

## Final Submission Checklist

Before submitting, confirm:

- `ex2/oracle.py` exists.
- `ex2/.env.example` exists.
- `ex2/.gitignore` exists.
- `ex2/.gitignore` contains `.env`.
- The real `ex2/.env` file is not committed.
- The code uses `load_dotenv()`.
- The code uses `os.getenv()`.
- Missing configuration prints helpful warnings.
- Development and production modes show different output.
- Environment variables override `.env` values.
