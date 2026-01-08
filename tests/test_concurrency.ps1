Write-Host "=== TEST: Concurrency (10 parallel requests) ==="

$jobs = @()

for ($i = 1; $i -le 10; $i++) {
    $jobs += Start-Job -ScriptBlock {
        curl.exe -s -x localhost:8888 --proxy-user admin:password123 http://httpbin.org/get
    }
}

Write-Host "Waiting for all jobs to complete..."
$jobs | Wait-Job | Receive-Job

Write-Host "=== TEST COMPLETE ==="-ForegroundColor green