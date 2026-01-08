# Expected Results — Base and Streaming Tests  
## Custom Network Proxy Server

This document specifies the **expected outcomes** for the automated test scripts
located in the `tests/` and `tests/streaming_tests/` directories.

All tests assume:
- The proxy server is running on the configured port
- Correct proxy credentials are used where required
- Tests are executed using PowerShell with `curl.exe`

##  How to Start the Proxy Server

The proxy server can be started using the provided **Makefile**, which simplifies execution and ensures consistency.

### Prerequisites
- Python 3.8 or above installed
- `make` utility available (Git Bash / MSYS2 / WSL recommended on Windows)

### Steps to Run

1. Open a terminal in the project root directory.
2. Start the proxy server using the following command:
```
make run
```
On successful startup, the following message will appear:
INFO - Proxy server running on port 8888
The proxy will now listen for incoming client connections on the configured port.

 Keep this terminal open while running tests, as the proxy must remain active.
---

## 1. Authentication Test (`test_auth.ps1`)

### Purpose
Verify that the proxy enforces authentication and allows access only with valid
credentials.

### Expected Results

- Request without credentials:
  HTTP/1.1 407 Proxy Authentication Required
  
- Request with valid credentials:
  HTTP/1.1 200 OK
  
Proxy logs should record authentication success or failure.

---

## 2. Domain Blocking Test (`test_blocking.ps1`)

### Purpose
Ensure requests to blocked domains are denied.

### Expected Results

HTTP/1.1 403 Forbidden

The proxy must not forward blocked requests, and the event should be logged.

---

## 3. Cache Behavior Test (`test_cache.ps1`)

### Purpose
Confirm correct cache handling for HTTP GET requests.

### Expected Results

- First request:
  - Cache miss
  - Response fetched from destination server
- Second request:
  - Cache hit
  - Response served directly from cache

Proxy logs should clearly indicate cache MISS followed by HIT.

---

## 4. Request Forwarding Test (`test_forwarding.ps1`)

### Purpose
Verify that standard HTTP requests are forwarded correctly through the proxy.

### Expected Results

HTTP/1.1 200 OK

The response body from the destination server should be returned unchanged.

---

## 5. Concurrency Test (`test_concurrency.ps1`)

### Purpose
Validate proxy behavior under multiple simultaneous client connections.

### Expected Results

- All concurrent requests complete successfully
- No server crashes or deadlocks
- Logs show overlapping request handling

This confirms correct thread pool operation.

---

## 6. HTTPS CONNECT Test (`test_https.ps1`)

### Purpose
Verify HTTPS tunneling using the CONNECT method.

### Expected Results

HTTP/1.1 200 Connection Established

After tunnel establishment:
- Encrypted TLS traffic passes transparently
- Proxy does not inspect or modify TLS data

---

## 7. Malformed Request Handling (`test_malformed.ps1`)

### Purpose
Ensure robustness against invalid or malformed HTTP requests.

### Expected Results

- Invalid requests are rejected gracefully
- Proxy does not crash or hang
- Errors are logged appropriately
- Connections are closed safely

Possible responses include:
HTTP/1.1 400 Bad Request

---

## 8. Direct Streaming Test (`streaming_tests/direct_stream.ps1`)

### Purpose
Measure baseline download behavior without proxy involvement.

### Expected Results

- File downloads successfully
- Transfer completes without interruption
- HTTP status code is 200
- No proxy logs are generated

This serves as the baseline for comparison.

---

## 9. Proxy Streaming Test (`streaming_tests/proxy_stream.ps1`)

### Purpose
Verify streaming behavior when traffic passes through the proxy.

### Expected Results

- File downloads completely via the proxy
- Data is streamed chunk by chunk
- No full response buffering occurs
- Memory usage remains stable
- Download speed is comparable to direct streaming

Proxy logs should indicate continuous data forwarding.

---

## 10. Sample Logs Verification (`sample_logs.txt`)

### Purpose
Validate correctness and clarity of proxy log output.

### Expected Results

Logs should include:
- Timestamps
- Request method and destination
- Cache hits and misses
- Authentication events
- Error messages where applicable

Log entries must be readable and thread-safe.

---

## Summary Table

| Test Script | Expected Outcome |
|------------|------------------|
test_auth.ps1 | Authentication enforced |
test_blocking.ps1 | Blocked domains denied |
test_cache.ps1 | Cache hit/miss verified |
test_forwarding.ps1 | HTTP forwarding successful |
test_concurrency.ps1 | Concurrent handling confirmed |
test_https.ps1 | HTTPS tunnel established |
test_malformed.ps1 | Graceful error handling |
direct_stream.ps1 | Baseline streaming success |
proxy_stream.ps1 | Streaming via proxy verified |

---

## Conclusion

All listed tests are expected to complete without proxy failure.  
Successful execution confirms correctness of authentication, filtering, caching,
concurrency handling, HTTPS tunneling, and streaming-based forwarding.

---

**End of Expected Results Document**
