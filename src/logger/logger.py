import logging
import atexit
from logging.handlers import SocketHandler, DEFAULT_TCP_LOGGING_PORT
from typing import Literal


class ProjectLogger:
    def __init__(
        self,
        name: str,
        level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG",
    ) -> None:
        self.logger = logging.getLogger(name)
        self.level = self._set_log_level(level)
        self.socket_handler = None

        self._set_logger_format()
        self._attach_listener()

        atexit.register(self._cleanup)

    def _set_log_level(
        self, level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ):
        match level:
            case "DEBUG":
                return logging.DEBUG
            case "INFO":
                return logging.INFO
            case "WARNING":
                return logging.WARNING
            case "ERROR":
                return logging.ERROR
            case "CRITICAL":
                return logging.CRITICAL

    def _set_logger_format(self) -> None:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _attach_listener(self) -> None:
        self.socket_handler = SocketHandler("localhost", DEFAULT_TCP_LOGGING_PORT)
        self.logger.addHandler(self.socket_handler)

    def _cleanup(self) -> None:
        if self.socket_handler:
            self.socket_handler.close()
            self.logger.removeHandler(self.socket_handler)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)

    def program_start(self) -> None:
        self.info("Program starting")

    def program_end(self) -> None:
        self.info("Program ending")


logger = ProjectLogger("Foo", "DEBUG")
logger.info("This is an info log")
logger.debug("Debuggin' out")
logger.warning("Last warning")
logger.error("That was a mistake buddy")
logger.critical("FUCKING RAGE")
