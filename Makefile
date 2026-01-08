
# Custom Network Proxy Server - Makefile

# ---------------- Variables ----------------

PYTHON      := python
SRC_DIR     := src
TEST_DIR    := tests
STREAM_DIR  := tests/streaming_tests

# PowerShell (Windows)
PWSH := powershell -NoProfile -ExecutionPolicy Bypass -File

.DEFAULT_GOAL := help

# ---------------- Main Targets ----------------

.PHONY: run install test check clean help

## Run the proxy server
run:
	$(PYTHON) $(SRC_DIR)/proxy_server.py

## Install dependencies (standard library only)
install:
	@echo "No external dependencies required."

## Run ALL tests
test:
	@echo "=== Running ALL proxy tests ==="
	$(MAKE) test_auth
	$(MAKE) test_blocking
	$(MAKE) test_cache
	$(MAKE) test_forwarding
	$(MAKE) test_concurrency
	$(MAKE) test_https
	$(MAKE) test_malformed
	$(MAKE) test_direct_stream
	$(MAKE) test_proxy_stream
	@echo "=== All tests completed ==="

## Python syntax check
check:
	@echo "Checking Python syntax..."
	$(PYTHON) -m py_compile $(SRC_DIR)/*.py
	@echo "Syntax OK"

## Cleanup generated files
clean:
	@echo "Cleaning generated files..."
	-del /Q *.zip *.bin 2>nul || true
	@echo "Cleanup complete"

# Individual Test Targets 

.PHONY: \
	test_auth test_blocking test_cache test_forwarding \
	test_concurrency test_https test_malformed \
	test_direct_stream test_proxy_stream

test_auth:
	$(PWSH) $(TEST_DIR)/test_auth.ps1

test_blocking:
	$(PWSH) $(TEST_DIR)/test_blocking.ps1

test_cache:
	$(PWSH) $(TEST_DIR)/test_cache.ps1

test_forwarding:
	$(PWSH) $(TEST_DIR)/test_forwarding.ps1

test_concurrency:
	$(PWSH) $(TEST_DIR)/test_concurrency.ps1

test_https:
	$(PWSH) $(TEST_DIR)/test_https.ps1

test_malformed:
	$(PWSH) $(TEST_DIR)/test_malformed.ps1

test_direct_stream:
	$(PWSH) $(STREAM_DIR)/direct_stream.ps1

test_proxy_stream:
	$(PWSH) $(STREAM_DIR)/proxy_stream.ps1

# ---------------- Help ----------------

help:
	@echo ""
	@echo "Custom Network Proxy Server - Make Commands"
	@echo "------------------------------------------"
	@echo ""
	@echo "Server:"
	@echo "  make run                 - Start proxy server"
	@echo ""
	@echo "Testing:"
	@echo "  make test                - Run all tests"
	@echo "  make test_auth           - Authentication tests"
	@echo "  make test_blocking       - Domain blocking tests"
	@echo "  make test_cache          - Cache hit/miss tests"
	@echo "  make test_forwarding     - HTTP forwarding tests"
	@echo "  make test_concurrency    - Multi-client tests"
	@echo "  make test_https          - HTTPS CONNECT tests"
	@echo "  make test_malformed      - Invalid request tests"
	@echo "  make test_direct_stream  - Direct streaming baseline"
	@echo "  make test_proxy_stream   - Proxy streaming test"
	@echo ""
	@echo "Utility:"
	@echo "  make check               - Python syntax check"
	@echo "  make clean               - Remove generated files"
	@echo ""
