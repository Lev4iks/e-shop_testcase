import asyncio
import typer
from loguru import logger

from app.database import init_models

cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    logger.info("Initialized database models")
