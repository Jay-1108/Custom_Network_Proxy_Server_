Write-Host "=== TEST: Direct Streaming (No Proxy) ==="-ForegroundColor green

# Measure raw download speed and total time without proxy
Measure-Command {
    curl.exe `
        http://speedtest.tele2.net/100MB.zip `
        --output direct.zip `
          -w "`nDownload completed with HTTP %{http_code}`n"
}

Write-Host "=== Check direct.zip downloaded ==="-ForegroundColor green

Write-Host "TEST COMPLETE"-ForegroundColor green
