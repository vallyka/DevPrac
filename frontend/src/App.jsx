import logger from "./utils/logger";
import { useEffect } from "react";

function App() {
  useEffect(() => {
    logger.info("⚡ React App загружено");
  }, []);

  const handleClick = () => {
    logger.error("Нажал на кнопку и всё сломалось 💥");
    throw new Error("💥 Имитация краша");
  };

  return (
    <div>
      <h1>Hello from React via Vite! 🎉</h1>
      <button onClick={handleClick}>Сломать</button>
    </div>
  );
}

export default App;