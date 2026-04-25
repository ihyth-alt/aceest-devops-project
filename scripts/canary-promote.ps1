Write-Host "Promoting canary to full deployment..." -ForegroundColor Yellow

kubectl scale deployment aceest-stable --replicas=0
kubectl scale deployment aceest-canary --replicas=5

Write-Host "Canary promoted. All traffic now on canary version." -ForegroundColor Green
kubectl get pods -l app=aceest-canary
