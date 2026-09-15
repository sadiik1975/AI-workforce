import logging
from pathlib import Path
from typing import Any


class WorkforceLogger:
    def __init__(self, logs_dir: Path | str):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.logs_dir / "workforce.log"

        self._logger = logging.getLogger("been_ventures_workforce")
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        if not self._logger.handlers:
            handler = logging.FileHandler(self.log_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            self._logger.addHandler(handler)

    def log(self, event: str, message: str, **kwargs: Any) -> None:
        self._logger.info("%s %s", event, message)

    def read(self) -> str:
        if not self.log_path.exists():
            return ""
        return self.log_path.read_text(encoding="utf-8")
