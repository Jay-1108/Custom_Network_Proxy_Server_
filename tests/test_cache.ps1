Write-Host "=== TEST: Cache Behavior ==="

Write-Host "First request (MISS expected)"
curl.exe -x localhost:8888 --proxy-user admin:password123 http://httpbin.org/get

Write-Host "`nSecond request (HIT expected)"
curl.exe -x localhost:8888 --proxy-user admin:password123 http://httpbin.org/get

Write-Host " TEST COMPLETE "-ForegroundColor green
