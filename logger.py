import logging


# Создаем кастомный форматтер
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    green = "\x1b[32;1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[41m"
    reset = "\x1b[0m"
    format = (
        "%(asctime)s | %(levelname)s | [%(filename)s:%(lineno)d] - %(message)s"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        record.levelname = record.levelname.ljust(8)
        return formatter.format(record)


# Настройка хендлера
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень логирования
handler.setFormatter(CustomFormatter())  # Используем кастомный форматтер

# Настройка логгера
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень логирования
logging.getLogger('asyncio').setLevel(logging.WARNING)  # Устанавливаем уровень WARNING для asyncio
logger.addHandler(handler)
logger.propagate = False
