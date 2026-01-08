# Concurrency Model and Design Rationale

## 1. Overview of the Concurrency Approach

The proxy server follows a **thread pool–based concurrency model** supported by a
**bounded connection queue**.  
This approach enables the server to process multiple client connections concurrently
while maintaining controlled resource usage and predictable behavior.

Instead of spawning a new thread for every incoming client, a fixed number of worker
threads are reused to handle connections fetched from a shared queue.

---

## 2. Selected Model: Thread Pool with Bounded Queue

### Key Characteristics

- A **single listener thread** accepts incoming TCP connections
- Accepted connections are placed into a **bounded FIFO queue**
- A fixed number of **worker threads** retrieve connections from the queue
- Each worker processes one client connection at a time

This design follows a classic **producer–consumer pattern**.

---

## 3. Rationale for Choosing a Thread Pool

### 3.1 Controlled Resource Utilization

A thread-per-connection model can lead to:
- excessive thread creation
- high memory consumption
- poor system stability under load

By using a thread pool:
- the number of active threads is capped
- CPU and memory usage remain predictable
- the system avoids resource exhaustion

---

### 3.2 Simplicity Compared to Event-Driven Models

Asynchronous event-loop models (e.g., `asyncio`, `select`, `epoll`) offer high scalability
but introduce:
- non-blocking I/O complexity
- callback-based or coroutine-based control flow
- increased debugging difficulty

A thread pool provides:
- linear, easy-to-follow execution flow
- simpler debugging and logging
- better suitability for academic projects and evaluations

---

### 3.3 Suitability for Network-Bound Workloads

This proxy server is primarily **I/O-bound**, not CPU-bound.

In Python:
- blocking network I/O releases the Global Interpreter Lock (GIL)
- multiple threads can make progress during socket operations

As a result, a thread pool performs efficiently for:
- HTTP request forwarding
- HTTPS tunneling
- streaming large responses

---

## 4. Operational Workflow

### Step-by-Step Execution Flow

1. **Main Listener Thread**
   - Listens on a configured TCP port
   - Accepts incoming client connections
   - Pushes `(client_socket, client_address)` into the queue

2. **Connection Queue**
   - Acts as a buffer between clients and workers
   - Enforces backpressure when the system is busy
   - Prevents unlimited connection buildup

3. **Worker Threads**
   Each worker repeatedly:
   - Retrieves a connection from the queue
   - Parses the HTTP or CONNECT request
   - Performs authentication checks
   - Applies domain filtering rules
   - Handles caching logic (GET requests only)
   - Forwards traffic to the destination server
   - Streams responses back to the client

This pipeline ensures balanced and fair request handling.

---

## 5. Benefits of the Chosen Model

### ✔ Predictable Performance
The fixed number of threads ensures stable behavior even during traffic spikes.

### ✔ Fair Request Handling
Connections are processed in FIFO order, avoiding starvation.

### ✔ Ease of Testing and Debugging
Thread-based logic produces clearer stack traces and simpler logs.

### ✔ Appropriate for Academic and Moderate Real-World Use
The model easily supports:
- lab experiments
- coursework evaluation
- moderate concurrent client traffic

---

## 6. Limitations

### ⚠ Queue Saturation
If incoming connections exceed the queue capacity, new clients must wait until space
becomes available.

### ⚠ Python GIL Constraints
While network I/O scales well, CPU-intensive tasks would not benefit significantly from
threading.

### ⚠ Not Optimized for Massive Scale
For extremely high concurrency (thousands of simultaneous clients), event-driven
architectures may scale better.

---

## 7. Justification for This Project

This concurrency model was chosen because it:

- Aligns well with project requirements
- Provides a clean and understandable architecture
- Balances performance and simplicity
- Demonstrates sound system design principles
- Is easy to explain during viva or evaluation

---

## 8. Summary

The proxy server employs a **thread pool combined with a bounded queue** to handle
concurrent client connections efficiently.  
This model delivers reliable performance, controlled resource usage, and clear execution
flow, making it an excellent fit for both academic evaluation and practical proxy
implementations.

---
