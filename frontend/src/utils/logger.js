const sendToBackend = (level, message) => {
    fetch("/api/logs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        level,
        message,
        service: "frontend",
      }),
    }).catch((e) => {
      console.warn("⛔ Не удалось отправить лог на backend:", e);
    });
  };
  
  const logger = {
    info: (...args) => {
      console.info("[INFO]", ...args);
      sendToBackend("info", args.join(" "));
    },
    warn: (...args) => {
      console.warn("[WARN]", ...args);
      sendToBackend("warn", args.join(" "));
    },
    error: (...args) => {
      console.error("[ERROR]", ...args);
      sendToBackend("error", args.join(" "));
    },
  };
  
  export default logger;