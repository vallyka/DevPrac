import React from "react";
import logger from "./utils/logger";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    logger.error("🔥 Ошибка в компоненте", error.toString(), info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return <h2>⚠️ Упс! Что-то пошло не так.</h2>;
    }

    return this.props.children;
  }
}

export default ErrorBoundary;