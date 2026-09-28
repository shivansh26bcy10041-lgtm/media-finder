"""
History persistence manager for recent queries.
"""

import json
from pathlib import Path

HISTORY_FILE = Path("search_history.json")
MAX_HISTORY = 25
STARTER_HISTORY = ["Pride and Prejudice", "Metropolis 1927", "Beethoven Symphony No. 5", "Severance"]


class HistoryManager:
    def __init__(self, file_path=HISTORY_FILE, max_items=MAX_HISTORY):
        self.file_path = file_path
        self.max_items = max_items
        self.history = self.load()

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return [str(item) for item in data][:self.max_items]
        except (OSError, ValueError):
            pass
        return list(STARTER_HISTORY)

    def remember(self, text):
        if text in self.history:
            self.history.remove(text)
        self.history.insert(0, text)
        self.history = self.history[:self.max_items]

        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
        except OSError:
            pass
        return self.history