"""
Top-level package global definitions
"""
import os
import yaml
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


BASE_PATH = Path(os.path.dirname(__file__))
CONFIG_PATH = BASE_PATH / "config"
DATA_PATH = BASE_PATH / "data"

load_dotenv()

from pathlib import Path


@dataclass(frozen=True)
class OpenAISettings:
    openai_key: str = os.getenv("OPENAI_KEY", "")

def general_settings():
    with open(CONFIG_PATH / "config.yaml") as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)

    return settings
