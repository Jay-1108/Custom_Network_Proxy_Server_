# Custom Network Proxy Server

A multi-threaded **HTTP and HTTPS proxy server** implemented in Python.  
This proxy supports **concurrent clients**, **authentication**, **domain filtering**,
**HTTPS tunneling (CONNECT method)**, **streaming-based forwarding**, and **optional caching**.

The project is designed for academic evaluation and demonstrates practical networking
and system design concepts used in real-world proxy servers.

---

##  Features

- HTTP request forwarding
- HTTPS tunneling using CONNECT method
- Concurrent client handling using a thread pool
- Streaming response relay (no full buffering)
- Basic proxy authentication
- Domain blocking and filtering
- Optional caching for GET requests
- Thread-safe logging
- Graceful handling of malformed requests

---

##  Technology Stack

- **Language:** Python 3  
- **Networking:** TCP sockets  
- **Concurrency:** Thread pool + queue  
- **Protocols:** HTTP/1.1, HTTPS (CONNECT)  
- **Testing:** PowerShell scripts + curl  

---

##  Project Structure

CUSTOM-NETWORK-PROXY-SERVER/
│
├── config/
│ └── proxy_config.json
│
├── docs/
│ ├── architecture_and_working.md
│ ├── concurrency_model.md
│ ├── data_flow_description.md
│ ├── error_handling.md
│ └── limitations_and_future_work.md
│
├── Project Statement/
│
├── src/
│ ├── proxy_server.py
│ ├── connection_handler.py
│ ├── http_parser.py
│ ├── https_tunnel.py
│ ├── auth.py
│ ├── filter_engine.py
│ ├── cache_manager.py
│ └── logger.py
│
├── tests/
│ ├── streaming_tests/
│ │ ├── direct_stream.ps1
│ │ └── proxy_stream.ps1
│ │
│ ├── test_auth.ps1
│ ├── test_blocking.ps1
│ ├── test_cache.ps1
│ ├── test_concurrency.ps1
│ ├── test_forwarding.ps1
│ ├── test_https.ps1
│ ├── test_malformed.ps1
│ └── sample_logs.txt
│
├── Makefile
├── setup.py
├── requirements.txt
├── README.md
├── direct.zip
├── proxy.zip
├── large_test.bin
└── received.bin

---

##  Configuration

Edit the proxy configuration file:

config/proxy_config.json

Example:

```json
{
  "listen_port": 8888,
  "thread_pool_size": 10,
  "log_file": "proxy.log"
}

# Running the Proxy Server
1 Install Python (if not installed)

Python version 3.8 or above is recommended.

2 Start the proxy server:
python src/proxy_server.py

You should see a message similar to:
INFO - Proxy server running on port 8888

Testing the Proxy

  On Windows PowerShell, always use curl.exe instead of curl.
🔹 HTTP Forwarding Test
    curl.exe -x localhost:8888 --proxy-user admin:password123 http://httpbin.org/get
🔹 HTTPS CONNECT Test
    curl.exe -x localhost:8888 --proxy-user admin:password123 https://httpbin.org/get
Expected output includes:
HTTP/1.1 200 Connection Established

🔹 Streaming Test (Large File)
     Direct streaming test:
     powershell -File tests/streaming_tests/direct_stream.ps1
    Proxy streaming test:
    powershell -File tests/streaming_tests/proxy_stream.ps1
These tests verify that responses are streamed chunk-by-chunk
without buffering entire files in memory.

🔹 Automated Test Suite (Makefile)
    If make is available:
    make run
    In another terminal:
    make test
Individual tests can also be run, for example:
make test_https
make test_malformed
make test_proxy_stream

# Authentication

  The proxy enforces Basic Proxy Authentication.

  Header used: Proxy-Authorization

  Unauthorized requests receive:
  HTTP/1.1 407 Proxy Authentication Required
# HTTPS Support

  HTTPS traffic is handled using the CONNECT method

  TLS traffic is forwarded transparently

  No TLS inspection or decryption is performed

# Concurrency Model

  Single listener thread

  Bounded connection queue

  Fixed-size worker thread pool

  Each worker handles one client connection at a time

  This ensures predictable performance and controlled resource usage.

# Limitations

  No persistent connection (keep-alive) support

  No TLS interception

  Limited caching strategy

  Thread-based scalability constraints

  See docs/limitations_and_future_work.md for details.

# Documentation

  Detailed documentation is available in the docs/ directory, including:

  Architecture and internal working

  Concurrency model and rationale

  Data flow description

  Error handling strategy

  Limitations and future enhancements

# Educational Value

This project demonstrates:

  Socket programming

  Multithreaded server design

  HTTP and HTTPS protocol handling

  Streaming I/O

  Robust error handling

  Proxy server architecture

📌# Conclusion

  The Custom Network Proxy Server provides a clear, modular, and practical
implementation of a real-world proxy system.
It balances simplicity and functionality, making it well-suited for academic
evaluation and learning purposes.


Author: A JAYENDRA SHIVASAI
        IIT Roorkee