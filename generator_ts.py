# -*- coding: utf-8 -*-
import logging.config
from settings import logger_config
from typing_extensions import TypeAlias
from typing import Literal
from pathlib import Path

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger.'+ __name__)

SRC_DIR = Path(__file__).parent / "src"

BaseFolder: TypeAlias = Literal["components", "pages"]
# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():




# -----------------------------------------------------------------------
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
