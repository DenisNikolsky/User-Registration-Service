import json
import logging
from opentelemetry import trace


class JsonFormatter(logging.Formatter):
    def format(self, record):
        current_span = trace.get_current_span()
        trace_id = "0" * 32

        if current_span and current_span.get_span_context().is_valid:
            trace_id = format(current_span.get_span_context().trace_id, '032x')

        log = {
            "level": record.levelname,
            "message": record.getMessage(),
            "trace_id": trace_id
        }

        return json.dumps(log)


logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger.addHandler(handler)
