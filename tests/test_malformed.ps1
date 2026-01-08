Write-Host "=== TEST SUITE: Malformed and Invalid HTTP Requests ===" -ForegroundColor Green
Write-Host "Purpose: Verify graceful error handling by proxy" -ForegroundColor Cyan


$proxyHost = "localhost"
$proxyPort = 8888


# Helper Function: Send Raw TCP Request
function Send-RawRequest {
    param (
        [string]$RawText
    )

    $client = New-Object System.Net.Sockets.TcpClient($proxyHost, $proxyPort)
    $stream = $client.GetStream()
    $data = [System.Text.Encoding]::ASCII.GetBytes($RawText)
    $stream.Write($data, 0, $data.Length)
    $stream.Close()
    $client.Close()
}


# Test 1: Request without Host Header
Write-Host "`n[Test 1] Missing Host Header" -ForegroundColor Yellow

$raw1 = "GET / HTTP/1.1`r`n`r`n"
Send-RawRequest $raw1


# Test 2: Malformed URL in Request Line
Write-Host "`n[Test 2] Malformed URL" -ForegroundColor Yellow

$raw2 = "GET http:///invalid_path HTTP/1.1`r`nHost: example.com`r`n`r`n"
Send-RawRequest $raw2


# Test 3: Unsupported HTTP Method
Write-Host "`n[Test 3] Invalid HTTP Method" -ForegroundColor Yellow

$raw3 = "UNKNOWNMETHOD /resource HTTP/1.1`r`nHost: example.com`r`n`r`n"
Send-RawRequest $raw3


# Test 4: Empty Request Payload
Write-Host "`n[Test 4] Empty Request" -ForegroundColor Yellow

$clientEmpty = New-Object System.Net.Sockets.TcpClient($proxyHost, $proxyPort)
$clientEmpty.Close()


# Test 5: Excessively Long Request Line
Write-Host "`n[Test 5] Very Long Request Line" -ForegroundColor Yellow

$longPath = "x" * 6000
$raw5 = "GET /$longPath HTTP/1.1`r`nHost: example.com`r`n`r`n"
Send-RawRequest $raw5


# Test 6: Random Non-HTTP Data
Write-Host "`n[Test 6] Random Garbage Input" -ForegroundColor Yellow

$noise = "!!@@##$$%%%%^^^^&&&&****((((()))))randomDATA123`n`n"
Send-RawRequest $noise


Write-Host "`n=== Malformed Request Test Suite Finished ===" -ForegroundColor Green
