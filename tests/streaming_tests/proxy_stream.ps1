Write-Host "=== TEST: Proxy Streaming (100MB via Proxy) ==="-ForegroundColor green

Measure-Command {
    curl.exe -v `
        -x localhost:8888 `
        --proxy-user admin:password123 `
        http://speedtest.tele2.net/100MB.zip `
        --output proxy.zip `
        -w "`nDownload completed with HTTP %{http_code}`n"
}

Write-Host "=== Check proxy.zip downloaded ==="-ForegroundColor green

Write-Host "TEST COMPLETE"-ForegroundColor green
