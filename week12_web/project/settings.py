"""settings.py - the project's configuration, read from environment variables (the kit's .env file)."""

import os
from pathlib import Path

from dotenv import load_dotenv

KIT = Path(__file__).resolve().parent.parent
load_dotenv(KIT / ".env")              # variables that are already set win (override=False)


def load_settings():
    """{"name": ..., "admin_token": ...}. The token protects the admin route; it is never printed."""
    return {"name": os.environ.get("APP_NAME", "Flashcard Maker"),
            "admin_token": os.environ.get("ADMIN_TOKEN", "")}
