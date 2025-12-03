"""
Compatibility shim so the rest of the project can keep importing ``generated_app``.

Depending on the most recent agent run, the generated implementation might live
under ``generated_code.generated_app`` (the intended location) or
``generated_tests.generated_app`` (occasionally produced by the generator).
This shim tries each known location and re-exports the important symbols so
``python -m generated_tests.test_generated_app`` can always import the module
it expects without manual file juggling.
"""

from importlib import import_module
from types import ModuleType
from typing import Optional

_CANDIDATE_MODULES = (
    "generated_code.generated_app",
    "generated_tests.generated_app",
)


def _load_impl() -> ModuleType:
    for module_name in _CANDIDATE_MODULES:
        try:
            return import_module(module_name)
        except ModuleNotFoundError:
            continue
    raise ModuleNotFoundError(
        "No generated app implementation found. "
        f"Tried: {', '.join(_CANDIDATE_MODULES)}. "
        "Run the workflow to generate code, or ensure the files exist."
    )


_impl = _load_impl()


def _require(attr_name: str):
    if not hasattr(_impl, attr_name):
        raise ImportError(
            f"Module '{_impl.__name__}' is missing required attribute '{attr_name}'. "
            "Regenerate the code so the expected API exists."
        )
    return getattr(_impl, attr_name)


def _maybe(attr_name: str):
    return getattr(_impl, attr_name, None)


CyberDefenderApp = _require("CyberDefenderApp")
CyberDefender = _maybe("CyberDefender")
PasswordManager = _maybe("PasswordManager")
Threat = _maybe("Threat")
main = _maybe("main") or _maybe("run")


__all__ = [
    name
    for name in (
        "CyberDefenderApp",
        "CyberDefender",
        "PasswordManager",
        "Threat",
        "main",
    )
    if globals().get(name) is not None
]

