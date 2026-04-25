param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("blue","green")]
    [string]$Color
)

Write-Host "Switching aceest-bg-service to $Color deployment..." -ForegroundColor Yellow

$patchFile = "k8s/patch-$Color.yaml"

if (-Not (Test-Path $patchFile)) {
@"
spec:
  selector:
    app: aceest-bg
    color: $Color
"@ | Out-File -Encoding ascii $patchFile
}

kubectl patch service aceest-bg-service --patch-file $patchFile

Write-Host "Service now points to $Color." -ForegroundColor Green
