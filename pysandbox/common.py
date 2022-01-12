import logging
import logging.config
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

LOGGING_CONFIG_FILE = Path("logging_config.yaml")

"""Helpful, reusable logic across many scripts"""


def initialize_logging_from_file(log_file: Path = LOGGING_CONFIG_FILE, debug: bool = False) -> None:
    with open(log_file) as f:
        logging_dict = yaml.safe_load(f)
    logging.config.dictConfig(logging_dict)
    if debug:
        pysandbox_logger = logging.getLogger("pysandbox")
        pysandbox_logger.level = logging.DEBUG
    logger.debug(f"Initialized logging from file: {log_file.resolve()}")
