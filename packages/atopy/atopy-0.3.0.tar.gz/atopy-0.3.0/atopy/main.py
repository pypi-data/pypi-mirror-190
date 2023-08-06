import typer
from loguru import logger

from atopy.datetime import pytz_timezone, utc_astimezone, utc_now

app = typer.Typer()


@app.command()
def now(tz: str = "UTC") -> None:
    dt = utc_astimezone(utc_now(), pytz_timezone(tz))
    logger.info(f"now: {dt}")


if __name__ == "__main__":
    app()
