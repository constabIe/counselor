from enum import StrEnum
from pathlib import Path
from typing import Optional
from dotenv import dotenv_values

# try:
#     import yaml
# except ImportError:
#     yaml = None

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class SettingBaseModel(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True, extra="ignore")


class Settings(SettingBaseModel):
    """Настройки приложения"""
    
    schema_: Optional[str] = Field(None, alias="$schema")

    app_root_path: str = ""
    
    # Database settings
    db_url: SecretStr = Field(
        default=SecretStr("postgresql+asyncpg://postgres:postgres@localhost:5432/t1"),
        description="Database URL",
        examples=[
            "postgresql+asyncpg://postgres:postgres@localhost:5432/t1",
            "sqlite+aiosqlite:///./counselor.db",
        ]
    )
    
    # JWT settings
    jwt_secret_key: SecretStr = Field(
        default=SecretStr("your-secret-key-change-this-in-production"),
        description="Secret key for JWT token generation"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_hours: int = Field(default=24, description="JWT token expiration in hours")
    
    # CORS settings
    cors_allow_origin_regex: str = ".*"
    
    # Environment
    environment: Environment = Environment.DEVELOPMENT
    
    # LLM API settings
    llm_api_url: str = Field(
        default="https://llm.t1v.scibox.tech/completions",
        description="LLM API URL"
    )
    llm_api_token: SecretStr = Field(
        default=SecretStr("sk-oWtKHDq9UET7fCG0JaJDWQ"),
        description="LLM API token"
    )
    llm_model: str = Field(
        default="Qwen2.5-72B-Instruct-AWQ",
        description="LLM model name"
    )

    # @classmethod
    # def from_yaml(cls, path: Path) -> "Settings":
    #     if yaml is None:
    #         raise ImportError("PyYAML is required for YAML configuration")
    #     with open(path) as f:
    #         yaml_config = yaml.safe_load(f)
    #     return cls.model_validate(yaml_config)

    # @classmethod
    # def save_schema(cls, path: Path) -> None:
    #     if yaml is None:
    #         raise ImportError("PyYAML is required for YAML configuration")
    #     with open(path, "w") as f:
    #         schema = {"$schema": "https://json-schema.org/draft-07/schema", **cls.model_json_schema()}
    #         yaml.dump(schema, f, sort_keys=False)
            
    @classmethod
    def from_env(cls, path: Path) -> "Settings":
        """Загрузка конфигурации из .env файла"""
        if not path.exists():
            raise FileNotFoundError(f".env файл не найден: {path}")
        env_config = dotenv_values(path)
        return cls.model_validate(env_config)

    @classmethod
    def save_schema(cls, path: Path) -> None:
        """Сохранение JSON-схемы настроек (для документации)"""
        schema = {"$schema": "https://json-schema.org/draft-07/schema", **cls.model_json_schema()}
        with open(path, "w", encoding="utf-8") as f:
            import json
            json.dump(schema, f, ensure_ascii=False, indent=2)
