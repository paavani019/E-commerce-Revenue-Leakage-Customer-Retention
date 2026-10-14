from __future__ import annotations

import logging
import sys

from src.analysis import run_pipeline
from src.logging_utils import configure_logging


def main() -> int:
    configure_logging()
    logger = logging.getLogger("main")
    try:
        outputs = run_pipeline()
        logger.info("Pipeline complete.")
        logger.info("Memo: %s", outputs.memo_path)
        logger.info("Charts dir: %s", outputs.figures_dir)
        logger.info("Tables dir: %s", outputs.tables_dir)
        return 0
    except Exception:
        logger.exception("Pipeline failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

