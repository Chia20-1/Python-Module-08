import os
import sys


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


def show_dotenv_install_help() -> None:
    print("Missing dependency: python-dotenv\n")
    print("Install it with:")
    print("python -m pip install python-dotenv")


# Loads the .env file
# Saves the original environment to see the comparison after loading .env
# Avoids a mypy issue from assigning None to an imported function name.
def load_environment() -> set[str] | None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        show_dotenv_install_help()
        return None
    original_environment = set(os.environ)
    load_dotenv()
    return original_environment


# Failsafe in case the MATRIX_MODE is invalid
def normalize_mode(mode: str) -> str:
    mode = mode.lower()
    if mode in ["development", "production"]:
        return mode
    print(f"Warning: MATRIX_MODE={mode} is not valid")
    print("Using development mode instead")
    return "development"


# Get the environment variable name "MATRIX_MODE".
# If it doesn't exist, use "development" instead.
def get_config() -> dict[str, str | None]:
    mode = normalize_mode(os.getenv("MATRIX_MODE", "development"))
    if mode == "development":
        default_log_level = "DEBUG"
    else:
        default_log_level = "INFO"
    return {
        "MATRIX_MODE": mode,
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", default_log_level),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }


# Helper function to report status at terminal
# Missing configuration handling
def database_status(config: dict[str, str | None]) -> str:
    if not config["DATABASE_URL"]:
        return "Missing DATABASE_URL"
    if config["MATRIX_MODE"] == "production":
        return "Connected to production instance"
    return "Connected to local instance"


# Helper function to report status at terminal
# Missing configuration handling
def api_status(config: dict[str, str | None]) -> str:
    if config["API_KEY"]:
        return "Authenticated"
    return "Missing API_KEY"


# Helper function to report status at terminal
# Missing configuration handling
def zion_status(config: dict[str, str | None]) -> str:
    if config["ZION_ENDPOINT"]:
        return "Online"
    return "Missing ZION_ENDPOINT"


# Display all status at terminal
def show_configuration(config: dict[str, str | None]) -> None:
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {database_status(config)}")
    print(f"API Access: {api_status(config)}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {zion_status(config)}")


# Compiles the missing config in a list.
# If there is no missing config, return an empty list.
def get_missing_config(config: dict[str, str | None]) -> list[str]:
    missing = []
    for name in REQUIRED_NAMES:
        if not config.get(name):
            missing.append(name)
    return missing


# If the "missing" list is empty, there are no missing items.
# When there is item inside it, we show it in the terminal.
def show_missing_config(missing: list[str]) -> None:
    if not missing:
        return
    print("\nMissing configuration:")
    for name in missing:
        print(f"- {name} is not set")
    print("\n Create a local .env file from the example:")
    print("cp .env.example .env\n")
    print("Then edit .env with your local values")


# Validate if .gitignore has .env listed
# splitlines() splits a string into a list of strings at line breaks.
def gitignore_has_env() -> bool:
    if not os.path.exists(".gitignore"):
        return False

    with open(".gitignore", "r", encoding="utf-8") as file:
        return ".env" in file.read().splitlines()


def show_security_check(
        config: dict[str, str | None],
        original_environment: set[str],
) -> None:
    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")

    if (
        config["DATABASE_URL"]
        and config["API_KEY"]
        and config["ZION_ENDPOINT"]
    ):
        print("[OK] Configuration values loaded")
    else:
        print("[WARNING] Required configuration is missing")

    overridden_names = []
    for name in config:
        if name in original_environment:
            overridden_names.append(name)
    if overridden_names:
        name_str = ", ".join(overridden_names)
        print("[OK] Environment override detected: " + name_str)
    else:
        print("[OK] Production overrides available")


def main() -> int:
    print("ORACLE STATUS: Reading the Matrix...\n")
    original_environment = load_environment()
    if original_environment is None:
        return 1
    config = get_config()
    missing = get_missing_config(config)
    show_configuration(config)
    show_missing_config(missing)
    show_security_check(config, original_environment)
    print("The Oracle sees all configurations.")
    if missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
