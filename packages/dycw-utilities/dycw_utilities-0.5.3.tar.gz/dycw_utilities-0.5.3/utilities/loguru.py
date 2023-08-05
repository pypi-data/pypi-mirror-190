from sys import stdout

from beartype import beartype
from loguru import logger

from utilities.logging import LogLevel
from utilities.pathlib import PathLike


@beartype
def setup_loguru(*, name: PathLike = "log") -> None:
    """Set up `loguru` with the standard format strings."""
    logger.remove()

    fmt = (
        "<green>{time:YYYY-MM-DD}</green>"
        " "
        "<bold><green>{time:HH:mm:ss}</green></bold>"
        "."
        "{time:SSS}"
        "  "
        "<cyan>{process.name}</cyan>-{process.id}"
        "  "
        "<green>{name}</green>-<cyan>{function}</cyan>"
        "  "
        "<bold><level>{level.name}</level></bold>"
        "\n"
        "{message}"
    )

    _ = logger.add(stdout, level=LogLevel.INFO, format=fmt, enqueue=True)
    _ = logger.add(
        name,
        level=LogLevel.DEBUG,
        enqueue=True,
        rotation="10 MB",
        retention="1 week",
    )
