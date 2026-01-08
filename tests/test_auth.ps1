Write-Host "=== TEST: Proxy Authentication ===" -ForegroundColor Green

$proxy = "localhost:8888"
$creds = "admin:password123"

Write-Host "`n[1] Without credentials (should fail)" -ForegroundColor Cyan
curl.exe -v -x $proxy http://httpbin.org/get

Write-Host "`n[2] With correct credentials (should succeed)" -ForegroundColor Cyan
curl.exe -v -x $proxy --proxy-user $creds http://httpbin.org/get

Write-Host "`n=== Authentication Test Completed ===" -ForegroundColor Green
