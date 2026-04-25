# ACEest Fitness - Kubernetes Rollback Script
param(
    [string]$Deployment = "aceest-rolling"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "ACEest Fitness - Rollback Manager" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

Write-Host "`nCurrent rollout history for $Deployment :" -ForegroundColor Yellow
kubectl rollout history deployment/$Deployment

Write-Host "`nRolling back to previous revision..." -ForegroundColor Yellow
kubectl rollout undo deployment/$Deployment

Write-Host "`nWaiting for rollout to complete..." -ForegroundColor Yellow
kubectl rollout status deployment/$Deployment

Write-Host "`nCurrent pods:" -ForegroundColor Green
kubectl get pods -l app=aceest

Write-Host "`nRollback complete." -ForegroundColor Green
