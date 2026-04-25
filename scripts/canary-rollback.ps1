Write-Host "Rolling back canary deployment..." -ForegroundColor Red

kubectl scale deployment aceest-canary --replicas=0
kubectl scale deployment aceest-stable --replicas=5

Write-Host "Canary removed. All traffic on stable version." -ForegroundColor Green
kubectl get pods -l app=aceest-canary
