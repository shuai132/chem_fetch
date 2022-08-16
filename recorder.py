import json

MAX_RECORD_LINES = 10000


class Recorder:
    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            with open(self.file_path) as f:
                self.data = json.loads(f.read())
                if len(self.data) > MAX_RECORD_LINES:
                    self.clear()
        except Exception:
            self.clear()

    def record(self, name: str):
        self.data[name] = True

    def check(self, name: str) -> bool:
        return self.data.get(name) is True

    def save(self):
        with open(self.file_path, "w") as f:
            f.write(json.dumps(self.data, indent=2))

    def clear(self):
        self.data = {}
        self.save()

    def __del__(self):
        self.save()
