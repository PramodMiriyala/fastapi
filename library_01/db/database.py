"""This module will have database connection and nessasary methods"""
import os
from dotenv import load_dotenv

# loads values from .env file, skips if env variable is explicitly set
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
