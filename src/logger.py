import datetime
import threading


class ProxyLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.lock = threading.Lock()   # 🔒 Thread lock

    def log(self, msg, level="INFO"):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        out = f"{ts} - {level} - {msg}".encode(
            'utf-8', errors='replace'
        ).decode('utf-8')

        print(out)

        # 🔒 Thread-safe file write
        with self.lock:
            with open(self.log_path, "a", encoding='utf-8') as f:
                f.write(out + "\n")

    def log_info(self, msg):
        self.log(msg, "INFO")

    def log_error(self, msg):
        self.log(msg, "ERROR")
