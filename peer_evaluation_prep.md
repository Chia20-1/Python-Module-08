# PM08 Peer Evaluation Prep

This file prepares you to explain the project during peer review.

The subject says you should demonstrate:

- Your understanding of virtual environments and why they are important.
- The differences between pip and Poetry for dependency management.
- How environment variables keep applications secure and configurable.
- Your ability to explain these concepts to other learners.

## 1. Short Opening Explanation

You can start peer evaluation with this:

```text
This project is about Python environment and configuration management.

Exercise 0 shows why virtual environments matter.
Exercise 1 shows how dependencies are installed with pip and Poetry.
Exercise 2 shows how configuration and secrets should come from environment variables instead of being hardcoded.
```

## 2. Virtual Environments

### Simple explanation

A virtual environment is an isolated Python workspace.

It lets one project have its own packages without affecting the global Python installation or other projects.

### Why virtual environments are important

Without a virtual environment:

- Packages are installed globally.
- Different projects can accidentally depend on different versions of the same package.
- Updating one package can break another project.
- It becomes harder to reproduce the project on another machine.

With a virtual environment:

- Dependencies stay inside the project environment.
- The project is safer to experiment with.
- Package versions are easier to control.
- Other learners can recreate the same setup.

### How ex0 demonstrates this

In `ex0/construct.py`, the program checks:

```python
sys.prefix
sys.base_prefix
```

If they are different, Python is running inside a virtual environment.

If they are the same, Python is running in the global environment.

### Peer explanation

Say this:

```text
I check whether sys.prefix is different from sys.base_prefix.
If they are different, it means Python is currently using a virtual environment.
That matters because packages installed there will not pollute the global Python setup.
```

## 3. pip And `requirements.txt`

### What pip is

`pip` is Python's package installer.

It installs packages into the currently active Python environment.

### What `requirements.txt` is

`requirements.txt` is a simple list of packages.

Example from ex1:

```text
numpy>=1.25.0
pandas>=2.1.0
matplotlib>=3.7.0
```

### How to install with pip

From inside `ex1/`:

```powershell
python -m pip install -r requirements.txt
```

### What this means

```text
Install every dependency listed in requirements.txt into the active environment.
```

### Peer explanation

Say this:

```text
pip reads requirements.txt and installs the listed packages into whichever Python environment is active. That is why I should activate a virtual environment before running pip install.
```

## 4. Poetry And `pyproject.toml`

### What Poetry is

Poetry is a dependency and project management tool.

It uses `pyproject.toml` to store project metadata and dependency information.

### What `pyproject.toml` is

`pyproject.toml` is a structured configuration file.

Example from ex1:

```toml
[tool.poetry.dependencies]
python = ">=3.10,<4.0"
numpy = "^1.25.0"
pandas = "^2.1.0"
matplotlib = "^3.7.0"
```

### How to install with Poetry

From inside `ex1/`:

```powershell
poetry install
```

Then run:

```powershell
poetry run python loading.py
```

### Peer explanation

Say this:

```text
Poetry reads pyproject.toml, resolves dependencies, and runs the project in its managed environment. It is more structured than requirements.txt because it stores both project metadata and dependencies.
```

## 5. pip vs Poetry

### Main difference

`pip` is mainly an installer.

Poetry is a project and dependency manager.

### Simple comparison

| Topic | pip | Poetry |
|---|---|---|
| Main file | `requirements.txt` | `pyproject.toml` |
| Purpose | Install packages | Manage project and dependencies |
| Environment | Uses active environment | Can create/manage its own environment |
| Metadata | Usually not included | Project name, version, authors, dependencies |
| Run command | `python loading.py` | `poetry run python loading.py` |

### Peer explanation

Say this:

```text
pip is simpler. It installs what requirements.txt lists.
Poetry is more complete. It manages dependencies, project metadata, and the environment more consistently.
```

## 6. Environment Variables

### Simple explanation

Environment variables are values stored outside the source code.

They are useful for configuration like:

- Mode
- Database URL
- API key
- Log level
- External endpoint

In ex2, the required variables are:

```text
MATRIX_MODE
DATABASE_URL
API_KEY
LOG_LEVEL
ZION_ENDPOINT
```

### Why environment variables are secure

Secrets should not be written directly in code.

Bad example:

```python
API_KEY = "real-secret-key"
```

Better:

```python
api_key = os.getenv("API_KEY")
```

This means the secret comes from the environment or `.env`, not from the source code.

### Peer explanation

Say this:

```text
Environment variables keep secrets out of the codebase. The code only knows the name API_KEY, but the real value comes from the environment or a local .env file.
```

## 7. `.env`, `.env.example`, And `.gitignore`

### `.env`

The `.env` file stores real local configuration.

Example:

```text
API_KEY=my-real-local-key
```

This file should not be committed.

### `.env.example`

The `.env.example` file is a safe template.

Example:

```text
API_KEY=replace_me_with_your_local_key
```

This file can be committed because it does not contain real secrets.

### `.gitignore`

`.gitignore` should include:

```text
.env
```

This prevents Git from tracking the real `.env` file.

### Peer explanation

Say this:

```text
.env.example documents the required variables with fake values.
.env contains real local values and should be ignored by Git.
That is why .env is listed in .gitignore.
```

## 8. How ex2 Loads Configuration

### Loading `.env`

`python-dotenv` provides:

```python
load_dotenv()
```

This loads values from `.env` into the environment.

### Reading values

Python reads the values with:

```python
os.getenv("API_KEY")
```

### Default values

Some values can safely have defaults:

```python
os.getenv("MATRIX_MODE", "development")
```

This is okay because `MATRIX_MODE` is not a secret.

### Missing values

Secrets and connection details should report missing:

```python
os.getenv("API_KEY")
os.getenv("DATABASE_URL")
os.getenv("ZION_ENDPOINT")
```

The program should not invent fake secrets or fake external connections.

### Peer explanation

Say this:

```text
I use defaults only for safe non-secret settings like MATRIX_MODE or LOG_LEVEL. For API_KEY, DATABASE_URL, and ZION_ENDPOINT, I report missing configuration because the program should not pretend those values exist.
```

## 9. Environment Variable Overrides

### What override means

An environment override means a real environment variable takes priority over `.env`.

For example, `.env` may say:

```text
MATRIX_MODE=development
```

But the shell can override it:

```powershell
$env:MATRIX_MODE = "production"
python oracle.py
```

The program should use `production`.

### Why this matters

Development can use `.env`.

Production can inject real environment variables without changing code.

### Peer explanation

Say this:

```text
load_dotenv() does not overwrite existing environment variables by default. So if MATRIX_MODE is already set in the real environment, that value wins over the .env value. This is useful for production overrides.
```

## 10. Exercise 1 Data Analysis Explanation

### What NumPy does

NumPy generates the fake Matrix data.

Example:

```python
rng = np.random.default_rng(seed=42)
latency_ms = rng.integers(low=10, high=200, size=1000)
```

### What pandas does

pandas stores and analyzes the data.

Example:

```python
df = pd.DataFrame(data)
average_latency = df["latency_ms"].mean()
```

### What matplotlib does

matplotlib creates the visualization and saves it.

Example:

```python
plt.savefig("matrix_analysis.png")
```

### Peer explanation

Say this:

```text
NumPy creates the dataset, pandas analyzes it as a table, and matplotlib saves the visualization. This satisfies the subject requirement that the dataset comes from NumPy and is analyzed with pandas.
```

## 11. Common Peer Questions

### Why not hardcode the API key?

Answer:

```text
Because secrets should not be stored in source code. If code is pushed to Git, the secret can leak. Environment variables keep the value outside the code.
```

### Why is `.env.example` committed but `.env` ignored?

Answer:

```text
.env.example is only a safe template. .env contains real local values, so it should be ignored by Git.
```

### Why does `MATRIX_MODE` have a default?

Answer:

```text
MATRIX_MODE is not a secret, and development is a safe fallback. But API_KEY and DATABASE_URL should not have fake defaults because the program should not pretend it has real credentials.
```

### What happens if dependencies are missing in ex1?

Answer:

```text
The program checks dependencies with importlib and prints installation instructions instead of crashing with a long traceback.
```

### What is the difference between `requirements.txt` and `pyproject.toml`?

Answer:

```text
requirements.txt is a simple package list for pip. pyproject.toml is a structured project configuration file used by Poetry to manage dependencies and project metadata.
```

### Why use a virtual environment before installing packages?

Answer:

```text
It keeps project dependencies isolated. Installing packages globally can affect other projects and make debugging harder.
```

## 12. Demo Flow For Peer Evaluation

### Demo ex0

Explain:

```text
This checks whether Python is running inside a virtual environment.
```

Run:

```powershell
python ex0/construct.py
```

### Demo ex1

Explain:

```text
This checks packages, generates data with NumPy, analyzes with pandas, and saves a visualization with matplotlib.
```

Run:

```powershell
cd ex1
python loading.py
```

### Demo ex2 without `.env`

Explain:

```text
This shows missing configuration warnings.
```

Run:

```powershell
cd ex2
python oracle.py
```

### Demo ex2 with `.env`

Explain:

```text
This loads local development configuration from .env.
```

Run:

```powershell
Copy-Item .env.example .env
python oracle.py
```

### Demo ex2 override

Explain:

```text
This shows that real environment variables override .env values.
```

Run:

```powershell
$env:MATRIX_MODE = "production"
$env:API_KEY = "secret123"
python oracle.py
```

Clean up:

```powershell
Remove-Item Env:\MATRIX_MODE
Remove-Item Env:\API_KEY
```

## 13. Final One-Minute Summary

Use this if your evaluator asks you to summarize the whole project:

```text
The project teaches how to manage Python execution environments and configuration.

Virtual environments isolate dependencies so one project does not break another.
pip installs packages from requirements.txt into the active environment.
Poetry uses pyproject.toml to manage project metadata, dependencies, and its environment.
Environment variables keep secrets and configuration outside source code.
.env is useful for local development, .env.example documents the expected variables, and .gitignore prevents real secrets from being committed.
```
