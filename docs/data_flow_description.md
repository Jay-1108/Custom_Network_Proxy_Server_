# Data Flow Description  
## Incoming Request Handling and Outbound Forwarding

This document describes the **end-to-end data flow** within the Custom Network Proxy Server, explaining how client requests are received, processed, forwarded to destination servers, and how responses are relayed back to clients.

The focus is on **clarity of flow**, **module interaction**, and **streaming-based forwarding**.

---

## 1. Overview of Data Flow

The proxy server operates as an intermediary that intercepts client requests, applies policy and processing logic, and then forwards traffic to destination servers. Responses from servers are streamed back to clients without full buffering.

At a high level, the data flow follows this sequence:


---

## 2. Incoming Request Data Flow

### 2.1 Client Connection Establishment

1. A client initiates a TCP connection to the proxy server.
2. The proxy listener socket accepts the connection.
3. The accepted client socket is placed into a shared connection queue.

This decouples connection acceptance from request processing.

---

### 2.2 Assignment to Worker Thread

1. A worker thread retrieves a `(client_socket, client_address)` pair from the queue.
2. The worker becomes responsible for handling the complete lifecycle of that client request.

---

### 2.3 Request Reception

1. The worker reads raw bytes from the client socket.
2. HTTP headers are read first until the header terminator (`\r\n\r\n`) is encountered.
3. If a `Content-Length` header is present, the exact number of request body bytes is read.
4. The complete request is reconstructed as a raw byte sequence.

This ensures correctness for methods such as POST and PUT.

---

### 2.4 HTTP Parsing

1. The raw request bytes are passed to the HTTP parser.
2. The parser extracts:
   - HTTP method
   - Request URL
   - HTTP version
   - Header fields
   - Destination host and port
3. A structured request object is created and used by downstream modules.

---

## 3. Request Processing Pipeline

After parsing, the request flows through a fixed sequence of processing stages.

---

### 3.1 Authentication Check

1. The worker examines the `Proxy-Authorization` header.
2. Credentials are validated against the authentication module.
3. If authentication fails:
   - The request is rejected
   - A `407 Proxy Authentication Required` response is returned
   - Processing stops

---

### 3.2 Domain Filtering

1. The destination host is checked against a blocklist.
2. If the host is blocked:
   - A `403 Forbidden` response is sent
   - No outbound connection is created

---

### 3.3 HTTPS CONNECT Handling

If the request method is `CONNECT`:

1. The proxy establishes a TCP connection to the specified host and port.
2. A `200 Connection Established` response is sent to the client.
3. The proxy enters tunneling mode.
4. Encrypted bytes are forwarded bidirectionally between client and server.
5. TLS payloads are not inspected or modified.

For CONNECT requests, no HTTP-level forwarding occurs beyond tunnel setup.

---

## 4. Outbound Forwarding Flow (Non-CONNECT Requests)

For standard HTTP methods (GET, POST, PUT, etc.), the following steps are performed.

---

### 4.1 Cache Lookup (Optional)

1. A cache key is generated from the request host and path.
2. If a cached response exists:
   - The response is sent directly to the client
   - No server connection is made
3. If no cached entry is found:
   - The request is forwarded to the destination server

Caching is applied only to eligible GET requests.

---

### 4.2 Establishing Server Connection

1. A new TCP socket is created for the destination server.
2. The socket connects to the resolved host and port.
3. The raw client request bytes are sent to the server.

---

## 5. Streaming Response Relay

### 5.1 Response Reception

1. The proxy begins reading data from the server socket in fixed-size chunks.
2. No attempt is made to read the entire response into memory.

---

### 5.2 Streaming to Client

1. Each chunk received from the server is immediately forwarded to the client socket.
2. This continues until the server closes the connection or no more data is available.

This streaming approach ensures:
- Low memory usage
- Immediate data delivery
- Efficient handling of large responses

---

### 5.3 Connection Termination

1. Once the response stream ends:
   - The server socket is closed
   - The client socket is closed
2. The worker thread returns to the queue to handle the next connection.

---

## 6. Error Handling Flow

At any stage of the data flow:
- Socket errors
- Parsing errors
- Connection failures

are handled gracefully by:
- Logging the error
- Sending appropriate HTTP error responses
- Closing affected sockets safely

---

## 7. Summary of Data Flow

The proxy server processes data using a clear and linear flow:

1. Accept client connection
2. Read and parse request
3. Authenticate and filter
4. Handle CONNECT or HTTP forwarding
5. Stream server responses back to client
6. Clean up resources

This design ensures correctness, efficiency, and scalability.

---

## 8. Conclusion

The data flow architecture of the proxy server emphasizes **modularity**, **streaming-based forwarding**, and **robust request handling**.  
By separating connection acceptance, request processing, and response forwarding, the system achieves efficient handling of concurrent network traffic while maintaining low resource usage.

---

**End of Document**
