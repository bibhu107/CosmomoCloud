from pydantic import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "mydatabase"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
