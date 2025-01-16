import logging


# Создаем кастомный форматтер
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    green = "\x1b[32;1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[41m"
    reset = "\x1b[0m"
    format = "%(asctime)s | %(levelname)s | [%(filename)s:%(lineno)d] - %(message)s"

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

# Проверяем, если хендлеры уже добавлены, чтобы избежать дублирования
if not logger.handlers:
    logger.addHandler(handler)

logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень логирования
# Устанавливаем уровень логирования WARNING для asyncio
logging.getLogger("asyncio").setLevel(logging.WARNING)

# Устанавливаем уровень логирования WARNING для sqlalchemy
logging.getLogger("sqlalchemy").setLevel(
    logging.ERROR
)  # Устанавливаем уровень ERROR для всех компонентов

# Исключаем логи для выполнения SQL-запросов в SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.dialects").setLevel(
    logging.ERROR
)  # Исключаем логи диалектов базы данных

# Отключаем прокачку логов в родительские логгеры
logger.propagate = False
