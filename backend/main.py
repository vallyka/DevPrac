from fastapi import FastAPI, HTTPException, Request
from db import get_connection
from pydantic import BaseModel
from logging_config import system_logger, application_logger

# ==== Prometheus ====
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# ============================
# Модели
# ============================

class Task(BaseModel):
    title: str
    done: bool = False

class FrontendLog(BaseModel):
    level: str
    message: str
    service: str = "frontend"

# ============================
# Инициализация FastAPI
# ============================

app = FastAPI()

# Логи при старте
system_logger.info("🚀 FastAPI запускается")
application_logger.info("📦 Приложение инициализировано")

# ============================
# Метрики Prometheus
# ============================

REQUEST_COUNT = Counter(
    "http_requests_total", "Общее количество HTTP-запросов",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Время выполнения запроса",
    ["method", "endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ============================
# Роуты
# ============================

@app.get("/")
def read_root():
    system_logger.info("📥 Получен GET-запрос на /")
    return {"message": "Hello from FastAPI!"}


@app.get("/tasks")
def get_tasks():
    application_logger.info("📥 Получен GET-запрос на /tasks")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, done FROM tasks")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        application_logger.info(f"✅ Найдено {len(rows)} задач(и)")
        return [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]
    except Exception as e:
        application_logger.error(f"❌ Ошибка при получении задач: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении задач")


@app.post("/tasks")
def create_task(task: Task):
    application_logger.info(f"📥 POST /tasks с данными: {task}")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
            (task.title, task.done)
        )
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        application_logger.info(f"✅ Задача создана с ID {task_id}")
        return {"id": task_id, "title": task.title, "done": task.done}
    except Exception as e:
        application_logger.error(f"❌ Ошибка при создании задачи: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании задачи")


@app.post("/api/logs")
async def receive_frontend_log(log: FrontendLog, request: Request):
    ip = request.client.host
    msg = f"[{log.service.upper()}] {ip} → {log.message}"

    level = log.level.lower()
    if level == "info":
        application_logger.info(msg)
    elif level in ("warn", "warning"):
        application_logger.warning(msg)
    elif level == "error":
        application_logger.error(msg)
    else:
        application_logger.warning(f"[FRONTEND] Неизвестный уровень '{log.level}', сообщение: {msg}")

    return {"status": "ok"}
