# Test FloatChat ARGO API
# Make sure the server is running first with: uvicorn argo_llm_api:app --host 0.0.0.0 --port 8000 --reload

Write-Host "Testing FloatChat ARGO API..." -ForegroundColor Green

# Test 1: Health Check
Write-Host "`n1. Testing Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "Health Status: $($health.status)" -ForegroundColor Green
    Write-Host "Database: $($health.database)" -ForegroundColor Green  
    Write-Host "LLM: $($health.llm)" -ForegroundColor Green
} catch {
    Write-Host "Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Chat with ARGO data
Write-Host "`n2. Testing Chat with ARGO data..." -ForegroundColor Yellow
$chatBody = @{
    message = "What are the temperature conditions in the Arabian Sea?"
    include_data = $true
    max_profiles = 3
} | ConvertTo-Json

try {
    $chatResponse = Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -Body $chatBody -ContentType "application/json"
    Write-Host "Chat Response:" -ForegroundColor Green
    Write-Host $chatResponse.response -ForegroundColor White
    Write-Host "`nData Summary:" -ForegroundColor Green
    Write-Host "Profiles used: $($chatResponse.argo_data_summary.profiles_count)" -ForegroundColor White
    Write-Host "Target region: $($chatResponse.argo_data_summary.target_region)" -ForegroundColor White
} catch {
    Write-Host "Chat test failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Error details: $responseBody" -ForegroundColor Red
    }
}

# Test 3: Simple query without LLM
Write-Host "`n3. Testing Data Query without LLM..." -ForegroundColor Yellow
$queryBody = @{
    region = "Arabian_Sea"
    max_results = 2
} | ConvertTo-Json

try {
    $dataResponse = Invoke-RestMethod -Uri "http://localhost:8000/argo/data" -Method POST -Body $queryBody -ContentType "application/json"
    Write-Host "Data Query Response:" -ForegroundColor Green
    Write-Host "Profiles returned: $($dataResponse.summary.profiles_returned)" -ForegroundColor White
    Write-Host "Floats returned: $($dataResponse.summary.floats_returned)" -ForegroundColor White
} catch {
    Write-Host "Data query test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nAPI Testing Complete!" -ForegroundColor Green