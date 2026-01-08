Write-Host "=== TEST: Domain Blocking ==="

# Ensure domain exists in blocklist
Add-Content -Path "config/blocked_domains.txt" -Value "example.com"

curl.exe -v -x localhost:8888 --proxy-user admin:password123 http://example.com

Write-Host " TEST COMPLETE "-ForegroundColor green
