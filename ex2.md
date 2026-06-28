# PM08 - Exercise 2 Guide

This guide is for `ex2`, the "Accessing the Mainframe" exercise. The main lesson is how Python programs read configuration safely from environment variables and `.env` files.

You are learning:

- How to keep secrets out of source code.
- How to use `.env.example` as a template.
- How to ignore the real `.env` file with `.gitignore`.
- How development and production configuration can be different.
- How `python-dotenv` loads `.env` values into your program.

## Segment 1: Understand The Subject Requirement

### What the exercise is asking for

The subject wants you to create a secure configuration program named:

```text
ex2/oracle.py
```

The program should read settings such as mode, database URL, API key, log level, and endpoint from environment variables.

The goal is not to hardcode secrets. The goal is to show that your program can load configuration safely from the outside.

### Files you must submit

Inside `ex2/`, the subject asks for these files:

```text
oracle.py
.env.example
.gitignore
```

The real `.env` file should not be submitted.

### Authorized modules

The authorized modules are:

```text
os
sys
python-dotenv modules
file operations
```

Important naming detail:

- The package you install is called `python-dotenv`.
- The module you import in Python is usually called `dotenv`.

Example:

```python
from dotenv import load_dotenv
```

### Required behavior

Your program must:

- Load configuration from environment variables.
- Use a `.env` file for development settings.
- Demonstrate different configuration for development and production.
- Handle missing configuration properly.
- Use `python-dotenv` to load `.env` files.
- Show clear output so the evaluator can see what configuration was loaded.
- Make sure real secrets are not committed.
- Put `.env` in `.gitignore`.

### Configuration variables you must handle

The subject lists these variables:

```text
MATRIX_MODE
DATABASE_URL
API_KEY
LOG_LEVEL
ZION_ENDPOINT
```

Suggested meaning:

- `MATRIX_MODE`: controls whether the program runs in `development` or `production`.
- `DATABASE_URL`: connection string for storage.
- `API_KEY`: secret key for external services.
- `LOG_LEVEL`: amount of logging detail, such as `DEBUG` or `INFO`.
- `ZION_ENDPOINT`: URL for the resistance network.

### What `.env.example` is for

`.env.example` is a safe template file. It shows which variables the program expects, but it must not contain real secrets.

Example:

```text
MATRIX_MODE=development
DATABASE_URL=sqlite:///matrix_dev.db
API_KEY=replace_me_with_your_local_key
LOG_LEVEL=DEBUG
ZION_ENDPOINT=http://localhost:4242/zion
```

This file can be committed because it only contains fake or example values.

### What `.env` is for

`.env` is the real local configuration file.

You create it from the example:

```powershell
Copy-Item .env.example .env
```

Or on Unix-style shells:

```bash
cp .env.example .env
```

Then you edit `.env` with your own local values.

The real `.env` file should stay private because it may contain secrets.

### What `.gitignore` is for

`.gitignore` tells Git which files should not be tracked.

For this exercise, it must include:

```text
.env
```

Good extra entries:

```text
__pycache__/
*.pyc
.venv/
```

The key requirement is that `.env` must be ignored.

### Environment variable priority

The subject expects this behavior:

```text
Environment variables should override values from .env.
```

This is useful because:

- `.env` can store development defaults.
- Production can inject safer real values from the system environment.
- You do not need to edit code when moving between environments.

With `python-dotenv`, this priority is easy:

```python
load_dotenv()
```

By default, `load_dotenv()` does not overwrite variables that already exist in the environment. So if `MATRIX_MODE` already exists before the program runs, that value wins over the `.env` value.

### What "missing configuration warnings" means

When configuration is missing, the program should not fail with a confusing error.

Instead, print something helpful:

```text
Missing configuration:
- API_KEY is not set
- DATABASE_URL is not set

Create a .env file from .env.example:
cp .env.example .env
```

You can decide whether the program should stop after missing required values. For secrets like `API_KEY`, stopping cleanly is usually better than pretending everything is fine.

### What development vs production should show

The subject says the difference must be visible in the output.

For example:

```text
Mode: development
Database: Connected to local instance
Log Level: DEBUG
```

And for production:

```text
Mode: production
Database: Connected to production instance
Log Level: INFO
```

The program does not need to really connect to a database. It can simulate the connection message based on the configuration.

## Segment 2: Learn How To Do This Exercise

### Recommended file structure

By the end, `ex2/` should look like this:

```text
ex2/
  oracle.py
  .env.example
  .gitignore
```

During local testing, you may also have:

```text
ex2/
  .env
```

But `.env` should not be submitted.

### Step 1: Create the folder and files

From the project root:

```powershell
New-Item -ItemType Directory -Force ex2
New-Item -ItemType File ex2\oracle.py
New-Item -ItemType File ex2\.env.example
New-Item -ItemType File ex2\.gitignore
```

You can also create them manually in your editor.

### Step 2: Fill `.env.example`

Use safe example values only:

```text
MATRIX_MODE=development
DATABASE_URL=sqlite:///matrix_dev.db
API_KEY=replace_me_with_your_local_key
LOG_LEVEL=DEBUG
ZION_ENDPOINT=http://localhost:4242/zion
```

Do not put real passwords, real API keys, or private URLs here.

### Step 3: Fill `.gitignore`

At minimum:

```text
.env
```

Recommended:

```text
.env
__pycache__/
*.pyc
.venv/
```

This proves you understand why `.env.example` is public but `.env` is private.

### Step 4: Install python-dotenv if needed

If your environment does not already have `python-dotenv`, install it:

```powershell
python -m pip install python-dotenv
```

Remember:

```python
from dotenv import load_dotenv
```

You install `python-dotenv`, but you import `dotenv`.

### Step 5: Plan `oracle.py`

A clean structure is:

```text
main()
  load .env file
  read configuration values
  validate missing values
  display loaded configuration
  display development or production behavior
  run environment security checks
```

Suggested functions:

- `load_environment()` calls `load_dotenv()`.
- `get_config()` reads values with `os.getenv()`.
- `validate_config()` checks missing or invalid values.
- `describe_database()` changes output based on `MATRIX_MODE`.
- `security_check()` checks whether `.env` is ignored and `.env.example` exists.
- `main()` controls the program flow.

### Step 6: Load the `.env` file

Basic idea:

```python
from dotenv import load_dotenv

load_dotenv()
```

This reads `.env` if it exists.

If `.env` does not exist, the program can still read real environment variables from the system.

### Step 7: Read environment variables

Use `os.getenv()`:

```python
mode = os.getenv("MATRIX_MODE", "development")
database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
log_level = os.getenv("LOG_LEVEL", "INFO")
zion_endpoint = os.getenv("ZION_ENDPOINT")
```

Good rule:

- Defaults are okay for non-secret values like `MATRIX_MODE` and `LOG_LEVEL`.
- Secrets like `API_KEY` should not have real defaults.

### Step 8: Validate the configuration

Check for missing required values:

```python
missing = []

if not database_url:
    missing.append("DATABASE_URL")
if not api_key:
    missing.append("API_KEY")
if not zion_endpoint:
    missing.append("ZION_ENDPOINT")
```

Then print a helpful warning:

```python
if missing:
    print("Missing configuration:")
    for name in missing:
        print(f"- {name} is not set")
    print("Create .env from .env.example and fill in the values.")
```

You can stop cleanly with:

```python
return 1
```

And in the entry point:

```python
sys.exit(main())
```

### Step 9: Make development and production visible

Use `MATRIX_MODE` to change the output.

Example logic:

```python
if mode == "production":
    database_status = "Connected to production instance"
    default_log_level = "INFO"
else:
    database_status = "Connected to local instance"
    default_log_level = "DEBUG"
```

This satisfies the subject requirement that development and production differences must be visible.

### Step 10: Show environment variable overrides

If `.env` contains:

```text
MATRIX_MODE=development
API_KEY=local_key
```

You can override it from PowerShell:

```powershell
$env:MATRIX_MODE = "production"
$env:API_KEY = "secret123"
python oracle.py
```

The program should show:

```text
Mode: production
API Access: Authenticated
```

On Unix-style shells, the subject shows this style:

```bash
MATRIX_MODE=production API_KEY=secret123 python3 oracle.py
```

### Step 11: Print output similar to the subject

Your output should be close to:

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
[OK] .env file properly configured
[OK] Production overrides available

The Oracle sees all configurations.
```

The exact words can be different, but the required behavior should be clear.

### Step 12: Test without `.env`

From inside `ex2/`:

```powershell
python oracle.py
```

Expected result:

- The program should not crash.
- It should warn about missing configuration.
- It should tell you to create `.env` from `.env.example`.

### Step 13: Test with `.env`

From inside `ex2/`:

```powershell
Copy-Item .env.example .env
python oracle.py
```

Expected result:

- The program loads values from `.env`.
- It shows development mode.
- It shows local database behavior.
- It shows the security checks.

### Step 14: Test production override

In PowerShell:

```powershell
$env:MATRIX_MODE = "production"
$env:API_KEY = "secret123"
python oracle.py
```

Expected result:

- The program uses `production` even if `.env` says `development`.
- The program uses the environment `API_KEY`.
- The output clearly shows production behavior.

After testing, you can clear the variables:

```powershell
Remove-Item Env:\MATRIX_MODE
Remove-Item Env:\API_KEY
```

### Final checklist

Before submitting, confirm:

- `ex2/oracle.py` exists.
- `ex2/.env.example` exists.
- `ex2/.gitignore` exists.
- `.gitignore` contains `.env`.
- `.env.example` contains only fake example values.
- The real `.env` file is not committed.
- `oracle.py` uses `python-dotenv`.
- `oracle.py` reads configuration with environment variables.
- Missing configuration shows helpful warnings.
- Development and production output are visibly different.
- Environment variables override `.env` values.
- The program output includes a security check.
