import socket
import json
import threading
import queue
import signal
import sys
from connection_handler import ConnectionHandler
from logger import ProxyLogger
from cache_manager import CacheManager


class ProxyServer:
    def __init__(self, config_path="config/proxy_config.json"):
        with open(config_path, "r") as f:
            config = json.load(f)

        self.listen_port = config["listen_port"]
        self.thread_pool_size = config["thread_pool_size"]

        self.logger = ProxyLogger(config["log_file"])
        self.connection_queue = queue.Queue(maxsize=100)

        # Shared cache manager
        self.cache_manager = CacheManager(max_entries=50)

        # Graceful shutdown state
        self.running = True
        self.server_socket = None

        # Register signal handlers
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.listen_port))
        self.server_socket.listen(100)

        self.logger.log_info(f"Proxy server running on port {self.listen_port}")

        # Start worker thread pool
        for _ in range(self.thread_pool_size):
            t = threading.Thread(
                target=ConnectionHandler,
                args=(self.connection_queue, self.logger, self.cache_manager),
                daemon=True
            )
            t.start()

        # Accept loop (graceful)
        while self.running:
            try:
                client_socket, client_addr = self.server_socket.accept()
                self.connection_queue.put((client_socket, client_addr))
            except OSError:
                break  # socket closed during shutdown

        self.logger.log_info("Proxy server stopped accepting new connections")

    def shutdown(self, signum, frame):
        self.logger.log_info(
            f"Received shutdown signal ({signum}). Shutting down gracefully..."
        )
        self.running = False

        # Close listening socket to unblock accept()
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

        sys.exit(0)


if __name__ == "__main__":
    ProxyServer().start()
