import asyncio
from functools import wraps
from typing import Annotated

import typer
import uvicorn
from src.core.logging import LOGGING

cli = typer.Typer()


def typer_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@cli.command()
def start_app(
    host: Annotated[str, typer.Argument()] = "0.0.0.0",
    port: Annotated[int, typer.Argument()] = 8000,
):
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_config=LOGGING,
        log_level="info",
        reload=False,
    )
