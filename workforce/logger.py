from __future__ import annotations

import logging
from pathlib import Path


class WorkforceLogger:
    def __init__(self, logs_dir: Path):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.logs_dir / "workforce.log"
        self._logger = logging.getLogger(f"been_ventures_workforce_{abs(hash(str(self.logs_dir)))}")
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        for handler in list(self._logger.handlers):
            self._logger.removeHandler(handler)
            handler.close()

        handler = logging.FileHandler(self.path)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def log(self, event: str, message: str):
        self._logger.info("%s %s", event, message)

    def read(self):
        if not self.path.exists():
            return ""
        return self.path.read_text(encoding="utf-8")
