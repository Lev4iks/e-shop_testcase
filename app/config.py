import argparse

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    class Config:
        env_file = '.env.example'


ap = argparse.ArgumentParser()
ap.add_argument("--insert-start-data", required=False,
                help="Set True if it needed to insert start data",
                default=False)
kwargs = vars(ap.parse_args())
insert_start_data = kwargs.get('insert_start_data')

settings = Settings()
