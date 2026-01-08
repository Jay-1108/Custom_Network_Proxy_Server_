# Custom Network Proxy Server  
## Architecture and Internal Working

This document explains the **architecture, design decisions, and request flow**
of the **Custom Network Proxy Server** project.  
The system is designed to efficiently handle **multiple concurrent HTTP and HTTPS
clients** using a **threaded, modular architecture**.

---

## 1. Overview

A proxy server acts as an **intermediary** between clients and destination servers.
All client requests are routed through the proxy, which enables:

- Authentication
- Domain filtering
- HTTPS tunneling
- Response streaming
- Optional caching
- Centralized logging

The proxy supports both **HTTP** and **HTTPS (CONNECT method)** traffic.

---

## 2. High-Level Architecture

                    ┌───────────────────────────┐
                    │          CLIENTS          │
                    │ Browsers / Curl / Scripts │
                    └──────────────┬────────────┘
                                   │
                                   ▼
               ┌──────────────────────────────────────┐
               │         PROXY SERVER (TCP)           │
               │──────────────────────────────────────│
               │ • Listens on configured port         │
               │ • Accepts client connections         │
               │ • Enqueues connections               │
               └──────────────┬─────────────────────-─┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │   CONNECTION QUEUE     │
                   │ (Bounded FIFO Queue)   │
                   └────────────┬─────────-─┘
                                │
        ┌───────────────────────┼────────────────────────┐
        ▼                       ▼                        ▼
 ┌─────────────┐        ┌─────────────┐          ┌─────────────┐
 │  Worker 1   │        │  Worker 2   │   ...    │  Worker N   │
 │  (Thread)   │        │  (Thread)   │          │  (Thread)   │
 └──────┬──────┘        └──────┬──────┘          └──────┬──────┘
        │                       │                        │
        ▼                       ▼                        ▼
 ┌────────────────────────────────────────────────────────────┐
 │                    REQUEST PROCESSING PIPELINE             │
 │────────────────────────────────────────────────────────────│
 │ • HTTP Parsing                                             │
 │ • Authentication                                           │
 │ • Domain Filtering                                         │
 │ • HTTPS Tunneling (CONNECT)                                │
 │ • Cache Lookup (GET only)                                  │
 │ • Streaming Forwarding                                     │
 │ • Logging                                                  │
 └────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────────┐
                    │   DESTINATION SERVERS     │
                    │ Websites / APIs / Services│
                    └───────────────────────────┘


---

## 3. Core Components

### 3.1 Client

Clients include:
- Web browsers
- Curl / command-line tools
- API testing tools
- Custom scripts

Clients send requests to the proxy instead of directly contacting servers.

---

### 3.2 Proxy Listener

The main server thread:
- Creates a TCP socket
- Binds to the configured port
- Listens for incoming connections
- Pushes accepted connections into a shared queue

This design prevents blocking during heavy traffic.

---

### 3.3 Connection Queue

The queue acts as a buffer between:
- The accepting thread
- The worker threads

Advantages:
- Controls concurrency
- Prevents overload
- Enables smooth request distribution

---

### 3.4 Worker Threads (Thread Pool)

A fixed-size thread pool is created at startup.

Each worker:
- Retrieves a client connection from the queue
- Processes exactly one connection at a time
- Runs independently of other workers

This enables **true concurrent client handling**.

---

## 4. Request Processing Pipeline

Each worker processes requests through the following steps.

---

### 4.1 HTTP Request Parsing

The parser extracts:
- HTTP method (GET, POST, CONNECT, etc.)
- URL
- HTTP version
- Headers
- Target host and port

This structured representation is used by all other modules.

---

### 4.2 Authentication

The proxy enforces **Basic Proxy Authentication** using the
`Proxy-Authorization` header.

- Authorized requests → processed normally
- Unauthorized requests → rejected with:
        HTTP/1.1 407 Proxy Authentication Required.
This prevents unauthorized proxy usage.

---

### 4.3 Domain Filtering

Requests are checked against a domain blocklist.

- If a domain is blocked:
   HTTP/1.1 403 Forbidden

This module enables access control and policy enforcement.

---

### 4.4 HTTPS Tunneling (CONNECT Method)

For HTTPS requests:
- The proxy detects the `CONNECT host:port` method
- Establishes a TCP connection to the destination server
- Responds with:
   HTTP/1.1 200 Connection Established

After this:
- Encrypted TLS data is forwarded bidirectionally
- No TLS inspection or modification is performed

---

### 4.5 Cache Manager

Caching is applied only to **HTTP GET requests**.

- Cache HIT → response served immediately
- Cache MISS → request forwarded to server

This reduces repeated network traffic and improves performance.

---

### 4.6 Streaming Response Relay

Server responses are relayed **in a streaming fashion**:

- Data is read in fixed-size chunks
- Each chunk is immediately forwarded to the client
- Entire responses are never buffered in memory

Benefits:
- Low memory usage
- Efficient large-file transfers
- Scalable behavior

---

### 4.7 Logging System

The logging module records:
- Incoming requests
- Authentication failures
- Filtered domains
- Cache hits and misses
- HTTPS tunnel creation
- Errors and exceptions

Log writes are thread-safe.

---

## 5. Architectural Benefits

- Supports multiple concurrent clients
- Handles both HTTP and HTTPS traffic
- Memory-efficient streaming
- Modular and extensible design
- Clear separation of responsibilities
- Realistic proxy server behavior

---

## 6. Limitations and Future Enhancements

Possible future improvements:
- Rate limiting
- IP-based access control
- Advanced cache expiration
- Traffic analytics
- TLS interception (out of scope for this project)

---

## 7. Conclusion

This project implements a **robust and scalable proxy server architecture**
that closely mirrors real-world proxy systems.  
By combining multithreading, streaming I/O, authentication, filtering, and HTTPS
tunneling, the proxy efficiently manages modern web traffic.

---

**End of Document**
