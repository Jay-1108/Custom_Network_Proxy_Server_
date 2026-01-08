Write-Host "=== TEST: HTTP Forwarding ==="
curl.exe -v -x localhost:8888 http://httpbin.org/get
Write-Host " TEST COMPLETE "-ForegroundColor green
