import logging
import os
import sys

# =======================
# Получаем уровень логирования из переменной окружения
# =======================
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# =======================
# Путь к лог-файлу
# =======================
log_dir = "/var/log/backend"
log_file_path = os.path.join(log_dir, "app.log")

# Убедимся, что директория существует
os.makedirs(log_dir, exist_ok=True)

# =======================
# Форматтеры для system и application
# =======================
system_formatter = logging.Formatter(
    fmt='[%(asctime)s] [SYSTEM] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

application_formatter = logging.Formatter(
    fmt='[%(asctime)s] [APP] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# =======================
# Создаём логгеры
# =======================
system_logger = logging.getLogger("system")
application_logger = logging.getLogger("application")

system_logger.setLevel(log_level)
application_logger.setLevel(log_level)

# =======================
# Хендлер — вывод в консоль (stdout)
# =======================
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(system_formatter)  # можно один и тот же

# =======================
# Хендлер — вывод в файл
# =======================
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(application_formatter)  # можно разный стиль

# =======================
# Добавляем хендлеры (если ещё не добавлены)
# =======================
if not system_logger.hasHandlers():
    system_logger.addHandler(console_handler)
    system_logger.addHandler(file_handler)

if not application_logger.hasHandlers():
    application_logger.addHandler(console_handler)
    application_logger.addHandler(file_handler)