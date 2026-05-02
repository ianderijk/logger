import logging
import platform
import os
from datetime import datetime
from pathlib import Path


class ProjectLogger:
    def __init__(self, project_name: str, level: str = "DEBUG") -> None:
        self.project_name = project_name
        self.level = level
        self.logger = logging.getLogger(self.project_name)
        self.logger.setLevel(self.level)
        self.logger.propagate = False
        self._create_project_log_directory()
        self._set_logger_format()

    def _build_log_path(self) -> None:
        device = platform.node()
        session_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if "raspberry" in device:
            logs_root = Path("/media/ianderijk/Backup/LogStore")
        else:
            logs_root = Path("/media/idr/ExtDrive/LogStore")
        log_path = logs_root / self.project_name / f"{session_timestamp}.log"
        self.log_path = log_path

    def _create_project_log_directory(self) -> None:
        self._build_log_path()
        log_dir = self.log_path.parent
        if log_dir.exists():
            return
        os.mkdir(log_dir)

    def _set_logger_format(self) -> None:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

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
