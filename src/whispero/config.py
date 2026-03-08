from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

DEFAULTS = {
    "backend": "local",
    "server": "http://localhost:8080",
    "model": "large-v3",
    "hotkey": {"windows": ["win", "ctrl"], "mac": ["cmd", "ctrl"]},
    "sounds": True,
}

VALID_BACKENDS = {"local", "server"}
VALID_MODELS = {"large-v3", "medium", "small", "base", "tiny"}

CONFIG_DIR = Path.home() / ".whispero"
CONFIG_PATH = CONFIG_DIR / "config.json"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _load_config_file() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _normalize(config: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(config)

    backend = str(normalized.get("backend", DEFAULTS["backend"])).lower()
    normalized["backend"] = backend if backend in VALID_BACKENDS else DEFAULTS["backend"]

    model = str(normalized.get("model", DEFAULTS["model"])).lower()
    normalized["model"] = model if model in VALID_MODELS else DEFAULTS["model"]

    normalized["server"] = str(normalized.get("server", DEFAULTS["server"]))
    return normalized


def _apply_env(config: dict[str, Any]) -> dict[str, Any]:
    updated = deepcopy(config)

    env_backend = os.environ.get("WHISPERO_BACKEND")
    if env_backend:
        backend = env_backend.strip().lower()
        if backend in VALID_BACKENDS:
            updated["backend"] = backend

    env_server = os.environ.get("WHISPERO_SERVER")
    if env_server:
        updated["server"] = env_server

    env_model = os.environ.get("WHISPERO_MODEL")
    if env_model:
        model = env_model.strip().lower()
        if model in VALID_MODELS:
            updated["model"] = model

    return updated


def save_config_value(key: str, value: Any) -> None:
    """Update a single key in the user config file, preserving other settings."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    file_config = _load_config_file()
    file_config[key] = value
    CONFIG_PATH.write_text(json.dumps(file_config, indent=2) + "\n", encoding="utf-8")


def load_config() -> dict[str, Any]:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    file_config = _load_config_file()
    merged = _deep_merge(DEFAULTS, file_config)
    env_applied = _apply_env(merged)
    return _normalize(env_applied)
