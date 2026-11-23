<#
.SYNOPSIS
    Continuous HTTP Traffic Audit for Zero-Downtime Rolling Update (PowerShell)
.DESCRIPTION
    Sends continuous asynchronous HTTP requests to the application version endpoint
    while kubectl rolls out deployment v2, logging status codes and versions.
#>
param(
    [string]$TargetUrl = "http://127.0.0.1:8080/version",
    [string]$Namespace = "devops-lab5"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ManifestPath = Join-Path (Split-Path -Parent $ScriptDir) "kubernetes\05-deployment-v2.yaml"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " Starting Continuous Traffic Audit for Zero-Downtime Rolling Update" -ForegroundColor Cyan
Write-Host " Target Endpoint : $TargetUrl" -ForegroundColor Cyan
Write-Host " Namespace       : $Namespace" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Step 1: Endpoint connectivity check
Write-Host "[Check] Verifying target endpoint availability... " -NoNewline
try {
    $preflight = Invoke-RestMethod -Uri $TargetUrl -TimeoutSec 2
    Write-Host "OK (HTTP 200 - Current Version: $($preflight.version))" -ForegroundColor Green
} catch {
    Write-Host "FAILED" -ForegroundColor Red
    Write-Host "ERROR: Target endpoint is not reachable at $TargetUrl." -ForegroundColor Red
    Write-Host "Ensure port-forwarding or local NodePort is active before testing:" -ForegroundColor Yellow
    Write-Host "  kubectl port-forward -n $Namespace svc/student-k8s-service 8080:80" -ForegroundColor Yellow
    exit 1
}

# Step 2: Background traffic generator
$log = [System.Collections.Concurrent.ConcurrentBag[PSCustomObject]]::new()
$cts = [System.Threading.CancellationTokenSource]::new()

Write-Host "[Traffic] Launching continuous request background worker..." -ForegroundColor Cyan
$task = [System.Threading.Tasks.Task]::Run([Action]{
    $client = [System.Net.Http.HttpClient]::new()
    $client.Timeout = [TimeSpan]::FromSeconds(1)
    $reqId = 0
    while (-not $cts.Token.IsCancellationRequested) {
        $reqId++
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        try {
            $response = $client.GetAsync($TargetUrl).GetAwaiter().GetResult()
            $body = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
            $status = [int]$response.StatusCode
            $version = if ($body -match '"version":\s*"([^"]+)"') { $matches[1] } else { "unknown" }
            $log.Add([PSCustomObject]@{
                Id = $reqId
                Timestamp = (Get-Date).ToString("HH:mm:ss.fff")
                StatusCode = $status
                Version = $version
                DurationMs = $sw.ElapsedMilliseconds
            })
        } catch {
            $log.Add([PSCustomObject]@{
                Id = $reqId
                Timestamp = (Get-Date).ToString("HH:mm:ss.fff")
                StatusCode = 0
                Version = "DROPPED"
                DurationMs = $sw.ElapsedMilliseconds
            })
        }
        [System.Threading.Thread]::Sleep(100)
    }
})

Start-Sleep -Seconds 2

# Step 3: Trigger Rolling Update
Write-Host "[Rollout] Applying updated deployment manifest (05-deployment-v2.yaml)..." -ForegroundColor Yellow
kubectl apply -f $ManifestPath

Write-Host "[Rollout] Monitoring rollout status in real-time..." -ForegroundColor Yellow
kubectl rollout status deployment/student-k8s-app -n $Namespace

Start-Sleep -Seconds 2

# Step 4: Stop worker
$cts.Cancel()
$task.Wait(2000)

# Step 5: Results Analysis
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "                  TRAFFIC AUDIT SUMMARY RESULTS                       " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$results = $log.ToArray() | Sort-Object Id
$total = $results.Count
$success = ($results | Where-Object { $_.StatusCode -eq 200 }).Count
$failed = $total - $success
$v1 = ($results | Where-Object { $_.Version -eq "v1.0.0" }).Count
$v2 = ($results | Where-Object { $_.Version -eq "v2.0.0" }).Count

Write-Host "Total HTTP Requests Sent : $total"
Write-Host "Successful (HTTP 200 OK)  : $success" -ForegroundColor Green
Write-Host "Failed / Dropped Requests : $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "Requests served by v1.0.0: $v1"
Write-Host "Requests served by v2.0.0: $v2"

Write-Host "`nHTTP Status Code Breakdown:"
$results | Group-Object StatusCode | ForEach-Object {
    Write-Host "  HTTP $($_.Name): $($_.Count) requests"
}

Write-Host "======================================================================" -ForegroundColor Cyan
if ($total -gt 10 -and $failed -eq 0) {
    Write-Host "VERIFICATION RESULT: PASS" -ForegroundColor Green
    Write-Host "Zero downtime confirmed. 100% of requests returned HTTP 200 during transition." -ForegroundColor Green
} elseif ($failed -gt 0) {
    Write-Host "VERIFICATION RESULT: FAIL" -ForegroundColor Red
    Write-Host "Downtime detected! $failed requests failed during rolling update." -ForegroundColor Red
    exit 1
} else {
    Write-Host "VERIFICATION RESULT: INCONCLUSIVE (Sample size too small: $total requests)" -ForegroundColor Yellow
    exit 1
}
