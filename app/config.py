# app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega o arquivo .env da raiz do projeto
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=ROOT / ".env")

MONGO_URL = os.getenv("MONGO_URL", "")
MONGO_DB = os.getenv("MONGO_DB", "chatdb_refatorado")

if not MONGO_URL:
    raise RuntimeError("A variável MONGO_URL não foi definida no arquivo .env.")