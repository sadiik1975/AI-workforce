from __future__ import annotations

import os
from pathlib import Path


ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def get_config() -> dict[str, str]:
    config = {
        "search_api_key": "",
        "email_api_key": "",
        "database_url": "sqlite:///data/tasks.db",
        "debug": False,
    }

    env_key_map = {
        "SEARCH_API_KEY": "search_api_key",
        "EMAIL_API_KEY": "email_api_key",
        "DATABASE_URL": "database_url",
        "DEBUG": "debug",
    }

    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            if not line or line.strip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            config_key = env_key_map.get(key, key)
            if config_key in {"search_api_key", "email_api_key", "database_url"}:
                config[config_key] = value
            elif config_key == "debug":
                config[config_key] = value.lower() == "true"

    environment_values = {
        "search_api_key": os.getenv("SEARCH_API_KEY"),
        "email_api_key": os.getenv("EMAIL_API_KEY"),
        "database_url": os.getenv("DATABASE_URL"),
        "debug": os.getenv("DEBUG"),
    }
    for key, value in environment_values.items():
        if value is None:
            continue
        config[key] = value.strip().lower() == "true" if key == "debug" else value.strip()

    return config


def require_config(keys: list[str]) -> None:
    config = get_config()
    missing = [key for key in keys if not config.get(key)]
    if missing:
        raise RuntimeError(f"Missing required configuration: {', '.join(missing)}")
