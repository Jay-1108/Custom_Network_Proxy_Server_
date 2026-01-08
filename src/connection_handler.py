import socket
from http_parser import HTTPParser
from filter_engine import FilterEngine
from cache_manager import CacheManager
from https_tunnel import handle_https_tunnel
from auth import AuthManager


class ConnectionHandler:
    def __init__(self, connection_queue, logger, cache_manager=None):
        self.queue = connection_queue
        self.logger = logger
        self.parser = HTTPParser()
        self.filter = FilterEngine()

        # Shared or local cache
        if cache_manager is not None:
            self.cache = cache_manager
        else:
            self.cache = CacheManager(max_entries=50)

        self.auth = AuthManager()
        self.run()

    def run(self):
        while True:
            client_socket, client_addr = self.queue.get()
            try:
                self.handle_client(client_socket, client_addr)
            except Exception as e:
                self.logger.log_error(f"Handler error: {e}")
            finally:
                client_socket.close()

    def handle_client(self, client_socket, client_addr):
        # Receive full HTTP request (headers + body if any)
        raw_request = self._recv_http_request(client_socket)

        self.logger.log_info(f"RAW REQUEST: {raw_request[:200]}...")

        # Parse request
        request = self.parser.parse(raw_request)
        if not request:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            self.logger.log_error("Malformed request")
            return

        # Extract Content-Length (case-insensitive)
        content_length = 0
        for k, v in request.headers.items():
            if k.lower() == "content-length":
                content_length = int(v)
                break

        self.logger.log_info(
            f"REQUEST {request.method} {request.host}:{request.port} "
            f"Content-Length={content_length}"
        )

        # Authentication
        if not self.auth.is_request_authorized(request.headers):
            client_socket.sendall(b"HTTP/1.1 407 Proxy Authentication Required\r\n\r\n")
            return

        # Filtering
        if self.filter.is_blocked(request.host):
            self.logger.log_info(f"Blocked: {request.host}")
            client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n")
            return

        # HTTPS CONNECT tunnel
        if request.method == "CONNECT":
            handle_https_tunnel(
                client_socket,
                request.host,
                int(request.port),
                self.logger
            )
            return

        # Cache key (GET only)
        if '?' in request.url:
            path = request.url.split('?')[0].split('/', 3)[-1]
            query = request.url.split('?')[1]
            cache_key = f"{request.host}:{path}?{query}"
        else:
            path = request.url.split('/', 3)[-1] if '/' in request.url else request.url
            cache_key = f"{request.host}:{path}"

        self.logger.log_info(f"CACHE KEY: {cache_key}")

        # Cache lookup (GET only)
        cached = self.cache.get(cache_key)
        if cached is not None:
            self.logger.log_info(f"CACHE HIT: {cache_key}")
            client_socket.sendall(cached)
            return

        # Forward request to server and STREAM response
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(10)
            server_socket.connect((request.host, int(request.port)))
            server_socket.sendall(request.raw)

            # ✅ STREAM response (no buffering)
            self.relay_stream(server_socket, client_socket)

            server_socket.close()

            self.logger.log_info(
                f"{request.method} {request.host}:{request.port} "
                f"Content-Length={content_length} - STREAMED"
            )

        except Exception as e:
            self.logger.log_error(f"Failed to fetch from server: {e}")
            client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")

    # ==========================================================
    # STREAMING RELAY (REQUIRED BY SPEC)
    # ==========================================================
    def relay_stream(self, source, destination):
        try:
            while True:
                chunk = source.recv(4096)
                if not chunk:
                    break
                destination.sendall(chunk)
        except:
            pass

    # ==========================================================
    # CONTENT-LENGTH–AWARE REQUEST RECEIVER
    # ==========================================================
    def _recv_http_request(self, sock):
        sock.settimeout(5)
        data = b""

        # Read headers
        while b"\r\n\r\n" not in data:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk

        if b"\r\n\r\n" not in data:
            return data

        header_part, remaining = data.split(b"\r\n\r\n", 1)
        headers_text = header_part.decode(errors="ignore")

        # Parse Content-Length
        content_length = 0
        for line in headers_text.split("\r\n"):
            if line.lower().startswith("content-length"):
                content_length = int(line.split(":", 1)[1].strip())
                break

        body = remaining
        bytes_needed = content_length - len(body)

        while bytes_needed > 0:
            chunk = sock.recv(4096)
            if not chunk:
                break
            body += chunk
            bytes_needed -= len(chunk)

        return header_part + b"\r\n\r\n" + body
