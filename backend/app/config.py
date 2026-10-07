from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR.parent / '.env'

if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv(BASE_DIR.parent / '.env.example')

APP_NAME = os.getenv('APP_NAME', 'AccessAI')
APP_ENV = os.getenv('APP_ENV', 'development')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', '8000'))
CORS_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',') if origin.strip()]
AI_PROVIDER = os.getenv('AI_PROVIDER', 'demo')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4o-mini')
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '10'))
