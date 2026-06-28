import sys
import os
import site


"""
If sys.base_prefix is different from sys.prefix, it shows that the script
is running inside a virtual environment.

If the old-version "real_prefix" exists, it means I uses the venv
to run the older version of Python.

hasattr() function returns True if the object has the attribute.

Vocabluary:
sys.executable   -> the Python binary currently running
sys.prefix       -> the active environment root
sys.base_prefix  -> the original/base Python install
site-packages    -> package install location derived from the active environment
os.path.basename -> to extract the final part of a file path
"""
def display_outside_venv() -> None:
    print("\nMATRIX STATUS: You're still plugged in.\n")
    print("Current Python:", sys.executable)
    print("Virtual Environment: None detected\n")
    print("Warning: You're in global environment!")
    print("The machines can see everything you install.\n")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Window")
    print("\nThen run this program again.")


def display_inside_venv() -> None:
    print("\nMATRIX STATUS: Welcome to the construct\n")
    print("Current Python:", sys.executable)
    print("Virtual Environment:", os.path.basename(sys.prefix))
    print("Environment Path:", sys.prefix)
    print("\nSUCCESS: You're in an isolated environemnt!")
    print("Safe to install packages without affecting the global system.\n")
    print("Package installation path:", site.getsitepackages())


def construct() -> None:
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix')
    and sys.base_prefix != sys.prefix):
        display_inside_venv()
    else:
        display_outside_venv()


if __name__ == "__main__":
    construct()
