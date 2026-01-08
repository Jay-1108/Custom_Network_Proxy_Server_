Write-Host "=== TEST: HTTPS CONNECT Tunneling ==="
curl.exe -v -x localhost:8888 --proxy-user admin:password123 https://httpbin.org/get

Write-Host " TEST COMPLETE "-ForegroundColor green




Write-Host "=== TEST: HTTP Methods Through Proxy ==="

# Proxy credentials and address (passed directly to curl)
$px = @("-x", "localhost:8888", "--proxy-user", "admin:password123")


# 1. GET
Write-Host "`n[1] GET Request:"
curl.exe @px -v http://httpbin.org/get




# 2. POST

Write-Host "`n[2] POST Request:"
curl.exe @px -v -X POST -d "name=srikanth&msg=hello" http://httpbin.org/post

# 3. PUT
Write-Host "`n[3] PUT Request:"
curl.exe @px -v -X PUT -d "update=this_is_put_test" http://httpbin.org/put

# 4. DELETE
Write-Host "`n[4] DELETE Request:"
curl.exe @px -v -X DELETE http://httpbin.org/delete


# 5. PATCH
Write-Host "`n[5] PATCH Request:"
curl.exe @px -v -X PATCH -d "patched=true" http://httpbin.org/patch 

# 6. OPTIONS
Write-Host "`n[6] OPTIONS Request:"
curl.exe @px -v -X OPTIONS http://httpbin.org/get


Write-Host "`n=== HTTP Method Tests Completed ==="
