import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    API_TOKEN = os.getenv("API_TOKEN", "your_secret_token") # for api auth
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///translation.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False