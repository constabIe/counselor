import os
from pathlib import Path

from src.config_schema import Settings

# settings_path = os.getenv("SETTINGS_PATH", "settings.yaml")
# settings: Settings = Settings.from_yaml(Path(settings_path)) if Path(settings_path).exists() else Settings() # type: ignore


settings_path = os.getenv("SETTINGS_PATH", ".env")
settings: Settings = Settings.from_env(Path(settings_path)) if Path(settings_path).exists() else Settings() # type: ignore
print(settings.db_url.get_secret_value())
print(settings.jwt_secret_key.get_secret_value())

