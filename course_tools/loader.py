"""Loads the code a module's tests should check.

By default the tests check YOUR file: modules/<module>/exercises.py.
The reference answers in solutions/ are only loaded when the
environment variable PYCOURSE_SOLUTIONS=1 is set (used to verify the course itself).
"""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(test_file: str):
    folder = Path(test_file).resolve().parent
    if os.environ.get("PYCOURSE_SOLUTIONS") == "1":
        path = ROOT / "solutions" / f"{folder.name}.py"
        name = f"solutions_{folder.name}"
    else:
        path = folder / "exercises.py"
        name = f"exercises_{folder.name}"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses need the module registered
    spec.loader.exec_module(module)
    return module
