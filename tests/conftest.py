import os
from pathlib import Path

from dotenv import load_dotenv

env = os.environ.get("ENV", "local")
load_dotenv(Path(__file__).parent / f".env.{env}")
