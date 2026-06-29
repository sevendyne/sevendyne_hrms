"""Backward-compatible settings shim — use config.settings.local or config.settings.production."""
from config.settings.local import *  # noqa: F403, F401
