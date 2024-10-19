import json
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from pydantic_settings import (
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).parent.parent

load_dotenv(dotenv_path=BASE_DIR)

with open(
    BASE_DIR / "src/resources/json/gifts.json", "r", encoding="utf-8"
) as json_file:
    _gift_dict = json.load(json_file)

with open(
    BASE_DIR / "src/resources/json/price_list.json", "r", encoding="utf-8"
) as json_file:
    _price_list_dict = json.load(json_file)

with open(
    BASE_DIR / "src/resources/json/images.json", "r", encoding="utf-8"
) as json_file:
    _images_dict = json.load(json_file)


class APIConfig(BaseModel):
    url: str


class DatabaseConfig(BaseModel):
    name: str
    password: str
    user: str
    host: str
    port: str
    url: str | PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class CommandsConfig(BaseModel):
    courses: str = "Курсы"
    orders: str = "Мои Заказы"
    help: str = "Помощь"


class BotConfig(BaseModel):
    token: str
    payments_token: str
    account_id: str
    channel_id: str
    channel_username: str
    gift_dict: dict = _gift_dict
    price_list_dict: dict = _price_list_dict
    images_dict: dict = _images_dict
    commands: CommandsConfig = CommandsConfig()


class Logging(BaseSettings):
    format: str
    debug: bool


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("src/.env.template", "src/.env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DatabaseConfig
    bot: BotConfig
    api: APIConfig
    # logging: Logging


settings = Settings()
