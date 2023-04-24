import logging
from datetime import datetime as dt

from pythonjsonlogger import jsonlogger

from app.config import settings # Для установки уровня логгирования


logger = logging.getLogger()    # Определяем логгер
logHandler = logging.StreamHandler()    # Указываем писать логи в консоль


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: dict, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s")

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.log_level)
