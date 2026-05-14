import logging
import json


class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage()
        }

        return json.dumps(log_record)


logger = logging.getLogger("BioSeqAnalyzer")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)

file_handler.setFormatter(JsonFormatter())

logger.handlers.clear()
logger.addHandler(file_handler)