import logging.config
from settings import logger_config


logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger.'+ __name__)


def main():
    logger.debug(r'это консоль')
    logger.info(r'это консоль и файл')
    logger.warning(r'это консоль файл телега')
    logger.error(r'это консоль файл телега мыло')
    print(10 + 15)


if __name__ == '__main__':
    main()
    assert passw_stranght('') == 'Too Weak'
