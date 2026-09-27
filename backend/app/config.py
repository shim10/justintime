import os

# Local/dev default is SQLite; cloud deployment sets DATABASE_URL to the managed PostgreSQL instance.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./justintime.db")
