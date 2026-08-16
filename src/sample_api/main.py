import json
import logging
import sys
from datetime import UTC, datetime

from fastapi import FastAPI, Request


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "@timestamp": datetime.now(UTC).isoformat(),
            "log.level": record.levelname.lower(),
            "message": record.getMessage(),
            "service.name": "proste-api",
            "logger.name": record.name,
        }
        if hasattr(record, "http_method"):
            log_record["http.method"] = record.http_method
        if hasattr(record, "http_path"):
            log_record["url.path"] = record.http_path
            
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())

logger = logging.getLogger("api-logger")
logger.setLevel(logging.INFO)
logger.handlers = [handler]
logger.propagate = False

app = FastAPI(title="Elastic JSON API", version="1.0")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now(UTC)
    response = await call_next(request)
    duration = (datetime.now(UTC) - start_time).total_seconds()

    logger.info(
        "HTTP request handled",
        extra={
            "http_method": request.method,
            "http_path": request.url.path,
            "http.status_code": response.status_code,
            "event.duration": duration
        }
    )
    return response

@app.get("/")
def read_root():
    logger.info("Wywołano endpoint główny /")
    return {"status": "ok", "message": "API działa"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    logger.info(f"Pobieranie przedmiotu o ID: {item_id}")
    return {"item_id": item_id, "name": "Przykładowy przedmiot"}

@app.get("/healtz")
def healtz():
    logger.info("Healtcheck")
    return {"result": "ok"}