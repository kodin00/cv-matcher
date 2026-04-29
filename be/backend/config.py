from dotenv import load_dotenv
import os

load_dotenv()

APP_TOKEN    = os.getenv("APP_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
MODEL_NAME   = os.getenv("MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
